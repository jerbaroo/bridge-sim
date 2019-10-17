"""Parameters for FEM simulations."""
from typing import List, Optional

from model.load import DisplacementCtrl, PointLoad
from model.response import ResponseType


class FEMParams:
    """Parameters for one FEM simulation.

    Point loads EOR displacement control, and response types to record.

    Args:
        ploads: List[PointLoad], a list of point loads to apply to the bridge.
        displacement_ctrl: DisplacementCtrl, apply a load until the given
            displacement in meters is reached.
        response_types: [ResponseType], response types to record.

    """
    def __init__(
            self, ploads: List[PointLoad], response_types: List[ResponseType],
            displacement_ctrl: Optional[DisplacementCtrl] = None):
        if len(ploads) == 0: assert displacement_ctrl is not None
        else: assert displacement_ctrl is None
        self.ploads = ploads
        self.displacement_ctrl = displacement_ctrl
        self.response_types = response_types

    def load_str(self):
        """String representing the loading parameters."""
        if self.displacement_ctrl is not None:
            return (f"disp-ctrl-{self.displacement_ctrl.displacement}"
                + f"-{self.displacement_ctrl.pier}")
        lstr = ",".join(str(l) for l in self.ploads)
        return f"[{lstr}]"


class ExptParams:
    """Parameters for multiple simulations."""
    def __init__(self, fem_params: List[FEMParams]):
        self.fem_params = fem_params

    def is_mobile_load(self):
        """"Whether each simulation is equal apart from load position.

        This could be useful for specifying a MOBILE Load in Diana:
        https://dianafea.com/manuals/d102/Analys/node39.html#89111

        """
        raise Exception("This is untested and incomplete.")
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
