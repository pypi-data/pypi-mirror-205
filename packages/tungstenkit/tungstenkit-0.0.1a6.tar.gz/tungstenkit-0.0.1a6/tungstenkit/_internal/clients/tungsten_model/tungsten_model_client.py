import time
import typing as t
from pathlib import Path

from tungstenkit._internal.containerized_services import ModelService

from . import schemas
from .tungsten_model_api_client import TungstenModelAPIClient


class TungstenModelClient:
    def __init__(self, model_service: ModelService) -> None:
        self.service = model_service

        self.api = TungstenModelAPIClient(
            base_url=self.service.url, model_name=self.service.model.name
        )

    def predict(
        self, inputs: t.List[t.Dict], move_files_in_inputs: bool = False
    ) -> t.Tuple[schemas.PredictionResponse, t.List[Path]]:
        files: t.List[Path] = []
        inputs, files_in_inputs = self.service.convert_file_uris_in_inputs(
            inputs, move=move_files_in_inputs
        )
        files.extend(files_in_inputs)
        result = self.api.predict(inputs)
        if result.outputs:
            result.outputs, files_in_outputs = self.service.convert_file_uris_in_outputs(
                result.outputs
            )
            files.extend(files_in_outputs)
        return result, files

    def create_prediction(
        self,
        inputs: t.List[t.Dict],
        move_files_in_inputs: bool = False,
    ) -> t.Tuple[str, t.List[Path]]:
        inputs, files = self.service.convert_file_uris_in_inputs(inputs, move=move_files_in_inputs)
        return self.api.create_prediction(inputs), files

    def get_prediction(
        self, prediction_id: str
    ) -> t.Tuple[schemas.PredictionResponse, t.List[Path]]:
        result = self.api.get_prediction(prediction_id=prediction_id)
        files: t.List[Path] = []
        if result.outputs:
            result.outputs, files = self.service.convert_file_uris_in_outputs(result.outputs)

        return result, files

    def cancel_prediction(self, prediction_id: str):
        self.api.cancel_prediction(prediction_id)

    def predict_demo(
        self, inputs: t.List[t.Dict], move_files_in_inputs: bool = False
    ) -> t.Tuple[schemas.DemoResponse, t.List[Path]]:
        files: t.List[Path] = []
        inputs, files_in_inputs = self.service.convert_file_uris_in_inputs(
            inputs, move=move_files_in_inputs
        )
        files.extend(files_in_inputs)
        prediction_id = self.api.create_demo(inputs)
        while True:
            result = self.api.get_demo(prediction_id)
            if result.status == "success" or result.status == "failure":
                break

            time.sleep(0.1)

        if result.outputs:
            result.outputs, files_in_outputs = self.service.convert_file_uris_in_outputs(
                result.outputs
            )
            files.extend(files_in_outputs)
        if result.demo_outputs:
            result.demo_outputs, files_in_demo_outputs = self.service.convert_file_uris_in_outputs(
                result.demo_outputs
            )
            files.extend(files_in_demo_outputs)
        return result, files

    def create_demo(
        self,
        inputs: t.List[t.Dict],
        move_files_in_inputs: bool = False,
    ) -> t.Tuple[str, t.List[Path]]:
        inputs, files = self.service.convert_file_uris_in_inputs(inputs, move=move_files_in_inputs)
        return self.api.create_demo(inputs), files

    def get_demo(self, prediction_id: str) -> t.Tuple[schemas.DemoResponse, t.List[Path]]:
        result = self.api.get_demo(prediction_id=prediction_id)
        files: t.List[Path] = []
        if result.outputs:
            result.outputs, files_in_outputs = self.service.convert_file_uris_in_outputs(
                result.outputs
            )
            files.extend(files_in_outputs)
        if result.demo_outputs:
            result.demo_outputs, files_in_demo_outputs = self.service.convert_file_uris_in_outputs(
                result.demo_outputs
            )
            files.extend(files_in_demo_outputs)

        return result, files

    def cancel_demo(self, prediction_id: str):
        self.api.cancel_demo(prediction_id)
