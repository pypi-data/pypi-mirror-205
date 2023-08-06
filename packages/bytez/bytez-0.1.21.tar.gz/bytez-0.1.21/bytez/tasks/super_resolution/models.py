from dataclasses import dataclass
from bytez.tasks.super_resolution._models.dsrvae import HolmesAlanDsrvaeModel


@dataclass
class _SuperResolutionModels:
    holmes_alan_dsrvae = HolmesAlanDsrvaeModel


@dataclass
class SuperResolutionModels:
    models = _SuperResolutionModels
