import itertools
import subprocess
from timeit import default_timer as timer
from typing import Dict, List, TypeVar

import matplotlib.pyplot as plt
import numpy as np

from config import Config
from fem.responses import Response
from fem.run.opensees.build import os_layer_paths, os_patch_path
from model import *
from util import *


def run_model(c: Config):
    """Run an OpenSees simulation."""
    subprocess.run([c.os_exe_path, c.os_built_model_path])


_sim_time = None
P = TypeVar("P")


def parse_responses(c: Config, response_types: [ResponseType]) -> Dict[ResponseType, P]:
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


def convert_responses(c: Config, parsed: Dict[ResponseType, P], _
                     ) -> Dict[ResponseType, List[Response]]:
    """Convert parsed responses to Responses."""

    def translation_to_responses(trans):
        """Convert data indexed as [time][node] to a list of Response."""
        node_ids = c.os_node_ids()
        return [
            Response(trans[time][i], x=i * c.os_node_step, y=0, z=0,
                     time=time, node_id=node_ids[i])
            for time in range(len(trans))
            for i in range(len(trans[time]))]

    if ResponseType.XTranslation in parsed:
        x = translation_to_responses(parsed[ResponseType.XTranslation])
    if ResponseType.YTranslation in parsed:
        y = translation_to_responses(parsed[ResponseType.YTranslation])

    ##### Stress and strain for each section's fiber. #####

    def stress_to_responses(stress, section_id, fiber_cmd_id, y, z):
        """Stress or strain data to a list of Response."""
        # TODO: Check assertion makes sense.
        assert len(stress) == _sim_time
        elem_ids = c.os_elem_ids()
        return [
            Response(
                stress[time][i], x=i * c.os_node_step + (c.os_node_step / 2),
                y=y, z=z, time=time, elem_id=elem_ids[i],
                section_id=section_id, fiber_cmd_id=fiber_cmd_id)
            for time in range(len(stress))
            for i in range(len(stress[time]))]

    if ResponseType.Stress in parsed:
        stress = stress_to_responses(
            parsed[ResponseType.Stress], section.id, fiber_cmd_id, point.y,
            point.z)
    if ResponseType.Strain in parsed:
        strain = stress_to_responses(
            parsed[ResponseType.Strain], section.id, fiber_cmd_id, point.y,
            point.z)

    return {
        ResponseType.XTranslation:
            x if ResponseType.XTranslation in parsed else None,
        ResponseType.YTranslation:
            y if ResponseType.YTranslation in parsed else None,
        ResponseType.Stress:
            stress if ResponseType.Stress in parsed else None,
        ResponseType.Strain:
            strain if ResponseType.Strain in parsed else None
    }


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
