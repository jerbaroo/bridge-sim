"""Parameters for FEM simulations."""
from typing import List

from model import *


class FEMParams:
    """Parameters for a FEM simulation.

    NOTE:
      - Currently only static loads.

    Attributes:
        loads: [Load], a list of Load.
        response_types: [ResponseType], response types to record.
    """
    def __init__(self, loads: [Load]=[],
                 response_types: [ResponseType]=all_response_types):
        self.loads=loads
        self.response_types = response_types
        self.built_model_file = None

    # TODO: Rename for simulation-dependent results.
    def __str__(self):
        lstr = ",".join(str(l) for l in self.loads)
        return f"[{lstr}]"


class ExptParams:
    def __init__(self, fem_params: List[FEMParams]):
        self.fem_params = fem_params


if __name__ == "__main__":
    fem_params = FEMParams(loads=[Load(0.5, 5e3), Load(0.2, 5e1)])
    print(fem_params)
