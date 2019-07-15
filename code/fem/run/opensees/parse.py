"""Parse responses from an OpenSees simulation."""
from fem.run import Parsed
from config import Config
from model import *


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


def parse_responses(c: Config, response_types: [ResponseType]) -> Parsed:
    """Parse responses from an OpenSees simulation."""

    def parse_type(response_type: ResponseType):
        return response_type in response_types or response_types is None

    if parse_type(ResponseType.XTranslation):
        start = timer()
        x = openSeesToNumpy(c.os_x_path)
        print_i(f"OpenSees: Parsed XTranslation responses in {timer() - start:.2f}s")

    if parse_type(ResponseType.YTranslation):
        start = timer()
        y = openSeesToNumpy(c.os_y_path)
        print_i(f"OpenSees: Parsed YTranslation responses in {timer() - start:.2f}s")

    stress = []
    strain = []
    if parse_type(ResponseType.Stress) or parse_type(ResponseType.Strain):
        start = timer()
        for section in c.bridge.sections:
            # Convert fiber commands to (path, fiber_cmd_id, Point).
            patch_paths_and_more = [
                (os_patch_path(c, patch), patch.fiber_cmd_id, patch.center())
                for patch in section.patches]
            layer_paths_and_more = [
                zip(os_layer_paths(c, layer),
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
                        [stress_strain[t][i * 2] for i in range(num_measurements)]
                        for t in range(num_t)]
                if parse_type(ResponseType.Strain):
                    strain += [
                        [stress_strain[t][i * 2 + 1] for i in range(num_measurements)]
                        for t in range(num_t)]
        end = timer()
        print_i(f"OpenSees: Parsed stress/strain responses in {end - start:.2f}s")

    results = dict()
    if parse_type(ResponseType.XTranslation):
        results[ResponseType.XTranslation] = x
    if parse_type(ResponseType.YTranslation):
        results[ResponseType.YTranslation] = y
    if parse_type(ResponseType.Stress):
        results[ResponseType.Stress] = stress
    if parse_type(ResponseType.Strain):
        results[ResponseType.Strain] = strain
    return results
