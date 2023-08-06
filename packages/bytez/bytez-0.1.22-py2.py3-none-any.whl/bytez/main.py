from dataclasses import dataclass
from bytez.tasks import Tasks


@dataclass
class Pipeline:
    tasks = Tasks()
