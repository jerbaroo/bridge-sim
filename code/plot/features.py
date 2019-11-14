"""Plots for extracted events."""
# TODO: rename to events.py, no features here.
import math
from typing import List, Tuple

import matplotlib.patches as patches
import numpy as np

from classify.data.events import events_from_traffic
from config import Config
from fem.run import FEMRunner
from model.bridge import Bridge, Point
from model.load import MvVehicle
from model.response import Event, ResponseType
from model.scenario import BridgeScenario, TrafficScenario
from plot import plt
from util import print_d, print_i, pstr
from vehicles.sample import sample_vehicle

# Print debug information for this file.
D: bool = False


def plot_event(
    c: Config,
    event: Event,
    start_index: int,
    response_type: ResponseType,
    at: Point,
    overlap: Tuple[int, int],
    y_max: float,
    y_min: float,
):
    """Plot a single event with timing and overlap information."""
    time_series = event.get_time_series(noise=False)
    time_series_with_noise = event.get_time_series(noise=True)
    x_min = start_index * c.time_step
    x_max = (start_index + len(time_series)) * c.time_step
    overlap_height = y_max - y_min
    # Plot LHS overlap.
    if overlap[0]:
        overlap_width = (x_max - x_min) * (overlap[0] / len(time_series))
        plt.gca().add_patch(
            patches.Rectangle(
                xy=(x_min, y_min),
                width=overlap_width,
                height=overlap_height,
                alpha=0.1,
            )
        )
    # Plot RHS overlap.
    if overlap[1]:
        overlap_width = (x_max - x_min) * (overlap[1] / len(time_series))
        plt.gca().add_patch(
            patches.Rectangle(
                xy=(x_max - overlap_width, y_min),
                width=overlap_width,
                height=overlap_height,
                alpha=0.1,
            )
        )
    print_i(f"x_min = {x_min}")
    print_i(f"x_max = {x_max}")
    print_i(f"x.shape = {np.linspace(x_min, x_max, len(time_series)).shape}")
    x_axis = np.linspace(x_min, x_max, num=len(time_series))
    plt.plot(x_axis, time_series_with_noise, color="tab:orange")
    plt.plot(x_axis, time_series, color="tab:blue")
    plt.title(f"{response_type.name()} at {at.x:.2f}m")
    plt.xlabel("time (s)")
    plt.ylabel(f"{response_type.name().lower()} ({response_type.units()})")


def plot_events_from_traffic(
    c: Config,
    bridge: Bridge,
    bridge_scenario: BridgeScenario,
    traffic_name: str,
    traffic: "Traffic",
    start_time: float,
    time_step: float,
    response_type: ResponseType,
    points: List[Point],
    fem_runner: FEMRunner,
    cols: int = 4,
    save: str = None,
):
    """Plot events from a traffic simulation on a bridge."""
    # Determine rows, cols and events per row.
    time_per_event = int(c.time_end / time_step)
    events = events_from_traffic(
        c=c,
        traffic=traffic,
        bridge_scenario=bridge_scenario,
        points=points,
        response_types=[response_type],
        fem_runner=fem_runner,
        start_time=start_time,
        time_step=time_step,
    )
    print(
        f"event time = {c.time_end}, time step = {time_step}, time per event = {time_per_event}"
    )
    print(f"num traffic = {len(traffic)}")
    print(f"num events = {len(events)}")
    for p, point in enumerate(points):
        events_ = events[p][0]  # Currently only one response type.

        # First determine rows and max/min response.
        rows = math.ceil(len(events_) / cols)
        y_min, y_max = np.inf, -np.inf
        for event in events_:
            y_min = min(y_min, np.min(event.get_time_series(noise=True)))
            y_max = max(y_max, np.max(event.get_time_series(noise=True)))
        y_min = min(y_min, -y_max)
        y_max = max(y_max, -y_min)
        assert isinstance(y_min, float)
        assert isinstance(y_max, float)
        y_min, y_max = np.min([y_min, -y_max]), np.max([y_max, -y_min])
        print_i(f"rows, cols = {rows}, {cols}")

        # Plot each event, including overlap.
        event_index = 0
        for row in range(rows):
            if event_index >= len(events_):
                break
            for col in range(cols):
                if event_index >= len(events_):
                    break
                event = events_[event_index]
                print_i(f"row, col = {row}, {col}")
                plt.subplot2grid((rows, cols), (row, col))
                end_overlap = (
                    event.overlap if event_index < len(events_) - 1 else 0
                )
                plot_event(
                    c=c,
                    event=event,
                    start_index=event.start_index,
                    response_type=response_type,
                    at=point,
                    overlap=(event.overlap, end_overlap),
                    y_min=y_min,
                    y_max=y_max,
                )
                event_index += 1
        if save:
            plt.savefig(f"{save}-at-{pstr(str(point))}")
            plt.close()
