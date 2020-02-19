"""Load and save traffic information."""
import os
import pickle
from timeit import default_timer as timer

import dill

from config import Config
from model.scenario import TrafficScenario, to_traffic, to_traffic_array
from util import print_i, safe_str


def _traffic_name(c: Config, traffic_scenario: TrafficScenario, max_time: float):
    return safe_str(
        f"{traffic_scenario.name} {c.il_num_loads} {max_time} {c.sensor_hz}"
    )


def load_traffic(
    c: Config, traffic_scenario: TrafficScenario, max_time: float,
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
    # Create the traffic if it doesn't exist.
    if not os.path.exists(path):
        traffic_sequence = traffic_scenario.traffic_sequence(bridge=c.bridge, max_time=max_time)
        traffic = to_traffic(c=c, traffic_sequence=traffic_sequence, max_time=max_time)
        traffic_array = to_traffic_array(c=c, traffic_sequence=traffic_sequence, max_time=max_time)
        with open(path, "wb") as f:
            dill.dump((traffic_sequence, traffic, traffic_array), f)
    with open(path, "rb") as f:
        return dill.load(f)


if __name__ == "__main__":
    from classify.scenario.traffic import normal_traffic
    from model.bridge.bridge_705 import bridge_705_config, bridge_705_3d

    c = bridge_705_config(bridge_705_3d)
    traffic_scenario = normal_traffic(c, 5, 2)
    load_traffic_array(c=c, traffic_scenario=traffic_scenario, max_time=60 * 0.5)
