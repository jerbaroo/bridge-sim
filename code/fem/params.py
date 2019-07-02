"""
Parameters for FEM simulations.
"""
from model import *


class FEMParams():
    """Parameters for FEM simulations.

    NOTE:
      - Currently only static loads.

    Attributes:
        simulations: [[Load]], a list of Load per simulation.
    """
    def __init__(self, simulations: [[Load]]=[]):
        self.simulations=simulations

    def __str__(self):
        return "-".join(
            f"[{lstr}]" for lstr in (
                ",".join(str(l) for l in loads)
                for loads in self.simulations))


if __name__ == "__main__":
    fem_params = FEMParams(
        simulations=[[Load(0.5, 5e3), Load(0.2, 5e1)], [Load(0.6, 5e2)]])
    print(fem_params.id_str())
