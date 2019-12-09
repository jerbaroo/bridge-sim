"""Parse responses from a 3D OpenSees simulation."""
from collections import defaultdict
from timeit import default_timer as timer
from typing import List

import numpy as np

from config import Config
from fem.params import ExptParams, SimParams
from fem.run import Parsed
from fem.run.opensees.parse.common import opensees_to_numpy
from model.response import ResponseType
from util import print_i


def parse_translation_responses_3d(
    results_dict,
    fem_params: SimParams,
    sim_ind: int,
    responses_path: str,
    response_type: ResponseType,
):
    """Parse translation responses from a 3D OpenSees simulation."""
    print(f"response_type = {response_type}")
    print(f"fem_params.response_types = {fem_params.response_types}")
    if response_type in fem_params.response_types:
        start = timer()
        translation_responses = opensees_to_numpy(responses_path)
        translation_responses *= -1
        print_i(
            f"OpenSees: Parsed {response_type.name()} responses in"
            + f" {timer() - start:.2f}s"
        )
        results_dict[sim_ind][response_type] = translation_responses


def parse_stress_strain_responses_3d(
    results_dict,
    sim_params: SimParams,
    sim_ind: int,
    response_paths: List[str],
):
    """Parse stress or strain responses from a 3D OpenSees simulation."""
    if any(rt in sim_params.response_types for rt in [ResponseType.Strain, ResponseType.Stress]):
        lines = []
        for response_path in response_paths:
            with open(response_path) as f:
                new_lines = f.read()
                if new_lines.endswith("\n"):
                    new_lines = new_lines[:-1]
                new_lines = list(map(float, new_lines.split()))
                sections = len(new_lines) / 8
                if int(len(new_lines)) / 8 != sections:
                    raise ValueError("Unexpected length of parsed strains")
                per_element_lines = np.array_split(new_lines, sections)
                lines.append(per_element_lines)
        results_dict[sim_ind][ResponseType.Strain] = lines


def parse_responses_3d(
    c: Config, expt_params: ExptParams, os_runner: "OSRunner"
) -> Parsed:
    """Parse responses from a 3D OpenSees simulation."""
    # A dictionary of simulation index to ResponseType to parsed responses.
    results_dict = defaultdict(dict)
    for sim_ind, fem_params in enumerate(expt_params.sim_params):
        print(f"Parsing, sim_ind = {sim_ind}")
        # Parse x translation responses if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict,
            fem_params=fem_params,
            sim_ind=sim_ind,
            responses_path=os_runner.x_translation_path(fem_params),
            response_type=ResponseType.XTranslation,
        )
        # Parse y translation responses if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict,
            fem_params=fem_params,
            sim_ind=sim_ind,
            responses_path=os_runner.y_translation_path(fem_params),
            response_type=ResponseType.YTranslation,
        )
        # Parse z translation responses if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict,
            fem_params=fem_params,
            sim_ind=sim_ind,
            responses_path=os_runner.z_translation_path(fem_params),
            response_type=ResponseType.ZTranslation,
        )
        # Parse strain responses if necessary.
        parse_stress_strain_responses_3d(
            results_dict=results_dict,
            sim_params=fem_params,
            sim_ind=sim_ind,
            response_paths=[
                os_runner.strain_path(fem_params, i) for i in [1, 2, 3, 4]]
        )
    return results_dict
