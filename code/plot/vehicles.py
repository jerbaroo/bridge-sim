"""Plot vehicle distributions."""
from math import ceil
from typing import Callable, List, Tuple, TypeVar

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

from config import Config
from model.bridge_705 import bridge_705_config
from util import *
from vehicles.sample import length_groups


# TODO: Store axle number directly in data.
def axle_array_and_count(axle_array_str: str) -> int:
    """Return an axle array and count of non zero values from a string."""
    axle_array_str = axle_array_str.replace(
        "'", "").replace("[", "").replace("]", "")
    axle_array = list(map(float, axle_array_str.split(",")))
    count_non_zero = len(list(filter(lambda x: x != 0, axle_array)))
    return axle_array, count_non_zero


def plot_density(c: Config, save: str=None, show: bool=False):
    """Plot the vehicle density."""
    plt.bar(
        range(len(c.vehicle_density)),
        list(map(lambda x: x[1] / 100, c.vehicle_density)),
        tick_label=[f"{x[0]:.1f}" for x in c.vehicle_density])
    plt.title(f"Vehicle density on {c.bridge.name}")
    plt.xlabel(f"Maximum vehicle length (m)")
    plt.ylabel(f"Density")
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


pdDataFrameGroupBy = TypeVar("pd.DataFrameGroupBy")


def group_scatter_plots(
        c: Config, groups: List[Tuple[float, pdDataFrameGroupBy]],
        # Functions that return the x and y data.
        group_x: Callable[[pd.DataFrame], List[float]],
        group_y: Callable[[pd.DataFrame], List[float]],
        group_x_label: str=None, group_y_label: str=None,
        cols: int=2, save: str=None, title: str=None):
    """Scatter plots for each group of data and for the full data."""
    print(type(groups))
    # Setup groups, rows and columns.
    num_groups = max(map(lambda x: x[0], groups)) + 1  # + 1 for the 0 index.
    rows = ceil(num_groups / cols)
    row, col = 0, 0

    # Add a wide header plot of all the data.
    plt.subplot2grid((rows, cols), (row, col), colspan=cols)
    plt.scatter(group_x(c.vehicle_data), group_y(c.vehicle_data), s=10)
    if title: plt.title(f"{title} (all data)")
    if group_x_label: plt.xlabel(group_x_label)
    if group_y_label: plt.ylabel(group_y_label)
    xlim, ylim = plt.xlim(), plt.ylim()

    # Add a subplot for each group.
    def add_1():
        nonlocal col
        nonlocal row
        col = 0 if col == cols - 1 else col + 1
        if col == 0: row += 1
    row += 1  # For the wide header plot.
    last_i = 0
    for (i, group) in [(int(i), g) for i, g in groups]:
        [add_1() for _ in range(last_i + 1, i)]  # For any empty groups.
        last_i = i
        plt.subplot2grid((rows, cols), (row, col))
        plt.scatter(group_x(group), group_y(group), s=10)
        if title: plt.title(f"{title} (group {i})")
        if group_x_label: plt.xlabel(group_x_label)
        if group_y_label: plt.ylabel(group_y_label)
        plt.xlim(xlim); plt.ylim(ylim)
        add_1()
    plt.gcf().set_size_inches(16, 10)
    plt.tight_layout()
    if save:
        plt.savefig(save)
        plt.close()


def plot_length_vs_axles(c: Config, cols: int=2, save: str=None):
    """Plot length vs number of axles for each length group."""
    group_length = lambda group: group["length"] / 100
    group_num_axles = (lambda group:
        group["weight_per_axle"].apply(lambda s: axle_array_and_count(s)[1]))
    group_scatter_plots(
        c=c, groups=length_groups(c),
        group_x=group_num_axles, group_y=group_length,
        group_x_label="number of axles", group_y_label="length (m)",
        cols=cols, save=save, title="Vehicle length against number of axles"
    )


def plot_length_vs_weight(c: Config, cols: int=2, save: str=None):
    """Plot length vs number of axles for each length group."""
    group_length = lambda group: group["length"] / 100
    group_weight = lambda group: group["total_weight"]
    group_scatter_plots(
        c=c, groups=length_groups(c), 
        group_x=group_weight, group_y=group_length,
        group_x_label="weight (kN)", group_y_label="length (m)",
        cols=cols, save=save, title="Vehicle length against weight"
    )


def plot_weight_vs_axles(c: Config, cols: int=2, save: str=None):
    """Plot length vs number of axles for each length group."""
    group_weight = lambda group: group["total_weight"]
    group_num_axles = (lambda group:
        group["weight_per_axle"].apply(lambda s: axle_array_and_count(s)[1]))
    group_scatter_plots(
        c=c, groups=length_groups(c),
        group_x=group_weight, group_y=group_num_axles,
        group_x_label="weight (kN)", group_y_label="number of axles",
        cols=cols, save=save, title="Vehicle number of axles against weight"
    )
