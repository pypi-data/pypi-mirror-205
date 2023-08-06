from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .user import User


class ModelCreate(BaseModel):
    docker_image: str

    input_schema: dict
    output_schema: dict

    description: str
    batch_size: int

    gpu: bool
    gpu_min_memory: Optional[int] = None


class Model(BaseModel):
    id: int
    version: str
    description: Optional[str] = None

    docker_image: str
    docker_image_size: int

    input_schema: dict
    output_schema: dict

    os: str
    architecture: str
    gpu: bool

    has_readme: bool
    source_files_count: int
    examples_count: int

    creator: User
    created_at: datetime


class ModelReadmeUpdate(BaseModel):
    content: str


class ModelPredictionExampleCreate(BaseModel):
    input: dict
    output: dict
    demo_output: dict
    input_files: List[str]
    output_files: List[str]


class ModelPredictionExample(BaseModel):
    id: int

    input: dict
    output: dict
    demo_output: dict

    creator: User
    created_at: datetime


class ListModelPredictionExamples(BaseModel):
    __root__: List[ModelPredictionExample]
