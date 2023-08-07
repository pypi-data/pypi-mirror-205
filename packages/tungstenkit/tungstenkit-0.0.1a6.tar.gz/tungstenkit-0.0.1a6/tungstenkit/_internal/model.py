import abc
import importlib
import inspect
import typing as t

import pydantic

from tungstenkit import exceptions
from tungstenkit._internal import io
from tungstenkit._internal.configs import ModelConfig
from tungstenkit._internal.io_schema import IOClasses, validate_input_class, validate_output_class
from tungstenkit._internal.utils.imports import check_module, import_module_in_lazy_import_ctx
from tungstenkit._internal.utils.typing import get_type_args, get_type_origin

InputType = t.TypeVar("InputType", bound=io.BaseIO)
OutputType = t.TypeVar("OutputType", bound=io.BaseIO)


class _ModelMeta(abc.ABCMeta):
    def __new__(*args, **argv):
        cls = abc.ABCMeta.__new__(*args, **argv)
        return cls

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        type_args = cls.get_type_args()

        # Validate only when cls is a strict subclass of TungstenModel.
        # The TungstenModel class itself cannot be instantiated since it is a abstract class.
        if type_args is not None:
            cls.validate_type_args(type_args)
            cls.validate_setup_fn()
            cls.validate_predict_fn()
            cls._type_args = type_args

    def get_type_args(cls: "t.Type[TungstenModel]") -> t.Optional[t.Tuple]:  # type: ignore
        mro = inspect.getmro(cls)
        base_class = mro[-3]
        for base in cls.__orig_bases__:  # type: ignore
            if get_type_origin(base) is base_class:
                args = get_type_args(base)
                return args
        if len(mro) <= 3:
            return None
        else:
            return tuple()

    def validate_type_args(cls: "t.Type[TungstenModel]", type_args: t.Tuple):  # type: ignore
        if len(type_args) != 2:
            raise exceptions.TungstenModelError(
                f"'{TungstenModel.__name__}' should have 2 type arguments, "
                f"not {len(type_args)}: 'InputType' and 'OutputType'."
            )
        input_type = type_args[0]
        validate_input_class(input_type)
        output_type = type_args[1]
        validate_output_class(output_type)

    def validate_setup_fn(cls: "t.Type[TungstenModel]"):  # type: ignore
        setup_args = inspect.getfullargspec(cls.setup).args
        if len(setup_args) > 1:
            fn_name = cls.__class__.__name__ + "." + cls.setup.__name__
            raise exceptions.TungstenModelError(f"Too many args for '{fn_name}'")

    def validate_predict_fn(cls: "t.Type[TungstenModel]"):  # type: ignore
        pred_args = inspect.getfullargspec(cls.predict).args
        if len(pred_args) > 2:
            raise exceptions.TungstenModelError(
                f"Too many args for '{cls.__class__.__name__ + '.' + cls.predict.__name__}'"
            )
        elif len(pred_args) < 2:
            raise exceptions.TungstenModelError(
                f"'{cls.__class__.__name__ + '.' + cls.predict.__name__}' has no argument 'inputs'"
            )


class TungstenModel(t.Generic[InputType, OutputType], metaclass=_ModelMeta):
    """
    Base class for all Tungsten models.

    Your models should also subclass this class.

    This class should take two classes as type arguments,
    which define input and output types respectively.

    ```python
    from typing import List
    from tungstenkit import model, io

    class Input(io.BaseIO):
        # Define your input fields
        pass

    class Output(io.BaseIO):
        # Define your output fields
        pass

    class Model(model.TungstenModel[Input, Output]):
        def setup(self):
            # Setup your model
            pass

        def predict(self, inputs: List[Input]) -> List[Output]:
            # Run a (batch) prediction
            pass
    ```
    """

    __model_config: t.Optional[ModelConfig] = None
    _type_args: t.Tuple[InputType, OutputType]

    def setup(self) -> t.Any:
        pass

    @abc.abstractmethod
    def predict(self, inputs: t.List[InputType]) -> t.Sequence[OutputType]:
        pass

    def predict_demo(
        self, inputs: t.List[InputType]
    ) -> t.Tuple[t.Sequence[OutputType], t.Sequence[t.Union[t.Dict[str, t.Any], io.BaseIO]]]:
        outputs = self.predict(inputs)
        return outputs, outputs

    @classmethod
    def _get_model_config(cls) -> ModelConfig:
        if cls.__model_config is None:
            return ModelConfig.with_types(cls._get_io_classes())(
                environment_variables={
                    "TUNGSTEN_MODEL_MODULE": cls.__module__,
                    "TUNGSTEN_MODEL_CLASS": cls.__name__,
                },
                description=cls.__name__,
            )
        return cls.__model_config

    @classmethod
    def _set_model_config(cls, value: ModelConfig):
        if not value.description:
            value.description = cls.__name__
        value.environment_variables["TUNGSTEN_MODEL_MODULE"] = cls.__module__
        value.environment_variables["TUNGSTEN_MODEL_CLASS"] = cls.__name__
        cls.__model_config = value

    @staticmethod
    def _from_module(mod: str, cls: str, lazy_import: bool = False, **kwargs) -> "TungstenModel":
        if not check_module(mod):
            raise exceptions.TungstenModelError(f"Module not found: {mod}")
        if lazy_import:
            help_msg_on_lazy_import_err = (
                f"Lazy import of module '{mod}' is failed. "
                "Modules not found should not be executed during lazy import."
            )
            tungsten_model_module = import_module_in_lazy_import_ctx(
                mod,
                help_msg_on_lazy_import_err,
            )
        else:
            tungsten_model_module = importlib.import_module(mod)
        if not hasattr(tungsten_model_module, cls):
            raise exceptions.TungstenModelError(f"Class '{cls}' is not defined in module '{mod}'")
        model_class: t.Type[TungstenModel] = getattr(tungsten_model_module, cls)
        return model_class(**kwargs)

    @classmethod
    def _get_io_classes(cls: "t.Type[TungstenModel]") -> IOClasses:
        return IOClasses(input=cls._type_args[0], output=cls._type_args[1])


# TODO Support TPU
# TODO Support multi-platform builds


def config(
    *,
    gpu: bool = False,
    description: t.Optional[str] = None,
    python_packages: t.Optional[t.List[str]] = None,
    python_version: t.Optional[str] = None,
    system_packages: t.Optional[t.List[str]] = None,
    cuda_version: t.Optional[str] = None,
    readme_md: t.Optional[str] = None,
    batch_size: int = 1,
    gpu_mem_gb: int = 16,
    mem_gb: int = 8,
    include_files: t.Optional[t.List[str]] = None,
    exclude_files: t.Optional[t.List[str]] = None,
    dockerfile_commands: t.Optional[t.List[str]] = None,
    base_image: t.Optional[str] = None,
) -> "t.Callable[[t.Type[TungstenModel]], t.Type[TungstenModel]]":
    r"""Returns a class decorator that sets the model configuration.

    The base docker image, maybe a cuda image, and the python version can be inferred
    for following pip packages:

    ``torch``, ``torchvision``, ``torchaudio``, and ``tensorflow``.

    While inferring, the runtime python version is preferred.

    Args:
        gpu: Indicates if the model requires GPUs.

        description (str | None): A text explaining the model.

        python_packages (list[str] | None): A list of pip requirements in ``<name>[==<version>]``
            format. If ``None`` (default), no python packages are added.

        python_version (str | None): Python version to use in ``<major>[.<minor>[.<micro>]]``
            format.
            If ``None`` (default), the python version will be automatically determined
            as compatible with pip packages while prefering the runtime python version.
            Otherwise, fix the python version as ``python_version``.

        system_packages (list[str] | None): A list of system packages, which are installed
            by the system package manager (e.g. ``apt``). This argument will be ignored while
            using a custom base image with which tungstenkit cannot decide which package manager to
            use.

        cuda_version (str | None): CUDA version in ``<major>[.<minor>[.<patch>]]`` format.
            If ``None`` (default), the cuda version will be automatically determined as compatible
            with pip packages. Otherwise, fix the CUDA version as ``cuda_version``. Raises
            ValueError if ``gpu`` is ``False`` but ``cuda_version`` is not None.

        readme_md (str | None): Path to the ``README.md`` file.

        batch_size (int): Max batch size for adaptive batching.

        gpu_mem_gb (int): Minimum GPU memory size required to run the model. This argument will be
            ignored if ``gpu==False``.

        mem_gb (int): Minimum memory size required to run the model.

        include_files (list[str] | None): A list of patterns as in ``.gitignore``.
            If ``None`` (default), all files in the working directory and its subdirectories
            are added, which is equivalent to ``[*]``.

        exclude_files (list[str] | None): A list of patterns as in ``.gitignore`` for matching
            which files to exclude.
            If ``None`` (default), all hidden files and Python bytecodes are ignored,
            which is equivalent to ``[".*/", "__pycache__/", "*.pyc", "*.pyo", "*.pyd"]``.

        dockerfile_commands (list[str] | None): A list of dockerfile commands. The commands will
            be executed *before* setting up python packages.

        base_image (str | None): Base docker image in ``<repository>[:<tag>]`` format.
            If ``None`` (default), the base image is automatically selected with respect to
            pip packages, the gpu flag, and the CUDA version. Otherwise, use it as the base image
            and ``system_packages`` will be ignored.
    """
    args = {name: value for name, value in locals().items() if value is not None}

    def wrap(cls: "t.Type[TungstenModel]") -> "t.Type[TungstenModel]":
        io_classes = cls._get_io_classes()
        try:
            model_config = ModelConfig.with_types(io_classes)(**args)
        except pydantic.ValidationError as e:
            raise exceptions.ModelConfigError(
                str(e).replace(
                    f"for {ModelConfig.__name__}",
                    f"in '{cls.__module__}.{cls.__name__}'",
                    1,
                )
            )
        cls._set_model_config(model_config)
        return cls

    return wrap
