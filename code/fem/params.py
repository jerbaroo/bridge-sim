"""Parameters for FEM simulations."""
from typing import List

from model import *


class FEMParams:
    """Parameters for a FEM simulation.

    Either non-moving loads or a displacement control.

    Args:
        loads: [Load], a list of Load to apply to the bridge.
        displacement_ctrl: DisplacementCtrl, apply a load until the
            displacement is reached. If given then "loads" are ignored.
        response_types: [ResponseType], response types to record.

    Attrs:
        built_model_file: str, path of the model file built for simulation.

    """
    def __init__(self, loads: [Load]=[],
                 displacement_ctrl: DisplacementCtrl=None,
                 response_types: [ResponseType]=[rt for rt in ResponseType]):
        self.loads=loads
        self.displacement_ctrl = displacement_ctrl
        assert not (len(loads) > 0 and displacement_ctrl is not None)
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

        Additionally each simulation must only have one load, and the loads
        must be increasing with equal step.

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
                if fp1.loads[0].total_kn() != fp2.loads[0].total_kn():
                    mobile_load = False
                if fp1.loads[0].lane != fp2.loads[0].lane:
                    mobile_load = False
                if fp1.response_types != fp2.response_types:
                    mobile_load = False
                if fp2.loads[0].x_frac < fp1.loads[0].x_frac:
                    mobile_load = False
                # Loads must be increasing with equal step.
                new_step = fp2.loads[0].x_frac - fp1.loads[0].x_frac
                if step is not None and step != new_step:
                    mobile_load = False
                step = new_step
        return mobile_load
