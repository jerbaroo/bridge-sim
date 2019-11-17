"""Load and save traffic information."""
import os
import pickle
from timeit import default_timer as timer

import numpy as np

from config import Config
from model.scenario import TrafficScenario, to_traffic_array
from util import print_i, safe_str


def _traffic_name(
        c: Config, traffic_scenario: TrafficScenario, max_time: float):
    return safe_str(
        f"{traffic_scenario.name} {c.il_num_loads} {max_time} {c.sensor_hz}")


def load_traffic_array(
    c: Config,
    traffic_scenario: TrafficScenario,
    max_time: float,
):
    """Load a 'TrafficArray' from disk, is is generated if necessary."""
    path = c.get_traffic_path(_traffic_name(
        c=c, traffic_scenario=traffic_scenario, max_time=max_time)) + ".npy"
    print(path)

    # Create the traffic if it doesn't exist.
    if not os.path.exists(path):
        traffic_sequence, start_time = traffic_scenario.traffic_sequence(
            bridge=c.bridge, max_time=max_time)
        total_time = start_time + max_time
        start = timer()
        traffic_array = to_traffic_array(
            c=c, traffic_sequence=traffic_sequence, max_time=total_time)
        np.save(path, traffic_array)
        print_i(
            f"Generated {start_time:.3f} + {max_time:.3f} = {total_time:.3f}s"
            + f" traffic of type {traffic_scenario.name} at {c.sensor_hz}Hz"
            + f" in {timer() - start:.3f}s ({c.il_num_loads} lane steps)"
        )

    return np.load(path)


if __name__ == "__main__":
    from classify.scenario.traffic import normal_traffic
    from model.bridge.bridge_705 import bridge_705_config, bridge_705_3d

    c = bridge_705_config(bridge_705_3d)
    traffic_scenario = normal_traffic(c, 5, 2)
    load_traffic_array(
        c=c, traffic_scenario=traffic_scenario, max_time=60*0.5)
