import json
from typing import BinaryIO, Literal, get_args
from dataclasses import dataclass
import requests
import os

current_module_path = os.path.abspath(__file__)
current_module_dir = os.path.dirname(current_module_path)

with open(f'{current_module_dir}/tasks.json', 'r') as file:
    tasks = json.loads(file.read())


@dataclass
class Handler:
    url: str

    def inference(self, input_img: BinaryIO) -> bytes:
        files = {'image': input_img}
        response = requests.post(self.url, files=files)

        # reset seek index to start of file
        input_img.seek(0)

        if not response.ok:
            raise Exception(f'Request failed with {response.status_code}')

        return response.content

# TODO use enums to accomplish this


def pipeline(task,
             model) -> Handler:
    task = tasks.get(task)

    if not task:
        raise Exception(f"{task} is not supported by this package.")

    url = task.get(model)

    if not url:
        raise Exception(f"{model} is not supported by this package.")

    return Handler(url=url)
