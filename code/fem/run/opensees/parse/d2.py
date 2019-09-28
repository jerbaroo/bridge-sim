"""Parse responses from a 2D OpenSees simulation."""
from __future__ import annotations
import itertools
from collections import defaultdict
from timeit import default_timer as timer

from config import Config
from fem.params import ExptParams
from fem.run import Parsed
from fem.run.opensees.parse.common import opensees_to_numpy, opensees_to_stress_strain
from model.response import ResponseType
from util import print_d, print_i

# Print debug information for this file.
D: bool = True


def parse_responses_2d(
        c: Config, expt_params: ExptParams, os_runner: "OSRunner") -> Parsed:
    """Parse responses from a 2D OpenSees simulation."""
    results = defaultdict(dict)

    # Iterate through each simulation and collect results.
    for sim_ind, fem_params in enumerate(expt_params.fem_params):

        # Is a ResponseType to be collected?
        parse_type = lambda rt: rt in fem_params.response_types

        # Collect x translation responses if required.
        if parse_type(ResponseType.XTranslation):
            start = timer()
            x = opensees_to_numpy(os_runner.x_translation_path(fem_params))
            x *= -1
            print_i("OpenSees: Parsed XTranslation responses in"
                    + f" {timer() - start:.2f}s")

        # Collect y translation responses if required.
        if parse_type(ResponseType.YTranslation):
            start = timer()
            y = opensees_to_numpy(os_runner.y_translation_path(fem_params))
            y *= -1
            print_i("OpenSees: Parsed YTranslation responses in "
                    + f"{timer() - start:.2f}s")

        stress = []
        strain = []
        # Collect stress and/or strain responses if required.
        if parse_type(ResponseType.Stress) or parse_type(ResponseType.Strain):
            start = timer()
            for section in c.bridge.sections:
                # Convert each fiber command to a tuple of
                # (path, fiber_cmd_id, Point), where path is the path where the
                # responses can be found, fiber_cmd_id is the ID of the fiber,
                # and Point is center of the fiber.

                # Start with the Patch fibers.
                patch_paths_and_more = [
                    zip(os_runner.patch_paths(fem_params, patch),
                        itertools.repeat(patch.fiber_cmd_id),
                        patch.points())
                    for patch in section.patches]
                patch_paths_and_more = list(
                    itertools.chain.from_iterable(patch_paths_and_more))

                # Then the layer fibers.
                layer_paths_and_more = [
                    zip(os_runner.layer_paths(fem_params, layer),
                        itertools.repeat(layer.fiber_cmd_id),
                        layer.points())
                    for layer in section.layers]
                layer_paths_and_more = list(
                    itertools.chain.from_iterable(layer_paths_and_more))

                # For each fiber: append the stress/strain responses.
                for path, fiber_cmd_id, point in (
                        patch_paths_and_more + layer_paths_and_more):
                    parsed_stress, parsed_strain = opensees_to_stress_strain(
                        path=path,
                        parse_stress=parse_type(ResponseType.Stress),
                        parse_strain=parse_type(ResponseType.Strain))
                    # In both cases, stress and strain, we map the parsed
                    # tuples from opensees_to_stress_strain to a tuple that is
                    # specific to the 2D case.
                    print_d(D, f"parse_d2: path = {path}")
                    if parse_type(ResponseType.Stress):
                        stress += list(map(
                            lambda tup: (
                                tup[0], tup[2], section.id, tup[1],
                                fiber_cmd_id, point),
                            parsed_stress))
                    if parse_type(ResponseType.Strain):
                        strain += list(map(
                            lambda tup: (
                                tup[0], tup[2], section.id, tup[1],
                                fiber_cmd_id, point),
                            parsed_strain))
                        print_d(D, f"len appended strain = {len(strain[-1])}")
            print_i("OpenSees: Parsed stress/strain responses in "
                    + f" {timer() - start:.2f}s")

        if parse_type(ResponseType.XTranslation):
            results[sim_ind][ResponseType.XTranslation] = x
        if parse_type(ResponseType.YTranslation):
            results[sim_ind][ResponseType.YTranslation] = y
        if parse_type(ResponseType.Stress):
            results[sim_ind][ResponseType.Stress] = stress
        if parse_type(ResponseType.Strain):
            results[sim_ind][ResponseType.Strain] = strain
    return results
