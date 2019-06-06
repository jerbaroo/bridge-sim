"""
Generate an influence line of bridge 705.
"""
import matplotlib.pyplot as plt
import numpy as np

from build_opensees_model import build_opensees_model
from model import Fix, Load, Patch
from run_opensees_model import run_opensees_model

# Filepath of an influence line matrix based on parameters.
matrix_filepath = (lambda filepath, num_loads, num_sensors, load, time:
    f"{filepath}-nl-{num_loads}-ns-{num_sensors}-l-{load}-t-{time}.npy")


def gen_matrix(filepath, num_loads, num_sensors, load, time):
    """Generate a matrix of sensor response for each sensor/load position."""
    matrix = np.empty(shape=(num_loads, num_sensors))
    for i, load_position in enumerate(np.linspace(0, 1, num_loads)):
        build_opensees_model(
            num_elems=num_sensors,
            fix=[Fix(x_pos, y=True) for x_pos in np.linspace(0, 1, 8)],
            load=[Load(load_position, load)]
        )
        x, y, stress, strain = run_opensees_model()
        matrix[i] = stress[time]
    np.save(
        matrix_filepath(filepath, num_loads, num_sensors, load, time),
        matrix)
    plt.imshow(matrix)
    plt.ylabel("load position")
    plt.xlabel("sensor position")
    plt.show()
    return matrix


if __name__ == "__main__":
    filepath = "generated/il/influence-line-matrix"
    num_loads = 10
    num_sensors = 100
    load = -5e4
    time = 1
    matrix = gen_matrix(filepath, num_loads, num_sensors, load, time)
    matrix = np.load(
        matrix_filepath(filepath, num_loads, num_sensors, load, time))
    for i in range(len(matrix)):
        plt.plot(matrix[i])
        plt.show()
