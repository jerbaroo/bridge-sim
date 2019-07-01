import itertools
import subprocess

import numpy as np

from build_opensees_model import os_layer_paths, os_patch_path
from config import Config
from model import *
from util import *


def run_model(c: Config):
    """Run an OpenSees model and return the recorded results."""
    print_i(f"Running OpenSees with {c.os_built_model_path}")
    subprocess.run([c.os_exe_path, c.os_built_model_path])
    x = openSeesToNumpy(c.os_x_path)
    y = openSeesToNumpy(c.os_y_path)
    stress = []
    strain = []
    for section in c.bridge.sections:
        patch_paths = [os_patch_path(c, patch) for patch in section.patches]
        layer_paths = [os_layer_paths(c, layer) for layer in section.layers]
        layer_paths = list(itertools.chain.from_iterable(layer_paths))
        for path in patch_paths + layer_paths:
            stress_strain = openSeesToNumpy(path)
            num_t = len(stress_strain)
            num_measurements = len(stress_strain[0]) // 2
            stress.append([
                [stress_strain[t][i * 2] for i in range(num_measurements)]
                for t in range(num_t)
            ])
            strain.append([
                [stress_strain[t][i * 2 + 1] for i in range(num_measurements)]
                for t in range(num_t)
            ])
    print_i("Parsed OpenSees recorded data")
    return {
        Response.XTranslation: [x],
        Response.YTranslation: [y],
        Response.Stress: stress,
        Response.Strain: strain
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
