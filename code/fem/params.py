"""Parameters for FEM simulations."""
from typing import List

from model import *


class FEMParams:
    """Parameters for a FEM simulation.

    NOTE:
      - Currently only static loads.

    Attributes:
        loads: [Load], a list of Load to place on the bridge.
        response_types: [ResponseType], response types to record.
    """
    def __init__(self, loads: [Load]=[],
                 response_types: [ResponseType]=[rt for rt in ResponseType]):
        self.loads=loads
        self.response_types = response_types
        self.built_model_file = None

    def load_str(self):
        """String representing the loads."""
        lstr = ",".join(str(l) for l in self.loads)
        return f"[{lstr}]"


class ExptParams:
    """Parameters for multiple simulations."""
    def __init__(self, fem_params: List[FEMParams]):
        self.fem_params = fem_params

    def is_mobile_load(self):
        """"Whether each simulation is equal apart from load position.

        Additionally each simulation must only have one load, and the
        loads must be increasing with equal step.
        """
        # MOBILE Diana load.
        mobile_load = True
        # Each simulation must consist of only one load.
        for fem_params in self.fem_params:
            if len(fem_params.loads) != 1:
                mobile_load = False
        # Each simulation must be equal (apart from x position).
        step = None
        if mobile_load:
            for fp1, fp2 in zip(
                    self.fem_params[:-1], self.fem_params[1:]):
                if fp1.loads[0].weight != fp2.loads[0].weight:
                    mobile_load = False
                if fp1.loads[0].lane != fp2.loads[0].lane:
                    mobile_load = False
                if fp1.response_types != fp2.response_types:
                    mobile_load = False
                if fp2.loads[0].x_pos < fp1.loads[0].x_pos:
                    mobile_load = False
                # Loads must be increasing with equal step.
                new_step = fp2.loads[0].x_pos - fp1.loads[0].x_pos
                if step is not None and step != new_step:
                    mobile_load = False
                step = new_step
        return mobile_load


if __name__ == "__main__":
    fem_params = FEMParams(loads=[Load(0.5, 5e3), Load(0.2, 5e1)])
    print(fem_params)
