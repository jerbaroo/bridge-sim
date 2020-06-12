"""Time series of responses to temperature.

Parsed temperature data is from:
https://www1.ncdc.noaa.gov/pub/data/uscrn/products/subhourly01/2019/

"""

import datetime
import os
from copy import deepcopy
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from lib.plot import plt
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression

from bridge_sim import sim
from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.util import print_d, print_i, print_w, project_dir

# D: str = "classify.temperature"
D: bool = False


def parse_line(line: str):
    """Parse a line of NOAA weather data.

    Args:
        line: a line of NOAA weather data.

    Returns: a tuple of (datetime, air temperature, solar radiation).

    """
    # 23803 20190101 0005 20181231 1805      3  -89.43   34.82    12.4
    # 0.0      0 0    10.9 C 0    88 0 -99.000 -9999.0  1115 0   0.79 0
    line = line.split()
    ds = line[1]  # Date string.
    ts = line[2]  # Time string.
    year, mon, day, hr, mn = (ds[0:4], ds[4:6], ds[6:8], ts[0:2], ts[2:4])
    # 2011-11-04T00:05
    dt = datetime.fromisoformat(f"{year}-{mon}-{day}T{hr}:{mn}")
    return [dt, float(line[-15]), float(line[-13])]


def load(
    name: str, temp_quantile: Tuple[float, float] = (0.001, 0.999)
) -> pd.DataFrame:
    """Load weather data from a file.

    The returned DataFrame will have duplicate datetimes removed, will have NaN
    and INF values removed and will have 'temp_quantile' lower and upper
    quantiles removed. Missing values will NOT be filled in.

    Args:
        name: name of the file to load (without extension).
        temp_quantile: tuple of lower and upper air temperature quantiles to
            ignore (incase of extreme values).

    Returns: a DataFrame of datetimes, air temperature and solar radiation.

    """
    # If the file is already parsed, return it..
    name_path = os.path.join(project_dir(), "data/temperature", name + ".txt")
    saved_path = name_path + ".parsed"
    if os.path.exists(saved_path):
        df = pd.read_csv(saved_path, index_col=0, parse_dates=["datetime"])
        lq = df["temp"].quantile(temp_quantile[0])
        hq = df["temp"].quantile(temp_quantile[1])
        print(f"Temperature {temp_quantile} quantiles = {lq}, {hq}")
        df = df[(df["temp"] >= lq) & (df["temp"] <= hq)]
        return df
    # ..otherwise read and parse the data.
    with open(name_path) as f:
        temps = list(map(parse_line, f.readlines()))
    # Remove NANs.
    for line_ind, [dt, temp, solar] in enumerate(temps):
        if np.isnan(temp):
            print_i(f"NAN in {name} temperature")
            temps[line_ind][1] = temps[line_ind - 1][1]
        if np.isnan(solar):
            print_i(f"NAN in {name} solar radiation")
            temps[line_ind][2] = temps[line_ind - 1][2]
    # Pack it into a DataFrame.
    df = pd.DataFrame(temps, columns=["datetime", "temp", "solar"])
    # Remove duplicate datetimes.
    len_before = len(df)
    df = df.drop_duplicates(subset=["datetime"], keep="first")
    len_after = len(df)
    print_i(f"Removed {len_before - len_after} duplicates, now {len_after} rows")
    # Sort by datetime.
    df = df.sort_values(by=["datetime"])
    # Save to file and return that DataFrame.
    df.to_csv(saved_path)
    return load(name=name)


def resize(
    temps: List[float],
    tmin: Optional[int] = None,
    tmax: Optional[int] = None,
    year: Optional[int] = None,
) -> List[float]:
    """Resize temperatures into a range.

    Args:
        temps: a list of temperatures.
        tmin: minimum temperature in returned range.
        tmax: maximum temperature in returned range.
        year: preset values for tmin and tmax, 2018 or 2019. If given there's no
            need to provide the tmin and tmax values.

    Returns: the given temperatures interpolated into a new range.

    """
    if year is not None:
        if year == 2018:
            tmin, tmax = -2, 32
        elif year == 2019:
            tmin, tmax = -5, 35
        else:
            raise NotImplementedError(f"Unknown year {year}")
    assert tmin < 0
    assert tmax > 30
    print_i(f"Resizing temps into: T_min, T_max = ({tmin}, {tmax})")
    return interp1d(
        np.linspace(min(temps), max(temps), 10000), np.linspace(tmin, tmax, 10000)
    )(temps)


def from_to_mins(df: pd.DataFrame, from_: datetime, to: datetime) -> pd.DataFrame:
    """Minutely weather data interpolated into a range (inclusive).

    Args:
        df: weather data loaded with 'load'.
        from_: datetime of the first minute in the range.
        to: datetime of the last minute in the range.

    Returns: a DataFrame with values interpolated in the given range.

    """
    # Create times and temperatures from given data.
    dates, temps, solar = df["datetime"], df["temp"], df["solar"]
    times = dates.apply(lambda d: datetime.timestamp(d))
    # Create times that are expected to return.
    result_dates, result_times = [], []
    curr = from_
    while curr <= to:
        result_dates.append(curr)
        result_times.append(datetime.timestamp(curr))
        curr += timedelta(minutes=1)
    # Interpolate to get results.
    result_temps = interp1d(times, temps, fill_value="extrapolate")(result_times)
    result_solar = interp1d(times, solar, fill_value="extrapolate")(result_times)
    # Pack it into a DataFrame.
    df = pd.DataFrame(
        np.array([result_dates, result_temps, result_solar]).T,
        columns=["datetime", "temp", "solar"],
    )
    # Sort.
    df = df.sort_values(by=["datetime"])
    df["temp"] = pd.to_numeric(df["temp"])
    df["solar"] = pd.to_numeric(df["solar"])
    return df


def temp_profile(temps: List[float], solar: List[float]):
    """Bottom and top bridge deck temperatures for given weather data.

    Args:
        temps: list of air temperature.
        solar: list of solar radiation.

    Returns: tuple of two lists, bottom and top bridge deck temperatures.

    """
    bd = 0.001

    temps_b = [temps[0]]
    for i, temp_a in enumerate(temps[1:]):
        temps_b.append((1 - bd) * temps_b[i - 1] + bd * temp_a)

    sn = 0.008
    ss = 0.0001
    temps_s = [temps[0]]

    for i, (temp_a, solar) in enumerate(zip(temps[1:], solar[1:])):
        if False:
            recent_max = np.max(temps[max(0, recent_start) : i])
            temps_s.append((1 - sd) * temps_s[i - 1] + sd * recent_max)
        else:
            temps_s.append((1 - sn - ss) * temps_s[i - 1] + sn * temp_a + ss * solar)

    return np.array(temps_b), np.array(temps_s)


def effect(
    config: Config,
    response_type: ResponseType,
    points: List[Point],
    weather: Optional[pd.DataFrame] = None,
    temps_bt: Optional[Tuple[List[float], List[float]]] = None,
    d: bool = False,
) -> List[List[float]]:
    """Temperature effect at points for some weather data.

    The returned responses contain the post-processing necessary for strain.
    Note that you should be using the same "weather" each time you use this
    function, this is because the calculation of bridge deck top and bottom
    temperatures will be different when calculated over a subset.

    Args:
        config: Config, simulation configuration object.
        response_type: type of sensor response to temp. effect.
        points:  points at which to calculate temperature effect.
        weather: DataFrame to calculate temperature profile time series from.
        temps_bt: if 'weather' is not provided you can pass in a tuple of the
            temperature at the bottom and top of the bridge deck.
        d: a flag for debugging.

    Returns: NumPy array of temperature effect, indexed by point then time.

    """
    # Unit effect from uniform temperature loading.
    uniform_responses = sim.responses.load(
        config=config, response_type=response_type, temp_deltas=(1, None)
    )
    linear_responses = sim.responses.load(
        config=config, response_type=response_type, temp_deltas=(None, 1)
    )
    if response_type.is_strain():
        uniform_responses = uniform_responses.add_temp_strain(
            config=config, temp_deltas=(1, None)
        )
        linear_responses = linear_responses.add_temp_strain(
            config=config, temp_deltas=(None, 1)
        )
    print_i("Loaded unit temperature responses")

    # Effect to unit temperature loading only at requested points.
    unit_uniforms = np.array(uniform_responses.at_decks(points))
    unit_linears = np.array(linear_responses.at_decks(points))
    assert len(unit_uniforms.shape) == 1
    assert unit_uniforms.shape[0] == len(points)

    # Determine temperature profile.
    if temps_bt is None:
        temps_bt = temp_profile(temps=weather["temp"], solar=weather["solar"])
        print_w("Make sure calculating profile from entire year!!")
    temps_bottom, temps_top = np.array(temps_bt[0]), np.array(temps_bt[1])
    temps_half = (temps_bottom + temps_top) / 2
    temps_linear = temps_top - temps_bottom
    temps_uniform = temps_half - config.bridge.ref_temp_c

    # print(f"temps_bottom.shape = {temps_bottom.shape}")
    # print(f"temps_top.shape = {temps_top.shape}")
    # print(f"temps_half.shape = {temps_half.shape}")
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
    # print(f"uniform_responses.shape = {uniform_responses.shape}")
    # print(f"linear_responses.shape = {linear_responses.shape}")
    print_d(D, f"uniform responses = {uniform_responses[:3]}")
    print_d(D, f"linear responses = {linear_responses[:3]}")
    if d:
        return temps_uniform, temps_linear, uniform_responses + linear_responses
    return uniform_responses + linear_responses


def remove_daily(num_samples, signal):
    """Remove from the given signal by interpolating at 'num_samples' points.

    Data must be of shape n samples x f features.

    Args:
        num_samples: number of samples e.g. 24.
        signal: the temperature or feature signal.

    Returns: a tuple of the interpolated signal, and the signal to remove.

    """
    # 'num_samples + 1' indices into given signal.
    indices = list(map(int, np.linspace(0, len(signal) - 1, num_samples + 1)))
    # Mean value of the signal between each pair of indices,
    # and new indices, at center between each pair of indices.
    y_samples, new_indices = [], []
    for i_lo, i_hi in zip(indices[:-1], indices[1:]):
        y_samples.append(np.mean(signal[i_lo:i_hi]))
        new_indices.append(int((i_lo + i_hi) / 2))
    rm = interp1d(new_indices, y_samples, fill_value="extrapolate")(
        np.arange(len(signal))
    )
    return rm, deepcopy(rm) - rm[0]


def regress_and_errors(x, y):
    """Linear regression predictor, and error from each given point."""
    lr = LinearRegression().fit(x.reshape(-1, 1), y)
    errors = []
    for x_, y_ in zip(x, y):
        errors.append(abs(y_ - lr.predict([[x_]])[0]))
    return lr, np.array(errors)


__all__ = ["load", "resize", "effect", "remove_daily", "regress_and_errors"]
