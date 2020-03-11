import math
import os
from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d

from classify.scenario.bridge import ThermalDamage
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.response import ResponseType
from util import print_d, print_i

D: str = "classify.temperature"
D: bool = False

# https://www1.ncdc.noaa.gov/pub/data/uscrn/products/subhourly01/2019/

__dir__ = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../"))


def parse_line(line):
    # 23803 20190101 0005 20181231 1805      3  -89.43   34.82    12.4
    # 0.0      0 0    10.9 C 0    88 0 -99.000 -9999.0  1115 0   0.79 0
    line = line.split()
    ds = line[1]  # Date string.
    ts = line[2]  # Time string.
    year, mon, day, hr, mn = (ds[0:4], ds[4:6], ds[6:8], ts[0:2], ts[2:4])
    # 2011-11-04T00:05
    dt = datetime.fromisoformat(f"{year}-{mon}-{day}T{hr}:{mn}")
    return [dt, float(line[-11])]


def load(name: str, offset: int = 0) -> pd.DataFrame:
    # If the file is already parsed, return it..
    name_path = os.path.join(__dir__, "data/temperature", name + ".txt")
    saved_path = name_path + ".parsed"
    if os.path.exists(saved_path):
        temps = pd.read_csv(saved_path, index_col=0, parse_dates=["datetime"])
        temps["temp"] = temps["temp"].add(offset)
        return temps
    # ..otherwise read and parse the data.
    with open(name_path) as f:
        temps = list(map(parse_line, f.readlines()))
    # Remove NANs.
    for line_ind, [dt, temp] in enumerate(temps):
        if np.isnan(temp):
            print_i(f"NAN in {name} temperature")
            temps[line_ind][-1] = temps[line_ind - 1][-1]
    # Pack it into a DataFrame.
    df = pd.DataFrame(temps, columns=["datetime", "temp"])
    # Convert to celcius.
    # df["temp"] = (df["temp"] - 32) * (5 / 9)
    # Remove duplicate times.
    len_before = len(df)
    df = df.drop_duplicates(subset=["datetime"], keep="first")
    len_after = len(df)
    print_i(f"Removed {len_before - len_after} duplicates, now {len_after} rows")
    # Sort.
    df = df.sort_values(by=["datetime"])
    # Save.
    df.to_csv(saved_path)
    return load_temperature(name=name, offset=offset)


def from_to_mins(df, from_, to, smooth: bool = False):
    # Create times and temperatures from given data.
    dates, temps = df["datetime"], df["temp"]
    times = dates.apply(lambda d: datetime.timestamp(d))
    # Create times that are expected to return.
    result_dates, result_times = [], []
    curr = from_
    while curr <= to:
        result_dates.append(curr)
        result_times.append(datetime.timestamp(curr))
        curr += timedelta(minutes=1)
    # Interpolate to get result temps.
    result_temps = interp1d(times, temps, fill_value="extrapolate")(result_times)
    # Pack it into a DataFrame.
    df = pd.DataFrame(
        np.array([result_dates, result_temps]).T, columns=["datetime", "temp"]
    )
    # Sort.
    df = df.sort_values(by=["datetime"])
    df["temp"] = pd.to_numeric(df["temp"])
    # Smooth.
    if smooth:
        df["temp"] = savgol_filter(df["temp"], 20, 3)
    return df


def from_to_indices(df, from_, to):
    """Indices of temperatures that correspond to the given range."""
    start, end = None, None
    for i, date in enumerate(df["datetime"]):
        if start is None and date >= from_:
            start = i
        if date >= to:
            return start, i
    raise ValueError("End date not found")


def temps_bottom_top(c: Config, temps: List[float], len_per_hour):
    """The top and bottom bridge temperatures for given air temperatures."""

    # temps_bottom = np.array(temps) - c.bridge.ref_temp_c
    # temps_top = temps_bottom + c.bridge.air_surface_temp_delta_c
    # return temps_bottom, temps_top

    bd = 0.001
    # bn = 0.008

    temps_b = [temps[0]]
    for i, temp_a in enumerate(temps[1:]):
        temps_b.append((1 - bd) * temps_b[i - 1] + bd * temp_a)

    recent_hours = 3
    sd = 0.008
    sn = 0.008
    temps_s = [temps[0]]

    for i, temp_a in enumerate(temps[1:]):
        recent_start = i - (len_per_hour * recent_hours)
        if i > 1 and temps_b[i - 1] > temps_b[i - 2]:
            recent_max = np.max(temps[max(0, recent_start) : i])
            temps_s.append((1 - sd) * temps_s[i - 1] + sd * recent_max)
        else:
            temps_s.append((1 - sn) * temps_s[i - 1] + sn * temp_a)

    return np.array(temps_b), np.array(temps_s)


def effect(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    len_per_hour: int = None,
    temps: List[float] = None,
    temps_bt=None,
    d: bool = False,
) -> List[List[float]]:
    """Temperature effect at given points for a number of given temperatures.

    The result is of shape (number of points, number of temperatures).

    NOTE: The 'ThermalDamage' method 'to_strain' multiplies the results by E-6,
        which is called by this function. Take note that the strain values are
        already increased by E-6, and do not need to be resized.

    Args:
        temps_bt: A 2-tuple of arrays, the first array is for the temperatures
            at the bottom of the bridge, and the second array is for the
            temperatures at the top of the bridge. If this argument is given
            then 'temps' and 'len_per_hour' will be ignored.

    """
    original_c = c
    # Unit effect from uniform temperature loading.
    unit_uniform = ThermalDamage(axial_delta_temp=c.unit_axial_delta_temp_c)
    c, sim_params = unit_uniform.use(original_c)
    uniform_responses = load_fem_responses(
        c=c, sim_runner=OSRunner(c), response_type=response_type, sim_params=sim_params,
    )
    # Convert uniform responses to correct type (thermal post-processing).
    if response_type in [ResponseType.Strain, ResponseType.StrainT]:
        uniform_responses = unit_uniform.to_strain(c=c, sim_responses=uniform_responses)
    elif response_type == ResponseType.Stress:
        uniform_responses = unit_uniform.to_stress(c=c, sim_responses=uniform_responses)
    unit_uniforms = np.array(
        [uniform_responses.at_deck(point, interp=True) for point in points]
    )
    # Unit effect from linear temperature loading.
    unit_linear = ThermalDamage(moment_delta_temp=c.unit_moment_delta_temp_c)
    c, sim_params = unit_linear.use(original_c)
    linear_responses = load_fem_responses(
        c=c, sim_runner=OSRunner(c), response_type=response_type, sim_params=sim_params,
    )
    # Convert linear responses to correct type (thermal post-processing).
    if response_type in [ResponseType.Strain, ResponseType.StrainT]:
        linear_responses = unit_linear.to_strain(c=c, sim_responses=linear_responses)
    elif response_type == ResponseType.Stress:
        linear_responses = unit_linear.to_stress(c=c, sim_responses=linear_responses)
    unit_linears = np.array(
        [linear_responses.at_deck(point, interp=True) for point in points]
    )
    print_d(D, f"unit uniform and linear = {unit_uniforms} {unit_linears}")
    # Determine temperature gradient throughout the bridge.
    if temps_bt is None:
        temps_bottom, temps_top = temps_bottom_top(
            c=c, temps=temps, len_per_hour=len_per_hour
        )
    else:
        temps_bottom, temps_top = temps_bt
        temps_bottom, temps_top = np.array(temps_bottom), np.array(temps_top)
    temps_half = (temps_bottom + temps_top) / 2
    temps_linear = temps_top - temps_bottom
    temps_uniform = temps_half - c.bridge.ref_temp_c
    print_d(D, f"tb = {temps_bottom[:3]}")
    print_d(D, f"tt = {temps_top[:3]}")
    print_d(D, f"th = {temps_half[:3]}")
    print_d(D, f"temps linear = {temps_linear[:3]}")
    print_d(D, f"temps uniform = {temps_uniform[:3]}")
    # Combine uniform and linear responses.
    uniform_responses = np.array(
        [unit_uniform * temps_half for unit_uniform in unit_uniforms]
    )
    linear_responses = np.array(
        [unit_linear * temps_linear for unit_linear in unit_linears]
    )
    print_d(D, f"uniform responses = {uniform_responses[:3]}")
    print_d(D, f"linear responses = {linear_responses[:3]}")
    if d:
        return temps_uniform, temps_linear, uniform_responses + linear_responses
    return uniform_responses + linear_responses
    # return (np.array(temps) - c.bridge.ref_temp_c) * unit_response


def get_len_per_min(c: Config, speed_up: float):
    """Length of time series corresponding to 1 minute of temperature."""
    return int(np.around(((1 / c.sensor_hz) * 60) / speed_up, 0))


def resize(temps, tmin=-5, tmax=35):
    """Resize temperatures into a range."""
    return interp1d(
        np.linspace(min(temps), max(temps), 1000), np.linspace(tmin, tmax, 1000)
    )(temps)


def apply(effect: List[float], responses: List[float]):
    """Given effect interpolated across given responses."""
    i = interp1d(
        np.linspace(0, len(responses) - 1, 10000),
        np.linspace(0, len(effect) - 1, 10000)
    )(np.arange(len(responses)))
    return interp1d(np.arange(len(effect)), effect)(i)


def apply_effect(
    c: Config,
    points: List[Point],
    responses: List[List[float]],
    effect: List[List[float]],
    speed_up: int = 1,
    repeat_responses: bool = False,
) -> List[float]:
    """Time series of effect due to temperature at given points.

    Returns: a NumPy array of shape the same as given responses. The effect due
        to temperature is interpolated across the date range of the given
        responses, this is calculated under the assumption that temperature
        effect is given at one data point per minute and that the sensor
        responses are given at a rate of 'c.sensor_hz'.

    """
    raise ValueError("Deprecated")
    assert len(responses) == len(points)
    # Convert the temperature data into temperature effect at each point.
    # effect_ = effect(c=c, response_type=response_type, points=points, temps=temps)
    assert len(effect) == len(points)
    # A temperature sample is available per minute. Here we calculate the
    # number of responses between each pair of recorded temperatures and the
    # number of temperature samples required for the given responses.
    len_per_min = get_len_per_min(c=c, speed_up=speed_up)
    print_i(f"Length per minute = {len_per_min}, speed_up = {speed_up}")
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
        print_i(
            f"Increasing length of responses from {len(responses[0])} to {avail_len}"
        )
        num_temps_req = len(effect[0])
        new_responses = np.empty((len(responses), avail_len))
        for i in range(len(responses)):
            for j in range(math.ceil(avail_len / len(responses[0]))):
                start = j * len(responses[0])
                end = min(avail_len - 1, start + len(responses[0]))
                new_responses[i][start:end] = responses[i][: end - start]
        responses = new_responses
    # Fill in the responses array with the temperature effect.
    result = np.zeros((len(points), len(responses[0])))
    for i in range(len(points)):
        for j in range(num_temps_req - 1):
            start = j * len_per_min
            end = min(len(result[i]), start + len_per_min)
            print_d(D, f"start = {start}")
            print_d(D, f"end = {end}")
            print_d(D, f"end - start = {end - start}")
            # print_d(D, f"temp_start, temp_end = {temps[j]}, {temps[j + 1]}")
            print_d(
                D, f"effect_start, effect_end = {effect[i][j]}, {effect[i][j + 1]}"
            )
            result[i][start:end] = np.linspace(
                effect[i][j], effect[i][j + 1], end - start
            )
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
