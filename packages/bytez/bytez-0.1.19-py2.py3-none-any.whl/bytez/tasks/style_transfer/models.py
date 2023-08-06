from dataclasses import dataclass
import enum
from enum import Enum
from bytez.tasks.style_transfer._models.cmd_style_transfer import CmdStyleTransferModel
from bytez.tasks.style_transfer._models.fast_style_transfer import FastStyleTransferModel
from bytez.tasks.style_transfer._models.tensorflow_fast_style import TensorFlowFastStyleTransferModel


@dataclass
class _StyleTransferModels:
    fast_style_transfer = FastStyleTransferModel
    cmd_style_transfer = CmdStyleTransferModel
    tensorflow_fast_style = TensorFlowFastStyleTransferModel


@dataclass
class StyleTransferModels:
    models = _StyleTransferModels()
