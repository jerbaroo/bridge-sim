import itertools
from typing import Callable, Dict, Optional

import matplotlib
import numpy as np
import pandas as pd

from bridge_sim.model import Config, Point
from bridge_sim.sim.model import Responses
from bridge_sim.internal.plot import plt
from bridge_sim.util import print_i, scalar


def plot_mmm_strain_convergence(
    c: Config,
    pier: int,
    df: pd.DataFrame,
    all_strains: Dict[float, Responses],
    title: str,
    without: Optional[Callable[[Point], bool]] = None,
    append: Optional[str] = None,
):
    """Plot convergence of given fem as model size grows."""
    # A grid of points 1m apart, over which to calculate fem.
    grid = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, int(c.bridge.length)),
            np.linspace(c.bridge.z_min, c.bridge.z_max, int(c.bridge.width)),
        )
    ]
    # If requested, remove some values from the fem.
    if without is not None:
        grid = [point for point in grid if not without(point)]
        for msl, strains in all_strains.items():
            print(f"Removing points from strains with max_shell_len = {msl}")
            all_strains[msl] = strains.without(without)
    # Collect fem over all fem, and over the grid. Iterate by
    # decreasing max_shell_len.
    mins, maxes, means = [], [], []
    gmins, gmaxes, gmeans = [], [], []
    max_shell_lens = []
    for msl, strains in sorted(all_strains.items(), key=lambda kv: -kv[0]):
        max_shell_lens.append(msl)
        print_i(f"Gathering strains with max_shell_len = {msl}", end="\r")
        grid_strains = np.array([strains.at_deck(point, interp=True) for point in grid])
        gmins.append(scalar(np.min(grid_strains)))
        gmaxes.append(scalar(np.max(grid_strains)))
        gmeans.append(scalar(np.mean(grid_strains)))
        strains = np.array(list(strains.values()))
        mins.append(scalar(np.min(strains)))
        maxes.append(scalar(np.max(strains)))
        means.append(scalar(np.mean(strains)))
    print()
    # Normalize and plot the mins, maxes, and means.
    def normalize(ys):
        print(ys)
        return ys / np.mean(ys[-5:])

    mins, maxes, means = normalize(mins), normalize(maxes), normalize(means)
    gmins, gmaxes, gmeans = normalize(gmins), normalize(gmaxes), normalize(gmeans)
    deck_nodes = [df.at[msl, "deck-nodes"] for msl in max_shell_lens]
    pier_nodes = [df.at[msl, "pier-nodes"] for msl in max_shell_lens]
    num_nodes = np.array(deck_nodes) + np.array(pier_nodes)
    print(f"MSLs = {max_shell_lens}")
    print(f"num_nodes = {num_nodes}")
    # Plot all lines, for debugging.
    plt.landscape()
    plt.plot(num_nodes, mins, label="mins")
    plt.plot(num_nodes, maxes, label="maxes")
    plt.plot(num_nodes, means, label="means")
    plt.plot(num_nodes, gmins, label="gmins")
    plt.plot(num_nodes, gmaxes, label="gmaxes")
    plt.plot(num_nodes, gmeans, label="gmeans")
    plt.grid(axis="y")
    plt.xlabel("Nodes in FEM")
    plt.ylabel("Strain")
    plt.title(title)
    plt.tight_layout()
    plt.legend()
    plt.savefig(
        c.get_image_path("convergence-pier-strain", f"mmm-{append}-all.pdf", acc=False)
    )
    plt.close()
    # Only plot some lines, for the thesis.
    plt.landscape()
    plt.plot(num_nodes, gmins, label="Minimum")
    plt.plot(num_nodes, gmaxes, label="Maximum")
    plt.plot(num_nodes, gmeans, label="Mean")
    plt.grid(axis="y")
    plt.title(title)
    plt.xlabel("Nodes in FEM")
    plt.ylabel("Strain")
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        c.get_image_path("convergence-pier-strain", f"mmm-{append}.pdf", acc=False)
    )
    plt.close()


def plot_nesw_convergence(
    c: Config,
    df: pd.DataFrame,
    responses: Dict[float, Responses],
    point: Point,
    max_distance: float,
    from_: str,
):
    """Plot convergence of strain at different points around a load."""
    delta_distance = 0.05
    skip = 3
    # Create color mappable for distances.
    norm = matplotlib.colors.Normalize(vmin=0, vmax=max_distance)
    cmap = matplotlib.cm.get_cmap("jet")
    mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    color = lambda d: mappable.to_rgba(d)
    # For each compass point.
    compass_dir = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
    }
    plt.square()
    fig, axes = plt.subplots(nrows=2, ncols=2)
    for ax, compass, compass_name, in zip(
        axes.flat, ["N", "S", "E", "W"], ["North", "South", "East", "West"]
    ):
        # Collect data into fem.
        x_mul, z_mul = compass_dir[compass]
        for distance in np.arange(0, max_distance, step=delta_distance)[::skip]:
            dist_point = Point(
                x=point.x + (distance * x_mul),
                y=point.y,
                z=point.z + (distance * z_mul),
            )
            print(dist_point)
            if (
                dist_point.x < c.bridge.x_min
                or dist_point.x > c.bridge.x_max
                or dist_point.z < c.bridge.z_min
                or dist_point.z > c.bridge.z_max
            ):
                break
            line_responses = []
            for max_shell_len, sim_responses in responses.items():
                deck_nodes = float(df.at[max_shell_len, "deck-nodes"])
                pier_nodes = float(df.at[max_shell_len, "pier-nodes"])
                line_responses.append(
                    (
                        deck_nodes + pier_nodes,
                        # max_shell_len,
                        scalar(sim_responses.at_deck(dist_point, interp=True)),
                    )
                )
            line_responses = np.array(sorted(line_responses, key=lambda t: t[0])).T
            ax.plot(line_responses[0], line_responses[1], color=color(distance))
            if distance > max_distance:
                break
        ax.grid(axis="y")
        ax.set_title(
            f"Strain at increasing distance\nin direction {compass_name} from\n{from_}"
        )
        ax.set_xlabel("Nodes in FEM")
        ax.set_ylabel("Strain")
        # ax.set_xlim(ax.get_xlim()[1], ax.get_xlim()[0])
    plt.tight_layout()
    clb = plt.colorbar(mappable, ax=axes.ravel())
    clb.ax.set_title("Distance (m)")
