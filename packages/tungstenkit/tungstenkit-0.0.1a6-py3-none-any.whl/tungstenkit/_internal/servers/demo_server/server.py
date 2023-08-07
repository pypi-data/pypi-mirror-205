import signal
import typing as t
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from tungstenkit._internal.clients import TungstenModelClient
from tungstenkit._internal.containerized_services import ModelService
from tungstenkit._internal.local_store import LocalStore
from tungstenkit._internal.logging import log_error

from . import schemas
from .services import ExampleService, FileService, PredictionService

frontend_dir_in_pkg = Path(__file__).parent / "frontend"


def create_demo_app(tmp_dir: Path, model_service: ModelService):
    # TODO https
    # TODO issue access token like jupyter
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    frontend_dir_in_tmp_dir = tmp_dir / "frontend"
    frontend_dir_in_tmp_dir.symlink_to(frontend_dir_in_pkg)

    _add_api_endpoints(
        app=app,
        model_service=model_service,
        file_dir=tmp_dir / "files",
    )
    _mount_frontend_dir(app=app, dir=frontend_dir_in_tmp_dir)

    return app


def _add_api_endpoints(
    app: FastAPI,
    model_service: ModelService,
    file_dir: Path,
):
    store = LocalStore()
    model = model_service.model
    model_client = TungstenModelClient(model_service=model_service)
    file_service = FileService(base_dir=file_dir)
    prediction_service = PredictionService(file_service=file_service, model_client=model_client)
    example_service = ExampleService(
        model_name=model.name, file_service=file_service, prediction_service=prediction_service
    )
    file_gc_thread = file_service.start_garbage_collection()
    prediction_gc_thread = prediction_service.start_garbage_collection()
    is_gc_error_printed = False

    def log_gc_errors(*args, **argv):
        if not is_gc_error_printed:
            if not prediction_gc_thread.is_alive():
                log_error("Prediction garbage collector is unexpectedly terminated")
            if not file_gc_thread.is_alive():
                log_error("File garbage collector is unexpectedly terminated")

    signal.signal(signal.SIGUSR2, log_gc_errors)

    @app.get("/metadata", response_model=schemas.Metadata)
    def get_model_metadata(req: Request):
        return schemas.Metadata.build(
            model=store.get_model(model.name), file_service=file_service, request=req
        )

    @app.post("/predictions", response_model=schemas.PostPredictionResponse)
    def create_prediction(body: schemas.PostPredictionRequest, req: Request):
        prediction_id = prediction_service.create_prediction(input=body.__root__, request=req)
        return schemas.PostPredictionResponse(prediction_id=prediction_id)

    @app.get("/predictions/{prediction_id}", response_model=schemas.Prediction)
    def get_prediction(prediction_id: str, req: Request):
        return prediction_service.get_prediction_by_id(prediction_id=prediction_id, request=req)

    @app.post("/predictions/{prediction_id}/save", response_model=schemas.PostExampleResponse)
    def save_prediction_as_example(prediction_id: str, req: Request):
        pred = prediction_service.get_prediction_by_id(prediction_id, request=req)
        if pred.status != "success":
            raise HTTPException(status_code=422, detail="Not a succeeded prediction")

        example_id = example_service.add_example_by_prediction_id(prediction_id)
        return schemas.PostExampleResponse(example_id=example_id)

    @app.post("/predictions/{prediction_id}/cancel")
    def cancel_prediction(prediction_id: str):
        prediction_service.cancel_prediction_by_id(prediction_id)

    @app.get("/examples", response_model=t.List[schemas.Example])
    def list_examples(req: Request):
        return example_service.list_examples(req)

    @app.delete("/examples/{example_id}")
    def delete_example(example_id: str):
        example_service.delete_by_example_id(example_id)

    @app.post("/files", response_model=schemas.FileUploadResponse)
    def upload_file(file: UploadFile, req: Request):
        filename = file_service.add_file_by_buffer(
            filename=file.filename if file.filename else "file", buf=file.file, protected=False
        )
        return schemas.FileUploadResponse(
            serving_url=file_service.build_serving_url(filename, request=req)
        )

    @app.get(
        "/files/{filename}",
        response_class=FileResponse,
        dependencies=[Depends(file_service.acquire_read_lock)],
        name="files",
    )
    def get_file(filename: str):
        if not file_service.check_existence(filename, strict=True):
            raise HTTPException(status_code=404, detail=filename)
        path = file_service.get_path_by_filename(filename).resolve()
        return FileResponse(path=path)


def _mount_frontend_dir(app: FastAPI, dir: Path):
    app.mount("/", StaticFiles(directory=dir, html=True), name="webapp")
    # from fastapi import Request
    # from starlette.exceptions import HTTPException as StarletteHTTPException
    # from fastapi.exception_handlers import http_exception_handler
    # @app.exception_handler(StarletteHTTPException)
    # async def _redirect_to_home(req: Request, exc: StarletteHTTPException):
    #     # if req.url.path.startswith("model_static"):
    #     #     return RedirectResponse(urljoin(model_api_url, req.url.path))
    #     if exc.status_code == 404:
    #         return RedirectResponse("/")
    #     else:
    #         return await http_exception_handler(req, exc)
