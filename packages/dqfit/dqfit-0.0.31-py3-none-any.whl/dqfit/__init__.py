from typing import List
from pathlib import Path

import dqfit.io as io
from dqfit.model import DQIBase, DQI2, DQI3
from dqfit.dimensions import Conformant, Complete, Plausible
from dqfit.transform import transform_to_fhir_path


def read_fhir(dir: str) -> List[dict]:
    return io.read_fhir(dir)

PACKAGE_BASE = Path(__file__).parent.absolute()

__all__ = [
    "DQIBase",
    "DQI2",
    "DQI3",
    "Conformant",
    "Complete",
    "Plausible",
    "read_fhir"
]
