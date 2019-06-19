import subprocess

import numpy as np

from config import Config
from model import *
from util import print_i


def run_opensees_model(c: Config):
    """Run an OpenSees model and return the recorded results."""
    print_i(f"Running OpenSees with {c.os_built_model_path}")
    subprocess.run([c.os_exe_path, c.os_built_model_path])
    x = openSeesToNumpy(c.os_x_path)
    y = openSeesToNumpy(c.os_y_path)
    stress = []
    strain = []
    for patch in c.bridge.sections[0].patches:
        stress_strain = openSeesToNumpy(c.os_stress_strain_path(patch))
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
