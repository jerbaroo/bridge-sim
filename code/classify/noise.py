from timeit import default_timer as timer

import numpy as np

from util import print_i


def add_displa_noise(a, std: float = 0.0012 / 1000, mean: float = 0):
    """Add noise to a time series of displacements in meters.

    Default standard deviation of noise is 0.0012mm with a mean of 0.

    """
    start = timer()
    a = np.array(a, copy=True)
    noise = np.random.normal(mean, std, a.shape)
    print_i(f"Added {a.shape} of noise in {timer() - start:.3f} s")
    result = np.add(a, noise)
    print_i(f"Shapes = {a.shape} {noise.shape} {result.shape}")
    return result
