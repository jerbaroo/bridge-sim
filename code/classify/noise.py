import numpy as np


def add_displa_noise(a, std: float = 0.0012 / 1000, mean: float = 0):
    """Add noise to a time series of displacements in meters.

    Default standard deviation of noise is 0.0012mm with a mean of 0.

    """
    return np.array(a) + np.random.normal(mean, std, len(a))
