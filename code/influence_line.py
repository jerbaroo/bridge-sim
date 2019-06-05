"""
Generate an influence line of bridge 705.
"""
import matplotlib.pyplot as plt
import numpy as np

from build_opensees_model import build_opensees_model
from model import Fix, Load, Patch
from run_opensees_model import run_opensees_model


def gen_matrix(matrix_path="generated/influence-line-matrix.txt", num_loads=10,
               num_sensors=100, load=-5e4, time=1):
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
    np.save(matrix_path, matrix)
    plt.imshow(matrix)
    plt.show()


if __name__ == "__main__":
    gen_matrix()
