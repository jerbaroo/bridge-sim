import itertools
import subprocess
import sys

import numpy as np

from config import Config
from fem.responses import _Response
from fem.run.opensees.build import os_layer_paths, os_patch_path
from model import *
from util import *


def run_model(c: Config):
    """Run an OpenSees model and return the recorded responses."""
    print_i(f"Running OpenSees with {c.os_built_model_path}")
    subprocess.run([c.os_exe_path, c.os_built_model_path])

    ##### X and Y translation for each node. #####

    def translation_to_responses(trans):
        """Convert data indexed as [time][node] to a list of Response."""
        node_ids = c.os_node_ids()
        return [
            _Response(trans[time][i], x=i * c.os_node_step, y=0, z=0,
                      time=time, node_id=node_ids[i])
            for time in range(len(trans))
            for i in range(len(trans[time]))
        ]

    x = openSeesToNumpy(c.os_x_path)
    y = openSeesToNumpy(c.os_y_path)
    x = translation_to_responses(x)
    y = translation_to_responses(y)

    ##### Stress and strain for each section's fiber. #####

    def stress_to_responses(stress, section_id, fiber_cmd_id, y, z):
        """Stress or strain data to a list of Response."""
        elem_ids = c.os_elem_ids()
        return [
            _Response(
                stress[time][i], x=i * c.os_node_step + (c.os_node_step / 2),
                y=y, z=z, time=time, elem_id=elem_ids[i],
                section_id=section_id, fiber_cmd_id=fiber_cmd_id)
            for time in range(len(stress))
            for i in range(len(stress[time]))]
    
    stress = []
    strain = []
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
            more_stress = [
                [stress_strain[t][i * 2] for i in range(num_measurements)]
                for t in range(num_t)]
            more_strain = [
                [stress_strain[t][i * 2 + 1] for i in range(num_measurements)]
                for t in range(num_t)]
            more_stress = stress_to_responses(
                more_stress, section.id, fiber_cmd_id, point.y, point.z)
            more_strain = stress_to_responses(
                more_strain, section.id, fiber_cmd_id, point.y, point.z)

    print_i("Parsed OpenSees recorded data")

    responses_by_type = {
        Response.XTranslation: x,
        Response.YTranslation: y,
        Response.Stress: to_responses(stress),
        Response.Strain: to_responses(strain)
    }
    print_i("Formatted data into Responses")
    return responses_by_type


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
