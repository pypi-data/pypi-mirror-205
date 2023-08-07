# Tungstenkit
**Tungstenkit** is an open-source tool for building and using versatile and standardized ML model containers, Tungsten models. Key features of Tungsten models are:

- **Easy**: [Require only a few lines of Python code.](#build-a-tungsten-model)
- **Versatile**: Support multiple usages:
    - [RESTful API server](#run-it-as-a-restful-api-server)
    - [GUI application](#run-it-as-a-gui-application)
    - [Serverless function](#run-it-as-a-serverless-function)
    - CLI application (coming soon)
    - Python function (coming soon)
- **Abstracted**: [User-defined JSON input/output.](#run-it-as-a-restful-api-server)
- **Standardized**: [Support advanced workflows.](#run-it-as-a-restful-api-server)
- **Scalable**: Support adaptive batching and clustering (coming soon).



# Learn More
- [Documentation](https://tungsten-ai.github.io/docs/tungsten_model)
- [Getting Started](https://tungsten-ai.github.io/docs/tungsten_model/getting_started/)
- [Installation](#prerequisites)


# Take the tour
## Build a Tungsten model
Building a Tungsten model is easy. All you have to do is write a simple ``tungsten_model.py`` like below:

```python
from typing import List

import torch
from tungstenkit import io, model


class Input(io.BaseIO):
    prompt: str


class Output(io.BaseIO):
    image: io.Image


@model.config(
    gpu=True,
    python_packages=["torch", "torchvision"],
    batch_size=4,
    description="Text to image"
)
class Model(model.TungstenModel[Input, Output]):
    def setup(self):
        weights = torch.load("./weights.pth")
        self.model = load_torch_model(weights)

    def predict(self, inputs: List[Input]) -> List[Output]:
        input_tensor = preprocess(inputs)
        output_tensor = self.model(input_tensor)
        outputs = postprocess(output_tensor)
        return outputs
```

Now, you can start a build process with the following command:
```console
$ tungsten build

✅ Successfully built tungsten model: 'text-to-image:latest'
```


## Run it as a RESTful API server

You can start a prediction with a REST API call.

Start a server:

```console
$ docker run -p 3000:3000 --gpus all text-to-image:latest

INFO:     Setting up the model
INFO:     Getting inputs from the input queue
INFO:     Starting the prediction service
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

Send a prediction request with a JSON payload:

```console
$ curl -X 'POST' 'http://localhost:3000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[{"prompt": "a professional photograph of an astronaut riding a horse"}]'

{
    "status": "success",
    "outputs": [{"image": "data:image/png;base64,..."}],
    "error_message": null
}
```

## Run it as a GUI application
If you need a more user-friendly way to make predictions, start a GUI app with the following command:

```console
$ tungsten demo text-to-image:latest -p 8080

INFO:     Uvicorn running on http://localhost:8080 (Press CTRL+C to quit)
```

![tungsten-dashboard](https://github.com/tungsten-ai/assets/blob/main/common/local-model-demo.gif?raw=true "Tungsten Dashboard")

## Run it as a serverless function
We support remote, serverless executions via a [Tungsten server](https://tungsten-ai.github.io/docs/#tungsten-server).

Push a model:

```console
$ tungsten push exampleuser/exampleproject -n text-to-image:latest

✅ Successfully pushed to 'https://server.tungsten-ai.com'
```

Now, you can start a remote prediction in the Tungsten server:

![tungsten-platform-model-demo](https://github.com/tungsten-ai/assets/blob/main/common/platform-model-demo.gif?raw=true "Tungsten Platform Model Demo")


# Prerequisites
- Python 3.7+
- [Docker](https://docs.docker.com/engine/install/)
- (Optional) [nvidia-docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) for running GPU models locally. 


# Installation
```shell
pip install tungstenkit
```