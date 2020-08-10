"""Utilities for parsing fem from OpenSees simulations."""

from typing import List, NewType, Optional, Tuple

import numpy as np

from bridge_sim.util import print_d

# Print debug information for this file.
D: bool = False


def opensees_to_numpy(path: str):
    """Convert OpenSees output to 2d array."""
    with open(path) as f:
        x = f.read()
    # A string per unit time.
    x = list(filter(lambda y: len(y) > 0, x.split("\n")))
    # A list of string per unit time.
    for i in range(len(x)):
        x[i] = list(map(float, x[i].split()))
    return np.array(x)


# A tuple of collected stress or strain response.
SSTuple = NewType("SSTuple", Tuple[float, int, int])


def opensees_to_stress_strain(
    path: str, parse_stress: bool, parse_strain: bool
) -> Tuple[Optional[List[SSTuple]], Optional[List[SSTuple]]]:
    """Return a tuple of stress and/or strain fem.

    For both stress and strain the value is None if the respective argument
    parse_stress or parse_strain is None. Otherwise the value in each case is a
    list of tuples (V, T, I), where V is the value of the response, T is the
    time of the simulation and I is the index of the measurement at that time.

    NOTE: This return type should really be a matrix, but is like this for a
    legacy reason, feel free to change/update it.

    """
    print_d(D, f"path = {path}")
    stress_strain = opensees_to_numpy(path)
    num_time = len(stress_strain)
    num_measurements = len(stress_strain[0]) // 2
    stress, strain = None, None
    if parse_stress:
        stress = [
            (stress_strain[time][i * 2], time, i)
            for i in range(num_measurements)
            for time in range(num_time)
        ]
    if parse_strain:
        strain = [
            (stress_strain[time][i * 2 + 1], time, i)
            for i in range(num_measurements)
            for time in range(num_time)
        ]
    return stress, strain
