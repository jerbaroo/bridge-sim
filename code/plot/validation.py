import itertools
from collections import defaultdict
from typing import Dict

import numpy as np
import pandas as pd

from config import Config
from fem.responses import Responses
from model.bridge import Point
from plot import plt
from util import print_i, scalar


def plot_mmm_strain_convergence(
        c: Config,
        pier: int,
        parameters: pd.DataFrame,
        all_strains: Dict[float, Responses]
):
    """Plot convergence of given responses as model size grows."""
    # A grid of points 1m apart, over which to calculate responses.
    grid = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)),
            np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)),
        )
    ]
    # Collect responses over all responses, and over the grid.
    mins, maxes, means = [], [], []
    gmins, gmaxes, gmeans = [], [], []
    num_sims = len(list(all_strains))
    for sim, strains in enumerate(all_strains.values()):
        print_i(f"Gathering strains from simulation {sim + 1} / {num_sims}", end="\r")
        grid_strains = np.array(
            [strains.at_deck(point, interp=True) for point in grid]
        )
        gmins.append(scalar(np.min(grid_strains)))
        gmaxes.append(scalar(np.max(grid_strains)))
        gmeans.append(scalar(np.mean(grid_strains)))
        strains = np.array(list(strains.values()))
        mins.append(scalar(np.min(strains)))
        maxes.append(scalar(np.max(strains)))
        means.append(scalar(np.mean(strains)))
    print()
    max_shell_lens = list(all_strains.keys())
    plt.plot(max_shell_lens, mins, label="mins")
    plt.plot(max_shell_lens, maxes, label="maxes")
    plt.plot(max_shell_lens, means, label="means")
    plt.plot(max_shell_lens, gmins, label="gmins")
    plt.plot(max_shell_lens, gmaxes, label="gmaxes")
    plt.plot(max_shell_lens, gmeans, label="gmeans")
    plt.legend()
    plt.landscape()
    plt.xlim(plt.xlim()[1], plt.xlim()[0])
    plt.tight_layout()
    plt.savefig(c.get_image_path("convergence-pier-strain", "mmm.pdf"))
    plt.close()


def plot_nesw_convergence(
        point: Point,
        max_distance: float,
        parameters: pd.DataFrame,
        all_responses: Dict[float, Responses],
):
    """Plot convergence in each compass direction from a point."""
    compass_responses = defaultdict(lambda: [])
    for compass_name, x_mul, z_mul in [
            ("N", 0, 1), ("E", -1, 0), ("S", 0, -1), ("W", 1, 0)]:
        print(f"compass name = {compass_name}")
        for delta in np.arange(0, max_distance, 0.05):
            print(f"delta = {delta}")
            compass_responses[compass_name].append([])
            for max_shell_len, responses in all_responses:
                compass_responses[compass_name][-1].append(
                    scalar(responses.at_deck(point, interp=True))
                )
