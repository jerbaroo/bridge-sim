"""
Generate an influence line of bridge 705.
"""
import matplotlib.pyplot as plt
import numpy as np

from build_opensees_model import build_opensees_model
from model import Fix, Load, Patch
from models import bridge_705
from plot import plot_bridge
from run_opensees_model import run_opensees_model

# The filepath of an influence line matrix.
il_filepath = (lambda filepath, num_loads, num_sensors, load, time:
    f"{filepath}-nl-{num_loads}-ns-{num_sensors}-l-{load}-t-{time}.npy")

# Load an influence line matrix from a file.
load_il = (lambda filepath, num_loads, num_sensors, load, time:
    np.load(il_filepath(filepath, num_loads, num_sensors, unit_load, time)))


def gen_matrix(model, filepath, num_loads, num_sensors, unit_load, time):
    """Generate a matrix of stress response for each sensor/load position.

    Args:
        model: specification of a model of a bridge.
        filepath: path of where to save the matrix.
        num_loads: amount of points at which to place the load.
        num_sensors: amount of points at which to record the response.
        unit_load: the value of load which is placed on the bridge.
        time: int, time index at which to read the response after loading.
    """
    matrix = np.empty(shape=(num_loads, num_sensors))
    for i, load_position in enumerate(np.linspace(0, 1, num_loads)):
        build_opensees_model(
            num_elems=num_sensors,
            load=[Load(load_position, unit_load)]
        )
        x, y, stress, strain = run_opensees_model()
        matrix[i] = stress[time]
    np.save(
        il_filepath(filepath, num_loads, num_sensors, load, time),
        matrix)
    plt.imshow(matrix)
    plt.ylabel("load position")
    plt.xlabel("sensor position")
    plt.show()


def plot_ils(matrix, at=None):
    """Plot each influence line from the matrix.

    Args:
        matrix: influence line matrix indexed by load then sensor position.
        at: plot the influence line at given index, else all influence lines.
    """
    il_indices = range(len(matrix)) if at is None else [at]
    for i in il_indices:
        plt.plot(matrix[i])
        plot_bridge()
        plt.show()


def il_response(matrix, response_pos, load_pos, load, unit_load):
    """The response of a load at a position from an influence line matrix.

    Args:
        matrix: influence line matrix indexed by load then sensor position.
        response_pos: position of the returned response, in [0 1].
        load_pos: position of the load, in [0 1].
        load: the value of the load.
        unit_load: the unit load used to generate the influence line.
    """
    # Convert load_pos to a matrix index.
    load_ind = int(np.interp(load_pos, [0, 1], [0, len(matrix) - 1]))
    # Convert response_pos to a matrix index.
    response_ind = int(np.interp(
        response_pos, [0, 1], [0, len(matrix[0]) - 1]))
    # Return the matrix value times the load factor.
    return matrix[load_ind, response_ind] * (load / unit_load)


if __name__ == "__main__":
    model = bridge_705
    filepath = "generated/il/influence-line-matrix"
    num_loads = 10
    num_sensors = 100
    unit_load = -5e4
    time = 1

    # gen_matrix(filepath, num_loads, num_sensors, unit_load, time)
    matrix = load_il(filepath, num_loads, num_sensors, unit_load, time)
    il_response(matrix, 0.5, 0.6, -5e6, unit_load)
    plot_ils(matrix, at=4)
