"""Run FE simulations with OpenSees."""
import os

import distutils.spawn as spawn
from typing import Callable, List, Optional

from bridge_sim.model import ResponseType, Config, Bridge
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run import FEMRunner
from bridge_sim.sim.run.opensees.build import build_model
from bridge_sim.sim.run.opensees.convert import convert_responses
from bridge_sim.sim.run.opensees.parse import parse_responses
from bridge_sim.sim.run.opensees.run import run_model
from bridge_sim.util import print_i, print_w


def opensees_supported_response_types(bridge: Bridge) -> List[ResponseType]:
    """The response types supported by OpenSees."""
    return [
        ResponseType.XTrans,
        ResponseType.YTrans,
        ResponseType.ZTrans,
        ResponseType.StrainXXB,
        ResponseType.StrainXXT,
        ResponseType.StrainZZB,
    ]


class OSRunner(FEMRunner):
    def __init__(self, c: Config, exe_path: str):
        super().__init__(
            c=c,
            name="OpenSees",
            exe_path=exe_path,
            supported_response_types=opensees_supported_response_types,
            build=build_model,
            run=run_model,
            parse=parse_responses,
            convert=convert_responses,
        )

        def opensees_out_path(*args, **kwargs):
            return self.sim_out_path(*args, **kwargs).replace("\\", "/")

        self.opensees_out_path = opensees_out_path

    # NOTE: All of the path functions below are only used within the OpenSees
    # FEMRunner, used to save results from OpenSees simulations.

    def translation_path(self, fem_params: SimParams, axis: str):
        return self.opensees_out_path(
            sim_params=fem_params, ext="out", append=f"node-{axis}"
        )

    def x_translation_path(self, fem_params: SimParams):
        return self.translation_path(fem_params=fem_params, axis="x")

    def y_translation_path(self, fem_params: SimParams):
        return self.translation_path(fem_params=fem_params, axis="y")

    def z_translation_path(self, fem_params: SimParams):
        return self.translation_path(fem_params=fem_params, axis="z")

    def element_path(self, fem_params: SimParams):
        return self.opensees_out_path(sim_params=fem_params, ext="out", append="-elems")

    def stress_path(self, sim_params: SimParams):
        return self.opensees_out_path(
            sim_params=sim_params, ext="out", append="-stress"
        )

    def strain_path(self, sim_params: SimParams, point: int):
        return self.opensees_out_path(
            sim_params=sim_params, ext="out", append=f"-strain-{point}"
        )

    def forces_path(self, sim_params: SimParams):
        return self.opensees_out_path(
            sim_params=sim_params, ext="out", append=f"-forces"
        )


def os_runner(exe_path: Optional[str] = None) -> Callable[["Config"], OSRunner]:
    # Try using OpenSees on PATH.
    if exe_path is None:
        exe_path = spawn.find_executable("OpenSees")
        if exe_path is not None:
            print_i(f"Found Opensees at: {exe_path}")
    # Else try a few hardcoded possibilities e.g. for Singularity.
    try_exes = ["/opensees/bin/OpenSees"]
    if exe_path is None:
        for path in try_exes:
            if os.path.exists(path):
                print_i(f"Found Opensees at: {path}")
                exe_path = path
                break
    if exe_path is None:
        print_w("Could't find OpenSees executable")
    return lambda c: OSRunner(c=c, exe_path=exe_path)
