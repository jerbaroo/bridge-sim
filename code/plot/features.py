"""Plots for extracted events and features."""
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np

from classify.data.features import abs_threshold_trigger, events_from_time_series
from classify.data.responses import responses_to_mv_load, times_on_bridge_
from config import Config
from fem.run import FEMRunner
from model import MovingLoad, Point, ResponseType
from util import *
from vehicles.sample import sample_vehicle


def plot_threshold_distribution(
        c: Config, mv_loads: List[MovingLoad], response_type: ResponseType,
        fem_runner: FEMRunner, at: Point, num_thresholds: int,
        use_lengths: bool=False, save: str=None, show: bool=False):
    """Plot distribution of distance to a sensor while varying threshold.

    Plot the mean distance to the sensor each threshold value when the event is
    triggered is collected. Alternatively the mean lengths of the collected
    events per threshold value can be plotted. For each plot also include on a
    separate y-axis the amount of missed and phantom events recorded per
    threshold value.

    """
    time_serieses = []
    for i, mv_load in enumerate(mv_loads):
        mv_load_times = times_on_bridge_(c, mv_load)
        time_serieses.append(responses_to_mv_load(
            c, mv_load, response_type, fem_runner, mv_load_times, [at]))
        # print_d(f"time_series = {time_serieses[-1]}")
        print_d(f"times = {mv_load_times}")
        print_d(f"len times = {len(mv_load_times)}")
        print_d(f"len = {len(time_serieses[-1])}")
        print_d(f"min = {min(time_serieses[-1])}")
        print_d(f"max = {max(time_serieses[-1])}")
    time_serieses = np.array(time_serieses)
    min_response = np.amin(np.abs(time_serieses))
    max_response = np.amax(np.abs(time_serieses))
    print_d(f"min = {min_response}, max = {max_response}")
    thresholds = np.linspace(min_response, max_response, num_thresholds)
    # events = events_from_time_series(mv_load_time_series)
    # print_d(f"num events = {len(events)}")

    missed, extra, distances, lengths = [], [], [], []
    for thresh_i, threshold in enumerate(thresholds):
        print_i(f"threshold = {threshold:.2f}, {thresh_i / len(thresholds)}")
        missed_events = 0
        extra_events = 0
        event_distances = []
        event_lengths = []
        trigger = abs_threshold_trigger(threshold)
        print_d(f"threshold = {threshold}")
        for i, time_series in enumerate(time_serieses):
            events, event_start_times = events_from_time_series(
                c, trigger, time_series, with_time=True)
            print_d(f"{time_series}")
            print_d(f"{events}")
            print_d(f"{event_start_times}")
            print_d(f"threshold = {threshold}")
            print_d(f"len time_series = {len(time_series)}")
            print_d(f"len events = {len(events)}")
            # e, s = events[0], event_start_times[0]
            # print_d(f"start time = {s}")
            # print_d(f"time = {s * c.time_step}")
            # print_d(f"at = {mv_loads[i].x_at(s * c.time_step, c.bridge)}")
            print_d(f"sensor = {at.x}")
            event_distances.extend(
                [np.abs(mv_loads[i].x_at(start_time * c.time_step, c.bridge)
                        - at.x)
                 for start_time in event_start_times])
            # print_d(f"distances = {event_distances[-1]}")
            event_lengths.extend([len(event) for event in events])
            # print_d(f"lengths = {event_lengths[-1]}")
            missed_events += max(0, 1 - len(events))
            print_d(f"missed = {max(0, 1 - len(events))}")
            print_d(f"{extra_events}")
            print_d(f"{len(events)}")
            print_d(f"{len(events) - 1}")
            print_d(f"{max(0, len(events) - 1)}")
            extra_events += max(0, len(events) - 1)
            print_d(f"extra = {max(0, len(events) - 1)}")
        missed.append(missed_events)
        extra.append(extra_events)
        distances.append(event_distances)
        lengths.append(event_lengths)
    print_d(f"missed = {missed}")
    print_d(f"extra = {extra}")
    print_d(f"distances = {distances}")
    print_d(f"lengths = {lengths}")
    _, ax = plt.subplots()
    ax.plot(missed, label="missed vehicles")
    ax.plot(extra, label="phantom vehicles")
    plt.legend()
    ax2 = ax.twinx()
    secondary_data = lengths if use_lengths else distances
    secondary_data_name = "lengths" if use_lengths else "distances"
    ax2.plot(
        list(map(np.mean, secondary_data)),
        label=secondary_data_name,
        color="green")
    secondary_data = lengths if not use_lengths else distances
    secondary_data_name = "lengths" if not use_lengths else "distances"
    ax2.plot(
        list(map(np.mean, secondary_data)),
        label=secondary_data_name,
        color="red")
    plt.legend()
    plt.show()


def plot_normal_threshold_distribution(
        c: Config, response_type: ResponseType, fem_runner: FEMRunner,
        at: Point, num_loads: int, num_thresholds: int, save: str=None,
        show: bool=False):
    """Like plot_threshold_distribution but for normal sampled loads."""
    vehicles = [sample_vehicle(c) for _ in range(num_loads)]
    mv_loads = [MovingLoad.from_vehicle(x_frac=0, vehicle=vehicle, lane=0)
                for vehicle in vehicles]
    plot_threshold_distribution(
        c, mv_loads, response_type, fem_runner, at, num_thresholds, save, show)
