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
from util import print_i

temperatures = dict()


def load_temperature_month(month: str) -> pd.DataFrame:
    if month in temperatures:
        return temperatures[month]
    def parse_line(line):
        line = line.split()  # 79J 2019 05 31 2330 0530
        ds = line[1]  # Date string.
        year, mon, day, hr, mn = ds[-16:-12], ds[-12:-10], ds[-10:-8], ds[-8:-6], ds[-6:-4]
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
        temperatures[month] = pd.read_csv(saved_path, index_col=0, parse_dates=["datetime"])
        return temperatures[month]
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
                to_append = pd.Series({
                    "datetime": curr,
                    "temp": float(df[df["datetime"] == dt]["temp"]),
                    "missing": True,
                })
                df = df.append(to_append, ignore_index=True)
            curr = curr + timedelta(minutes=1)
            if not isinstance(curr, datetime):
                print(type(curr))
                import sys; sys.exit()
        if delta_mins > 1:
            print(f"Missing {delta_mins - 1} minutes before {dt}")
        missing += delta_mins - 1
    print_i(f"Added {missing} minutes")
    # Sort.
    df = df.sort_values(by=["datetime"])
    # Add timestamp row.
    df["ts"] = df["datetime"].apply(lambda d: datetime.timestamp(d))
    # Smooth.
    df["temp"] = savgol_filter(df["temp"], 51, 3) # window size 51, polynomial order 3
    # Save.
    temperatures[month] = df
    df.to_csv(saved_path)
    return temperatures[month]


def temperature_effect(c: Config, response_type: ResponseType, temps: List[float]) -> List[float]:
    unit_thermal = ThermalDamage(axial_delta_temp=c.unit_axial_delta_temp_c)
    c, sim_params = unit_thermal.use(
        c=c, sim_params=SimParams(response_types=[response_type])
    )
    sim_responses = load_fem_responses(
        c=c,
        sim_runner=OSRunner(c),
        response_type=response_type,
        sim_params=sim_params,
    )
    point = Point(x=51, y=0, z=-8.4)
    unit_response = sim_responses.at_deck(point, interp=True)
    return (np.array(temps) - c.bridge.ref_temp_c) * unit_response
