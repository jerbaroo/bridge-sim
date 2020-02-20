import math
import os
from datetime import datetime, timedelta
from typing import List

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from classify.scenario.bridge import ThermalDamage
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.response import ResponseType
from util import print_d, print_i

temperatures = dict()

D: str = "classify.temperature"
# D: bool = False


def load_temperature_month(month: str, offset: int = 15) -> pd.DataFrame:
    if month in temperatures:
        return temperatures[month]

    def parse_line(line):
        line = line.split()  # 79J 2019 05 31 2330 0530
        ds = line[1]  # Date string.
        year, mon, day, hr, mn = (
            ds[-16:-12],
            ds[-12:-10],
            ds[-10:-8],
            ds[-8:-6],
            ds[-6:-4],
        )
        # 2011-11-04T00:05
        dt = datetime.fromisoformat(f"{year}-{mon}-{day}T{hr}:{mn}")
        try:
            return [dt, float(line[-1])]
        except Exception as e:
            return [dt, np.nan]

    # Read the file in from disk.
    month_path = os.path.join("data/temperature", month + ".txt")
    saved_path = month_path + ".parsed"
    if os.path.exists(saved_path):
        temperatures[month] = pd.read_csv(
            saved_path, index_col=0, parse_dates=["datetime"]
        )
        temperatures[month]["temp"] = temperatures[month]["temp"].add(offset)
        return load_temperature_month(month=month, offset=offset)
    with open(month_path) as f:
        temperatures[month] = list(map(parse_line, f.readlines()))
    # Remove NANs.
    for line_ind, [dt, temp] in enumerate(temperatures[month]):
        if np.isnan(temp):
            print_i(f"NAN in {month} temperature")
            temperatures[month][line_ind][-1] = temperatures[month][line_ind - 1][-1]
    # Unpack.
    df = pd.DataFrame(temperatures[month], columns=["datetime", "temp"])
    # Convert to celcius.
    df["temp"] = (df["temp"] - 32) * (5 / 9)
    # Remove duplicate times.
    len_before = len(df)
    df = df.drop_duplicates(subset=["datetime"], keep="first")
    len_after = len(df)
    print_i(f"Removed {len_before - len_after} duplicates, now {len_after} rows")
    # Add missing times.
    df["missing"] = False
    first, last = min(df["datetime"]), max(df["datetime"])
    curr = (first - timedelta(minutes=1)).to_pydatetime()
    missing = 0
    for dt in sorted(df["datetime"][:]):
        delta_mins = 0
        while curr < dt:
            delta_mins += 1
            if delta_mins > 1:
                to_append = pd.Series(
                    {
                        "datetime": curr,
                        "temp": float(df[df["datetime"] == dt]["temp"]),
                        "missing": True,
                    }
                )
                df = df.append(to_append, ignore_index=True)
            curr = curr + timedelta(minutes=1)
            if not isinstance(curr, datetime):
                print("classify/temperature", flush=True)
                print(type(curr), flush=True)
                import sys

                sys.exit()
        if delta_mins > 1:
            print(f"Missing {delta_mins - 1} minutes before {dt}")
        missing += delta_mins - 1
    print_i(f"Added {missing} minutes")
    # Sort.
    df = df.sort_values(by=["datetime"])
    # Add timestamp row.
    df["ts"] = df["datetime"].apply(lambda d: datetime.timestamp(d))
    # Smooth.
    df["temp"] = savgol_filter(df["temp"], 51, 3)  # window size 51, polynomial order 3
    # Save.
    df.to_csv(saved_path)
    return load_temperature_month(month=month, offset=offset)


def temperature_effect(
    c: Config, response_type: ResponseType, points: List[Point], temps: List[float]
) -> List[float]:
    # Unit effect from uniform temperature loading.
    unit_uniform = ThermalDamage(axial_delta_temp=c.unit_axial_delta_temp_c)
    c, sim_params = unit_uniform.use(c)
    uniform_responses = load_fem_responses(
        c=c, sim_runner=OSRunner(c), response_type=response_type, sim_params=sim_params,
    )
    unit_uniforms = np.array([uniform_responses.at_deck(point, interp=True) for point in points])
    # Unit effect from linear temperature loading.
    unit_linear = ThermalDamage(moment_delta_temp=c.unit_moment_delta_temp_c)
    c, sim_params = unit_linear.use(c)
    linear_responses = load_fem_responses(
        c=c, sim_runner=OSRunner(c), response_type=response_type, sim_params=sim_params,
    )
    unit_linears = np.array([linear_responses.at_deck(point, interp=True) for point in points])
    print_d(D, f"unit uniform and linear = {unit_uniforms} {unit_linears}")
    # Combine uniform and linear.
    temps_bottom = np.array(temps) - c.bridge.ref_temp_c
    temps_top = temps_bottom + c.bridge.air_surface_temp_delta_c
    temps_half = (temps_bottom + temps_top) / 2
    print_d(D, f"tb = {temps_bottom[:3]}")
    print_d(D, f"tt = {temps_top[:3]}")
    print_d(D, f"th = {temps_half[:3]}")
    uniform_responses = np.array([
        unit_uniform * temps_half for unit_uniform in unit_uniforms
    ])
    temps_delta = temps_top - temps_bottom
    linear_responses = np.array([
        unit_linear * temps_delta for unit_linear in unit_linears
    ])
    print_d(D, f"temps_delta = {temps_delta[:3]}")
    print_d(D, f"uniform responses = {uniform_responses[:3]}")
    print_d(D, f"linear responses = {linear_responses[:3]}")
    return uniform_responses + linear_responses
    # return (np.array(temps) - c.bridge.ref_temp_c) * unit_response


def get_len_per_min(c: Config, speed_up: float):
    """Length of time series corresponding to 1 minute of temperature."""
    return int(np.around(((1 / c.sensor_hz) * 60) / speed_up, 0))


def get_temperature_effect(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    responses: List[List[float]],
    temps: List[float],
    speed_up: int,
    repeat_responses: bool = False,
) -> List[float]:
    """Temperature effect corresponding to time series at a number of points."""
    assert len(responses) == len(points)
    # Convert the temperature data into temperature effect at each point.
    effect = temperature_effect(
        c=c, response_type=response_type, points=points, temps=temps
    )
    assert len(effect) == len(points)
    # A temperature sample is available per minute. Here we calculate the number
    # of responses between each pair of recorded temperatures and the number of
    # temperature samples required for the given responses.
    len_per_min = get_len_per_min(c=c, speed_up=speed_up)
    num_temps_req = math.ceil(len(responses[0]) / len_per_min) + 1
    if num_temps_req > len(effect[0]):
        raise ValueError(
            f"Not enough temperatures ({len(effect[0])}) for data"
            f" (requires {num_temps_req})"
        )
    # If additional temperature data is available, then use it if requested and
    # repeat the given responses. Here we calculate length, in terms of the
    # sample frequency, recall that temperature is sampled every minute.
    avail_len = (len(effect[0]) - 1) * len_per_min
    if repeat_responses and (avail_len > len(responses[0])):
        print_i(f"Increasing length of responses from {len(responses[0])} to {avail_len}")
        num_temps_req = len(effect[0])
        new_responses = np.empty((len(responses), avail_len))
        for i in range(len(responses)):
            for j in range(math.ceil(avail_len / len(responses[0]))):
                start = j * len(responses[0])
                end = min(avail_len - 1, start + len(responses[0]))
                new_responses[i][start:end] = responses[i][: end - start]
        responses = new_responses
    # Fill in the responses array with the temperature effect.
    result = np.zeros((len(responses), len(responses[0])))
    for i in range(len(responses)):
        for j in range(num_temps_req - 1):
            start = j * len_per_min
            end = min(len(result[i]), start + len_per_min)
            print_d(D, f"start = {start}")
            print_d(D, f"end = {end}")
            print_d(D, f"end - start = {end - start}")
            print_d(D, f"temp_start, temp_end = {temps[j]}, {temps[j + 1]}")
            print_d(D, f"effect_start, effect_end = {effect[i][j]}, {effect[i][j + 1]}")
            result[i][start:end] = np.linspace(effect[i][j], effect[i][j + 1], end - start)
    if repeat_responses:
        return responses, result
    return result


def estimate_temp_effect(
    c: Config, responses: List[float], speed_up: float
) -> List[float]:
    from scipy.interpolate import interp1d

    # First get the length of the time series that corresponds to a minute, and
    # also to an hour, of temperature time.
    len_per_min = get_len_per_min(c=c, speed_up=speed_up)
    len_per_hr = len_per_min * 60
    # Determine indices of the readings in the given time series of responses.
    # And determine the reading, as the average response over the period.
    xs = np.arange(len(responses), 0, -len_per_hr)
    # print(f"xs = {xs}")
    temp_points = [np.mean(responses[max(0, i - len_per_hr) : i]) for i in xs]
    # print(f"len_per_hr = {len_per_hr}")
    # print(f"temp points = {temp_points}")
    f = interp1d(xs, temp_points, kind="cubic", fill_value="extrapolate")
    return f(np.arange(len(responses)))
    # import numpy.polynomial.polynomial as poly
    # coefs = poly.polyfit(xs, temp_points, 6)
    # print(f"coefs")
    # return poly.polyval(np.arange(len(responses)), coefs)
