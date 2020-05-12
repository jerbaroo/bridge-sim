"""Run FEM simulations with OpenSees."""
import os
from typing import Callable, List, Optional

from lib.config import Config
from lib.fem.params import SimParams
from lib.fem.run import FEMRunner
from lib.fem.run.opensees.build import build_model
from lib.fem.run.opensees.convert import convert_responses
from lib.fem.run.opensees.parse import parse_responses
from lib.fem.run.opensees.run import run_model
from lib.model.bridge import Bridge, Dimensions, Layer, Patch
from lib.model.response import ResponseType
from util import print_i


def opensees_supported_response_types(bridge: Bridge) -> List[ResponseType]:
    """The response types supported by OpenSees for a given bridge."""
    if bridge.dimensions == Dimensions.D2:
        return [
            ResponseType.XTranslation,
            ResponseType.YTranslation,
            ResponseType.Strain,
            ResponseType.Stress,
        ]
    elif bridge.dimensions == Dimensions.D3:
        return [
            ResponseType.XTranslation,
            ResponseType.YTranslation,
            ResponseType.ZTranslation,
            ResponseType.Strain,
            ResponseType.StrainT,
            ResponseType.StrainZZB,
        ]
    else:
        raise ValueError(f"{bridge.dimensions} not supported by OSRunner")


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

    def patch_paths(self, fem_params: SimParams, patch: Patch):
        return [
            self.opensees_out_path(
                sim_params=fem_params,
                ext="out",
                append=f"-patch-{point.y:.5f}-{point.z:.5f}",
            )
            for point in patch.points()
        ]

    def layer_paths(self, fem_params: SimParams, layer: Layer):
        return [
            self.opensees_out_path(
                sim_params=fem_params,
                ext="out",
                append=f"-layer-{point.y:.5f}-{point.z:.5f}",
            )
            for point in layer.points()
        ]

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
    try_exes = [
        "/Applications/OpenSees3.0.3/OpenSees",
        "c:/Program Files/OpenSees/bin/OpenSees",
    ]
    if exe_path is None:
        for path in try_exes:
            if os.path.exists(path):
                print_i(f"Found Opensees at: {path}")
                exe_path = path
                break
    if exe_path is None:
        raise ValueError("Could't find OpenSees executable")
    return lambda c: OSRunner(c=c, exe_path=exe_path)
