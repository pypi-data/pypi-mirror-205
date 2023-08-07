import multiprocessing as mp
import os
import signal
import tempfile
import time
import traceback
import typing as t
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from pathlib import Path
from threading import Lock

import attrs
import pydantic
from fastapi.encoders import jsonable_encoder

from tungstenkit import exceptions
from tungstenkit._internal.io import BaseIO, File
from tungstenkit._internal.model import IOClasses, TungstenModel
from tungstenkit._internal.utils.console import LogFileRedirector
from tungstenkit._internal.utils.pydantic import run_validation

from .. import server_exceptions

ACK_TIMEOUT_SEC = 1


@attrs.define
class PredictionRequest:
    inputs: t.List[t.Dict]
    is_demo: bool
    log_path: t.Optional[Path] = None


@attrs.define(kw_only=True)
class PredictionSuccess:
    outputs: t.List[t.Dict]
    demo_outputs: t.List[t.Optional[t.Dict]]
    files: t.List[File]


@attrs.define
class PredictionFailure:
    err_msg: str


class WorkerSubprocess(mp.Process):
    def __init__(
        self, model_module: str, model_class: str, setup_timeout: float, prediction_timeout: float
    ) -> None:
        self.model_module = model_module
        self.model_class = model_class
        self.setup_timeout = float(setup_timeout)
        self.predict_timeout = float(prediction_timeout)

        self._conn_in_mainproc, self._conn_in_subproc = mp.Pipe(duplex=True)
        self._lock = Lock()
        self._is_running: bool = False

        self._model: t.Optional[TungstenModel] = None
        self._io_classes: t.Optional[IOClasses] = None

        fd, path_str = tempfile.mkstemp()
        os.close(fd)
        self._setup_log_path = Path(path_str)
        fd, path_str = tempfile.mkstemp()
        self._predict_log_path = Path(path_str)
        os.close(fd)

        super().__init__(daemon=True, name="worker-subprocess")

    def setup(self) -> bool:
        start_time = time.monotonic()

        try:
            log_file_redirector = LogFileRedirector(self._setup_log_path)
            while self.is_alive() and not self._conn_in_mainproc.poll(0.1):
                log_file_redirector.update()
                if time.monotonic() - start_time > self.setup_timeout:
                    self.terminate()
                    raise server_exceptions.SetupFailed("Timeout")

            if self.is_alive():
                self._conn_in_mainproc.recv()
            log_file_redirector.update()
            if not self.is_alive():
                return False
            return True
        except BaseException:
            return False

    def predict(
        self,
        inputs: t.List[t.Dict],
        is_demo: bool,
        log_path: t.Optional[Path],
    ) -> t.Union[PredictionSuccess, PredictionFailure]:
        # Acquire lock to block cancelation
        with self._lock:
            assert self.pid is not None
            req = PredictionRequest(
                inputs=[jsonable_encoder(inp) for inp in inputs],
                is_demo=is_demo,
                log_path=log_path,
            )
            self._conn_in_mainproc.send(req)

            start_time = time.monotonic()

            # Wait unitl ack received
            while self.is_alive() and not self._conn_in_mainproc.poll(0.01):
                pass
            if not self.is_alive():
                raise server_exceptions.SubprocessTerminated(self._predict_log_path.read_text())
            self._conn_in_mainproc.recv()

        # Wait until result received
        while self.is_alive() and not self._conn_in_mainproc.poll(0.05):
            if time.monotonic() - start_time > self.predict_timeout:
                os.kill(self.pid, signal.SIGUSR2)
                break

        if not self.is_alive():
            raise server_exceptions.SubprocessTerminated(self._predict_log_path.read_text())

        return self._conn_in_mainproc.recv()

    def cancel(self):
        with self._lock:
            assert self.pid is not None
            os.kill(self.pid, signal.SIGUSR1)

    def run(self):
        with ExitStack() as exit_stack:
            _redirect_stream(exit_stack, self._setup_log_path, flush=True)

            signal.signal(signal.SIGUSR1, self._handle_cancellation)
            signal.signal(signal.SIGUSR2, self._handle_timeout)

            self._model = TungstenModel._from_module(self.model_module, self.model_class)
            self._io_classes = self._model._get_io_classes()
            self._model.setup()
            self._conn_in_subproc.send(None)

        with ExitStack() as exit_stack:
            _redirect_stream(exit_stack, self._predict_log_path, flush=True)
            while True:
                received: PredictionRequest = self._conn_in_subproc.recv()
                inputs = [self._io_classes.input.parse_obj(inp) for inp in received.inputs]
                is_demo = received.is_demo
                log_path = received.log_path
                if log_path:
                    exit_stack.pop_all()
                    _redirect_stream(exit_stack, log_path, flush=False)
                prediction_result = self._predict(inputs=inputs, is_demo=is_demo)
                exit_stack.pop_all()
                _redirect_stream(exit_stack, self._predict_log_path, flush=True)
                self._conn_in_subproc.send(prediction_result)

    def _predict(
        self,
        inputs: t.List[t.Dict],
        is_demo: bool,
    ) -> t.Union[PredictionSuccess, PredictionFailure]:
        assert self._model
        assert self._io_classes

        try:
            self._is_running = True
            # Send ACK to the main proc and release lock blocking cancelation
            self._conn_in_subproc.send(None)

            # print(f"working dir: {Path('.').resolve()}")
            parsed_inputs = [self._io_classes.input.parse_obj(inp) for inp in inputs]
            if is_demo:
                fn_name = self._model.__class__.__name__ + "." + self._model.predict_demo.__name__
                tup = self._model.predict_demo(parsed_inputs)
                try:
                    it = iter(tup)
                except TypeError:
                    raise exceptions.InvalidOutput(
                        f"Return of '{fn_name}' is not iterable. "
                        "It should return both 'outputs' and 'demo_outputs'."
                    )
                try:
                    outputs = next(it)
                except StopIteration:
                    raise exceptions.InvalidOutput(f"Return of '{fn_name}' has no element. ")
                try:
                    demo_outputs: t.Sequence[t.Any] = next(it)
                except StopIteration:
                    raise exceptions.InvalidOutput(
                        f"Return of '{fn_name}' has only 1 element. "
                        "It should return both 'outputs' and 'demo_outputs'."
                    )
                try:
                    iter(outputs)
                except TypeError:
                    raise exceptions.InvalidOutput(
                        f"Outputs (the first return value of '{fn_name}') are not iterable."
                    )
                try:
                    iter(demo_outputs)
                except TypeError:
                    raise exceptions.InvalidOutput(
                        f"Demo outputs (the second return value of '{fn_name}') are not "
                        "iterable."
                    )

            else:
                fn_name = self._model.__class__.__name__ + self._model.predict.__name__
                outputs = self._model.predict(parsed_inputs)
                try:
                    iter(outputs)
                except TypeError:
                    raise exceptions.InvalidOutput(
                        f"Outputs (the return value of '{fn_name}') are not iterable."
                    )
                demo_outputs = [None] * len(outputs)

            files = _get_files([outputs, demo_outputs])

            validated_outputs = _validate_and_serialize_outputs(outputs, self._io_classes.output)
            validated_demo_outputs = _validate_and_serialize_demo_outputs(demo_outputs)

            self._is_running = False
            return PredictionSuccess(
                outputs=validated_outputs, demo_outputs=validated_demo_outputs, files=files
            )

        except BaseException as e:
            self._is_running = False
            if isinstance(e, server_exceptions.PredictionCanceled):
                err_msg = "Canceled"
            elif isinstance(e, server_exceptions.PredictionTimeout):
                err_msg = "Timeout"
            else:
                err_msg = traceback.format_exc()
            print(err_msg)
            return PredictionFailure(err_msg=err_msg)

    def _handle_cancellation(self, *args, **argv):
        if self._is_running:
            raise server_exceptions.PredictionCanceled

    def _handle_timeout(self, *args, **argv):
        if self._is_running:
            raise server_exceptions.PredictionTimeout


def _get_files(outputs: t.Any) -> t.List[File]:
    files = []
    if isinstance(outputs, File):
        files.append(outputs)

    elif isinstance(outputs, list) or isinstance(outputs, tuple):
        for item in outputs:
            files.extend(_get_files(item))

    elif isinstance(outputs, dict):
        for item in outputs.values():
            files.extend(_get_files(item))

    elif isinstance(outputs, BaseIO):
        for field_name in outputs.__fields__.keys():
            files.extend(_get_files(getattr(outputs, field_name)))

    return files


def _validate_and_serialize_demo_outputs(
    demo_outputs: t.Iterable,
) -> t.List[t.Optional[t.Dict]]:
    validated_demo_outputs: t.List[t.Optional[t.Dict]] = []
    for o in demo_outputs:
        if o is None:
            validated_demo_outputs.append(o)
        elif isinstance(o, BaseIO) or isinstance(o, dict):
            validated_demo_outputs.append(jsonable_encoder(o))
            # TODO validate
        else:
            raise exceptions.InvalidOutput(
                f"Invalid demo output type: {type(o)}. " f"Allowed types: 'dict' and '{BaseIO}'"
            )

    return validated_demo_outputs


def _validate_and_serialize_outputs(
    outputs: t.Iterable, output_cls: t.Type[BaseIO]
) -> t.List[t.Dict]:
    validated_outputs: t.List[t.Dict] = []
    for o in outputs:
        try:
            if isinstance(o, output_cls):
                validated_outputs.append(jsonable_encoder(run_validation(o)))
            elif isinstance(o, dict):
                validated_outputs.append(jsonable_encoder(output_cls.parse_obj(o)))
            else:
                raise exceptions.InvalidOutput(
                    f"Invalid output type: {type(o)}. Allowed types: 'dict' and '{output_cls}'"
                )
        except pydantic.error_wrappers.ValidationError as e:
            raise exceptions.InvalidOutput(str(e))

    return validated_outputs


def _redirect_stream(exit_stack: ExitStack, path: Path, flush: bool = True):
    f = exit_stack.enter_context(open(path, "w+", buffering=1))
    if flush:
        f.flush()
    exit_stack.enter_context(redirect_stderr(f))
    exit_stack.enter_context(redirect_stdout(f))
