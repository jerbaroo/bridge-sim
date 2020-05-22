"""Load and save traffic information."""
import os
from typing import Optional

import dill
import numpy as np

from bridge_sim.model import Config
from bridge_sim.traffic import TrafficScenario, to_traffic, to_traffic_array
from bridge_sim.util import safe_str


def _traffic_name(c: Config, traffic_scenario: TrafficScenario, max_time: float):
    return safe_str(
        f"{traffic_scenario.name} {c.il_num_loads} {max_time} {c.sensor_hz}"
    )


def load_traffic(
    c: Config,
    traffic_scenario: TrafficScenario,
    max_time: float,
    add: Optional[str] = None,
):
    """Load traffic from disk, generated if necessary."""
    path = (
        c.get_data_path(
            "traffic",
            _traffic_name(c=c, traffic_scenario=traffic_scenario, max_time=max_time),
            acc=False,
        )
        + ".npy"
    )
    print(path)
    if add is not None:
        path += add
    # Create the traffic if it doesn't exist.
    if not os.path.exists(path + ".arr"):
        traffic_sequence = traffic_scenario.traffic_sequence(
            bridge=c.bridge, max_time=max_time
        )
        traffic = to_traffic(c=c, traffic_sequence=traffic_sequence, max_time=max_time)
        traffic_array = to_traffic_array(
            c=c, traffic_sequence=traffic_sequence, max_time=max_time
        )
        with open(path + ".seq", "wb") as f:
            dill.dump(traffic_sequence, f)
        with open(path + ".tra", "wb") as f:
            dill.dump(traffic, f)
        with open(path + ".arr", "wb") as f:
            np.save(f, traffic_array)
    with open(path + ".seq", "rb") as f:
        traffic_sequence = dill.load(f)
    with open(path + ".tra", "rb") as f:
        traffic = dill.load(f)
    with open(path + ".arr", "rb") as f:
        traffic_array = np.load(f)
    return traffic_sequence, traffic, traffic_array
