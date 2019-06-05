import subprocess

import numpy as np

from util import print_i

OPEN_SEES_PATH = 'c:/Program Files/OpenSees3.0.3-x64/OpenSees.exe'


def run_model(model="generated/built-model.tcl", open_sees_path=OPEN_SEES_PATH,
              node_x_out_file="generated/node-x.out",
              node_y_out_file="generated/node-y.out",
              node_stress_strain_out_file="generated/stress-strain.out"):
    """Run a model and return the recorded results."""
    print_i(f"Running OpenSees with {model}")
    subprocess.run([OPEN_SEES_PATH, model])
    x = openSeesToNumpy(node_x_out_file)
    y = openSeesToNumpy(node_y_out_file)
    stress_strain = openSeesToNumpy(node_stress_strain_out_file)
    print_i("Read OpenSees recorded data")
    return x, y, stress_strain


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
