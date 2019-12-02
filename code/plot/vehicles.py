"""Plot vehicle distributions."""
from math import ceil
from typing import Callable, List, Tuple, TypeVar

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from config import Config
from vehicles import axle_array_and_count, load_vehicle_data
from vehicles.sample import vehicle_pdf_groups
from util import print_d, print_i

# Print debug information for this file.
D: bool = False


def plot_db(c: Config):
    """Original A16 data, showing outliers, and downsampled final data."""
    # Print information on original data.
    a16 = load_vehicle_data("data/a16-data/original-a16.csv")
    print_i(f"Original A16 data has {len(a16)} rows")
    print_i(f"Minimum length = {np.min(a16['length']) / 100} m")
    print_i(f"Minimum weight = {np.min(a16['total_weight'])} kN")

    # Get and remove outliers.
    outliers = a16[(np.abs(stats.zscore(a16[["total_weight", "length"]])) >= 3)]
    num_outliers = len(a16) - len(outliers)
    print_i(
        f"Removed {len(outliers)} ({len(outliers) / len(a16):.4f}) outliers (by weight & length) from A16 data"
    )
    a16_no_outliers = a16.drop(outliers.index)

    # Sample to 10% of original size.
    sampled_a16 = a16_no_outliers.sample(n=int(len(a16) * 0.1))
    print_i(f"Sampled A16 data has {len(sampled_a16)} rows")
    sampled_a16.to_csv("data/a16-data/a16.csv")
    print_i("Wrote updated A16 data to disk")

    passengers = np.random.multivariate_normal(
        [700, 12.53], cov=np.eye(2), size=len(sampled_a16)
    ).T
    passengers = np.random.multivariate_normal(
        [700, 12.53], cov=np.eye(2), size=10
    ).T
    print(passengers)
    s = 1

    # Plot outliers.
    plt.subplot(1, 2, 1)
    plt.scatter(outliers["length"], outliers["total_weight"], s=s, color="red")
    plt.scatter(a16_no_outliers["length"], a16_no_outliers["total_weight"], s=s)

    plt.show()


def plot_density(c: Config, save: str = None):
    """Plot the vehicle density."""
    plt.bar(
        range(len(c.vehicle_pdf)),
        list(map(lambda x: x[1] / 100, c.vehicle_pdf)),
        tick_label=[f"{x[0]:.1f}" for x in c.vehicle_pdf],
    )
    plt.title(f"Vehicle density on {c.bridge.name}")
    plt.xlabel(f"Maximum vehicle length (m)")
    plt.ylabel(f"Density")
    if save:
        plt.savefig(save)
        plt.close()


pdDataFrameGroupBy = TypeVar("pd.DataFrameGroupBy")


def group_scatter_plots(
    c: Config,
    groups: List[Tuple[float, pdDataFrameGroupBy]],
    # Functions that return the x and y data.
    group_x: Callable[[pd.DataFrame], List[float]],
    group_y: Callable[[pd.DataFrame], List[float]],
    group_x_label: str = None,
    group_y_label: str = None,
    cols: int = 2,
    save: str = None,
    title: str = None,
):
    """Scatter plots for each group of data and for the full data."""
    # Setup groups, rows and columns.
    num_groups = max(map(lambda x: x[0], groups)) + 1  # + 1 for the 0 index.
    rows = ceil(num_groups / cols) + 1
    row, col = 0, 0

    # Add a wide header plot of all the data.
    print_d(D, f"rows = {rows}, cols = {cols}, row = {row}, col = {col}")
    plt.subplot2grid((rows, cols), (row, col), colspan=cols)
    plt.scatter(group_x(c.vehicle_data), group_y(c.vehicle_data), s=10)
    if title:
        plt.title(f"{title} (all data)")
    if group_x_label:
        plt.xlabel(group_x_label)
    if group_y_label:
        plt.ylabel(group_y_label)
    xlim, ylim = plt.xlim(), plt.ylim()

    # Add a subplot for each group.
    def add_1():
        nonlocal col
        nonlocal row
        col = 0 if col == cols - 1 else col + 1
        if col == 0:
            row += 1

    row += 1  # For the wide header plot.
    last_i = 0
    for (i, group) in [(int(i), g) for i, g in groups]:
        print_d(D, f"i = {i}")
        [add_1() for _ in range(last_i + 1, i)]  # For any empty groups.
        last_i = i
        print_d(D, f"rows = {rows}, cols = {cols}, row = {row}, col = {col}")
        plt.subplot2grid((rows, cols), (row, col))
        plt.scatter(group_x(group), group_y(group), s=10)
        if title:
            plt.title(f"{title} (group {i})")
        if group_x_label:
            plt.xlabel(group_x_label)
        if group_y_label:
            plt.ylabel(group_y_label)
        plt.xlim(xlim)
        plt.ylim(ylim)
        add_1()
    plt.gcf().set_size_inches(16, 10)
    plt.tight_layout()
    if save:
        plt.savefig(save)
        plt.close()


def plot_length_vs_axles(c: Config, cols: int = 2, save: str = None):
    """Plot length vs number of axles for each length group."""
    group_length = lambda group: group["length"] / 100
    group_num_axles = lambda group: group["weight_per_axle"].apply(
        lambda s: len(axle_array_and_count(s))
    )
    group_scatter_plots(
        c=c,
        groups=vehicle_pdf_groups(c),
        group_y=group_num_axles,
        group_x=group_length,
        group_y_label="number of axles",
        group_x_label="length (m)",
        cols=cols,
        save=save,
        title="Vehicle length against number of axles",
    )


def plot_length_vs_weight(c: Config, cols: int = 2, save: str = None):
    """Plot length vs number of axles for each length group."""
    group_length = lambda group: group["length"] / 100
    group_weight = lambda group: group["total_weight"]
    group_scatter_plots(
        c=c,
        groups=vehicle_pdf_groups(c),
        group_y=group_weight,
        group_x=group_length,
        group_y_label="weight (kN)",
        group_x_label="length (m)",
        cols=cols,
        save=save,
        title="Vehicle length against weight",
    )


def plot_weight_vs_axles(c: Config, cols: int = 2, save: str = None):
    """Plot length vs number of axles for each length group."""
    group_weight = lambda group: group["total_weight"]
    group_num_axles = lambda group: group["weight_per_axle"].apply(
        lambda s: len(axle_array_and_count(s))
    )
    group_scatter_plots(
        c=c,
        groups=vehicle_pdf_groups(c),
        group_x=group_weight,
        group_y=group_num_axles,
        group_x_label="weight (kN)",
        group_y_label="number of axles",
        cols=cols,
        save=save,
        title="Vehicle number of axles against weight",
    )
