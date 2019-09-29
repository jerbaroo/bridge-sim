"""Plots for extracted events and features."""
# TODO: rename to events.py.
from typing import List, Tuple

import matplotlib.patches as patches
import numpy as np

from classify.data.events import events_from_mv_loads
from config import Config
from fem.run import FEMRunner
from model.bridge import Point
from model.load import MovingLoad
from model.response import Event, ResponseType
from plot import plt
from util import print_d, print_i
from vehicles.sample import sample_vehicle

# Print debug information for this file.
D: bool = False


def plot_event(
        c: Config, event: Event, start_index: int, num_loads: int,
        response_type: ResponseType, at: Point, overlap: Tuple[int, int],
        y_max: float, y_min: float):
    """Plot a single event with timing and overlap information."""
    time_series = event.get_time_series(noise=False)
    time_series_with_noise = event.get_time_series(noise=True)
    x_min = start_index * c.time_step
    x_max = (start_index + len(time_series)) * c.time_step
    overlap_height = y_max - y_min
    # Plot LHS overlap.
    if overlap[0]:
        overlap_width = (x_max - x_min) * (overlap[0] / len(time_series))
        plt.gca().add_patch(patches.Rectangle(
            xy=(x_min, y_min), width=overlap_width, height=overlap_height,
            alpha=0.1))
    # Plot RHS overlap.
    if overlap[1]:
        overlap_width = (x_max - x_min) * (overlap[1] / len(time_series))
        plt.gca().add_patch(patches.Rectangle(
            xy=(x_max - overlap_width, y_min), width=overlap_width,
            height=overlap_height, alpha=0.1))
    print_i(f"x_min = {x_min}")
    print_i(f"x_max = {x_max}")
    print_i(f"x.shape = {np.linspace(x_min, x_max, len(time_series)).shape}")
    x_axis = np.linspace(x_min, x_max, num=len(time_series))
    plt.plot(x_axis, time_series_with_noise, color="tab:orange")
    plt.plot(x_axis, time_series, color="tab:blue")
    s = "s" if num_loads > 1 else ""
    plt.title(
        f"{response_type.name()} at {at.x:.2f}m from {num_loads} vehicle{s}")
    plt.xlabel("time (s)")
    plt.ylabel(f"{response_type.name().lower()} ({response_type.units()})")


def plot_events_from_mv_loads(
        c: Config, mv_loads: List[List[MovingLoad]],
        response_type: ResponseType, fem_runner: FEMRunner, at: Point,
        save: str = None, show: bool = False):
    """Plot events from each set of moving loads on a row."""
    print_d(D, f"TODO: Support multiple vehicles")
    # Determine rows, cols and events per row.
    rows = len(mv_loads)
    events = [
        list(events_from_mv_loads(
            c=c, mv_loads=mv_loads[row], response_types=[response_type],
            fem_runner=fem_runner, at=[at]))[0][0]
        for row in range(rows)]
    cols = max(len(es) for es in events)
    assert isinstance(events[0][0], Event)
    assert isinstance(events[0][0].time_series, list)
    print_i(f"first time series = {events[0][0].time_series}")
    y_min, y_max = 0, 0
    for es in events:
        for e in es:
            y_min = np.min([y_min, np.min(e.get_time_series(noise=True))])
            y_max = np.max([y_max, np.max(e.get_time_series(noise=True))])
    assert isinstance(y_min, float)
    assert isinstance(y_max, float)
    y_min, y_max = np.min([y_min, -y_max]), np.max([y_max, -y_min])
    print_i(f"rows, cols = {rows}, {cols}")
    # Plot each event, including overlap.
    for row in range(rows):
        for col, event in enumerate(events[row]):
            print_i(f"row, col = {row}, {col}")
            plt.subplot2grid((rows, cols), (row, col))
            print(len(events[row]) - 1)
            print(col)
            print(col < len(events[row]) - 1)
            end_overlap = (
                events[row][col + 1].overlap
                if col < len(events[row]) - 1
                else 0)
            plot_event(
                c=c, event=event, start_index=events[row][col].start_index,
                num_loads=len(mv_loads[row]), response_type=response_type,
                at=at, overlap=(events[row][col].overlap, end_overlap),
                y_min=y_min, y_max=y_max)
    if save: plt.savefig(save)
    if show: plt.show()
    if save or show: plt.close()


def plot_events_from_normal_mv_loads(
        c: Config, response_type: ResponseType, fem_runner: FEMRunner,
        at: Point, rows: int=5, loads_per_row: int=1, lane: int=0,
        save: str=None, show: bool=False):
    """Plot events from each set of sampled normal loads on a row."""
    mv_loads = [
        [MovingLoad.from_vehicle(
            x_frac=-i * 0.1, vehicle=sample_vehicle(c), lane=lane)
        for i in range(loads_per_row)]
        for _ in range(rows)]
    shape = np.array(mv_loads).shape
    assert len(shape) == 2
    assert shape[0] == rows
    assert shape[1] == loads_per_row
    plot_events_from_mv_loads(
        c=c, mv_loads=mv_loads, response_type=response_type,
        fem_runner=fem_runner, at=at, save=save, show=show)
