from dataclasses import dataclass
from bytez.tasks.super_resolution.models import SuperResolutionModels
from bytez.tasks.style_transfer.models import StyleTransferModels


@dataclass
class Tasks:
    super_resolution = SuperResolutionModels
    style_transfer = StyleTransferModels
