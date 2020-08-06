"""Run FE simulations with OpenSees."""

import os

import distutils.spawn as spawn
from typing import Callable, List, Optional, Union

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
    def __init__(self, exe_path: str):
        """Construct a FEMRunner that uses OpenSees to run simulations.

        Args:
            exe_path: command to run OpenSees on the command line.

        """
        super().__init__(
            name="OpenSees",
            supported_response_types=opensees_supported_response_types,
            build=build_model,
            run=run_model,
            parse=parse_responses,
            convert=convert_responses,
        )
        self.exe_path = exe_path

        def opensees_out_path(*args, **kwargs):
            return self.sim_out_path(*args, **kwargs).replace("\\", "/")

        self.opensees_out_path = opensees_out_path

    # NOTE: All of the path functions below are only used within the OpenSees
    # FEMRunner, used to save results from OpenSees simulations.

    def translation_path(self, config: Config, fem_params: SimParams, axis: str):
        return self.opensees_out_path(
            config=config, sim_params=fem_params, ext="out", append=f"node-{axis}"
        )

    def x_translation_path(self, config: Config, fem_params: SimParams):
        return self.translation_path(config=config, fem_params=fem_params, axis="x")

    def y_translation_path(self, config: Config, fem_params: SimParams):
        return self.translation_path(config=config, fem_params=fem_params, axis="y")

    def z_translation_path(self, config: Config, fem_params: SimParams):
        return self.translation_path(config=config, fem_params=fem_params, axis="z")

    def element_path(self, config: Config, fem_params: SimParams):
        return self.opensees_out_path(
            config=config, sim_params=fem_params, ext="out", append="-elems"
        )

    def stress_path(self, config: Config, sim_params: SimParams):
        return self.opensees_out_path(
            config=config, sim_params=sim_params, ext="out", append="-stress"
        )

    def strain_path(self, config: Config, sim_params: SimParams, point: int):
        return self.opensees_out_path(
            config=config, sim_params=sim_params, ext="out", append=f"-strain-{point}"
        )

    def forces_path(self, config: Config, sim_params: SimParams):
        return self.opensees_out_path(
            config=config, sim_params=sim_params, ext="out", append=f"-forces"
        )


def os_runner(exe_path: Optional[str] = None) -> Union[OSRunner, None]:
    """Construct a FEMRunner that uses OpenSees to run simulations.

    Args:
        exe_path: optional command to run OpenSees on the command line. If not
        given then will look for OpenSees on the PATH, if still not found will
        look for OpenSees in a few hardcoded places.

    """
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
        return None
    return OSRunner(exe_path=exe_path)
