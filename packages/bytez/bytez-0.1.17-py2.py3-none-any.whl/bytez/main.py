from dataclasses import dataclass
from bytez.tasks.style_transfer.models import StyleTransferModels
from bytez.tasks.super_resolution.models import SuperResolutionModels


@dataclass
class Tasks:
    super_resolution = SuperResolutionModels
    style_transfer = StyleTransferModels


@dataclass
class Pipeline:
    tasks = Tasks()
