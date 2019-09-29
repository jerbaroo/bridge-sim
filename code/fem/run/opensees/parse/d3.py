"""Parse responses from a 3D OpenSees simulation."""
from collections import defaultdict
from timeit import default_timer as timer

from config import Config
from fem.params import ExptParams, FEMParams
from fem.run import Parsed
from fem.run.opensees.parse.common import opensees_to_numpy
from model.response import ResponseType
from util import print_i


def parse_translation_responses_3d(
        results_dict, fem_params: FEMParams, sim_ind: int, responses_path: str,
        response_type: ResponseType):
    """Parse translation responses from a 3D OpenSees simulation."""
    if response_type in fem_params.response_types:
        start = timer()
        translation_responses = opensees_to_numpy(responses_path)
        translation_responses *= -1
        print_i(f"OpenSees: Parsed {response_type.name()} responses in"
                + f" {timer() - start:.2f}s")
        results_dict[sim_ind][response_type] = translation_responses


def parse_stress_strain_responses_3d(
        results_dict, fem_params: FEMParams, sim_ind: int, responses_path: str,
        response_type: ResponseType):
    """Parse stress or strain responses from a 3D OpenSees simulation."""
    if response_type in fem_params.response_types:
        raise NotImplementedError(
            f"3D Cannot parse stress or strain: was {response_type}")


def parse_responses_3d(
        c: Config, expt_params: ExptParams, os_runner: "OSRunner") -> Parsed:
    """Parse responses from a 3D OpenSees simulation."""
    # A dictionary of simulation index to ResponseType to parsed responses.
    results_dict = defaultdict(dict)
    for sim_ind, fem_params in enumerate(expt_params.fem_params):
        # Parse x translation responses if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict, fem_params=fem_params, sim_ind=sim_ind,
            responses_path=os_runner.x_translation_path(fem_params),
            response_type=ResponseType.XTranslation)
        # Parse y translation responses if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict, fem_params=fem_params, sim_ind=sim_ind,
            responses_path=os_runner.y_translation_path(fem_params),
            response_type=ResponseType.YTranslation)
        # Parse z translation responses if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict, fem_params=fem_params, sim_ind=sim_ind,
            responses_path=os_runner.z_translation_path(fem_params),
            response_type=ResponseType.ZTranslation)
        # Parse strain responses if necessary.
        parse_stress_strain_responses_3d(
            results_dict=results_dict, fem_params=fem_params, sim_ind=sim_ind,
            responses_path=None, response_type=ResponseType.Strain)
        # Parse stress responses if necessary.
        parse_stress_strain_responses_3d(
            results_dict=results_dict, fem_params=fem_params, sim_ind=sim_ind,
            responses_path=None, response_type=ResponseType.Stress)
    return results_dict

