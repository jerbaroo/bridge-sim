"""Run FEM simulations with OpenSees."""
from typing import List

from config import Config
from fem.params import SimParams
from fem.run import FEMRunner
from fem.run.opensees.build import build_model
from fem.run.opensees.convert import convert_responses
from fem.run.opensees.parse import parse_responses
from fem.run.opensees.run import run_model
from model.bridge import Bridge, Dimensions, Layer, Patch
from model.response import ResponseType


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
            ResponseType.Stress,
        ]
    else:
        raise ValueError(f"{bridge.dimensions} not supported by OSRunner")


class OSRunner(FEMRunner):
    def __init__(self, c: Config):
        super().__init__(
            c=c,
            name="OpenSees",
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
        return self.opensees_out_path(
            sim_params=fem_params, ext="out", append="-elems"
        )
