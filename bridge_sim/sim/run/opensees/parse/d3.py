"""Parse responses from an OpenSees simulation."""

from collections import defaultdict
from timeit import default_timer as timer
from typing import List

import numpy as np

from bridge_sim.model import Config, ResponseType, RT
from bridge_sim.sim.model import SimParams
from bridge_sim.sim.run import Parsed
from bridge_sim.sim.run.opensees.parse.common import opensees_to_numpy
from bridge_sim.util import print_i


def parse_translation_responses_3d(
    results_dict,
    fem_params: SimParams,
    sim_ind: int,
    responses_path: str,
    response_type: ResponseType,
):
    """Parse translation fem from a 3D OpenSees simulation."""
    print(f"response_type = {response_type}")
    if response_type not in [RT.XTrans, RT.YTrans, RT.ZTrans]:
        raise ValueError("Must be translation response type")
    start = timer()
    translation_responses = opensees_to_numpy(responses_path)
    translation_responses *= -1
    print_i(
        f"OpenSees: Parsed {response_type.name()} responses in"
        + f" {timer() - start:.2f}s"
    )
    results_dict[sim_ind][response_type] = translation_responses


def parse_stress_strain_responses_3d(
    results_dict, sim_params: SimParams, sim_ind: int, response_paths: List[str],
):
    """Parse stress or strain fem from a 3D OpenSees simulation."""
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
    lines = np.array(lines)
    print(lines.shape)
    # Save all strain responses under this one key.
    results_dict[sim_ind][ResponseType.StrainXXB] = lines


def parse_responses_3d(
    c: Config, expt_params: List[SimParams], os_runner: "OSRunner"
) -> Parsed:
    """Parse fem from a 3D OpenSees simulation."""
    # A dictionary of simulation index to ResponseType to parsed fem.
    results_dict = defaultdict(dict)
    for sim_ind, fem_params in enumerate(expt_params):
        print(f"Parsing, sim_ind = {sim_ind}")
        # Parse x translation fem if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict,
            fem_params=fem_params,
            sim_ind=sim_ind,
            responses_path=os_runner.x_translation_path(c, fem_params),
            response_type=ResponseType.XTrans,
        )
        # Parse y translation fem if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict,
            fem_params=fem_params,
            sim_ind=sim_ind,
            responses_path=os_runner.y_translation_path(c, fem_params),
            response_type=ResponseType.YTrans,
        )
        # Parse z translation fem if necessary.
        parse_translation_responses_3d(
            results_dict=results_dict,
            fem_params=fem_params,
            sim_ind=sim_ind,
            responses_path=os_runner.z_translation_path(c, fem_params),
            response_type=ResponseType.ZTrans,
        )
        # Parse strain fem if necessary.
        parse_stress_strain_responses_3d(
            results_dict=results_dict,
            sim_params=fem_params,
            sim_ind=sim_ind,
            response_paths=[
                os_runner.strain_path(c, fem_params, i) for i in [1, 2, 3, 4]
            ],
        )
    return results_dict
