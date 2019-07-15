"""Parse responses from an OpenSees simulation."""
from collections import defaultdict
from timeit import default_timer as timer

from config import Config
from fem.params import ExptParams
from fem.run import FEMRunner, Parsed
from model import *
from util import *


def openSeesToNumpy(path):
    """Convert OpenSees output to 2d array."""
    with open(path) as f:
        x = f.read()
    # A string per unit time.
    x = list(filter(lambda y: len(y) > 0, x.split("\n")))
    # A list of string per unit time.
    for i in range(len(x)):
        x[i] = list(map(float, x[i].split()))
    return np.array(x)


def parse_responses(c: Config, expt_params: ExptParams, fem_runner: FEMRunner
                   ) -> Parsed:
    """Parse responses from an OpenSees simulation."""
    results = defaultdict(dict)

    for sim_ind, fem_params in enumerate(expt_params.fem_params):

        def parse_type(response_type: ResponseType):
            return response_type in fem_params.response_types

        if parse_type(ResponseType.XTranslation):
            start = timer()
            x = openSeesToNumpy(fem_runner.x_translation_path(fem_params))
            print_i("OpenSees: Parsed XTranslation responses in"
                    + f" {timer() - start:.2f}s")

        if parse_type(ResponseType.YTranslation):
            start = timer()
            y = openSeesToNumpy(fem_runner.y_translation_path(fem_params))
            print_i("OpenSees: Parsed YTranslation responses in "
                    + f"{timer() - start:.2f}s")

        stress = []
        strain = []
        if parse_type(ResponseType.Stress) or parse_type(ResponseType.Strain):
            start = timer()
            for section in c.bridge.sections:
                # Convert fiber commands to (path, fiber_cmd_id, Point).
                patch_paths_and_more = [
                    (fem_runner.patch_path(fem_params, patch),
                     patch.fiber_cmd_id,
                     patch.center())
                    for patch in section.patches]
                layer_paths_and_more = [
                    zip(fem_runner.layer_paths(fem_params, layer),
                        itertools.repeat(layer.fiber_cmd_id),
                        layer.points())
                    for layer in section.layers]
                layer_paths_and_more = list(
                    itertools.chain.from_iterable(layer_paths_and_more))

                # For each fiber: collect and append the Responses.
                for path, fiber_cmd_id, point in (
                        patch_paths_and_more + layer_paths_and_more):
                    stress_strain = openSeesToNumpy(path)
                    num_t = len(stress_strain)
                    num_measurements = len(stress_strain[0]) // 2
                    if parse_type(ResponseType.Stress):
                        stress += [
                            [stress_strain[t][i * 2]
                            for i in range(num_measurements)]
                            for t in range(num_t)]
                    if parse_type(ResponseType.Strain):
                        strain += [
                            [stress_strain[t][i * 2 + 1]
                            for i in range(num_measurements)]
                            for t in range(num_t)]
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
