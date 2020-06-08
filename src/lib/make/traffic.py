import matplotlib.pyplot as plt

from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.sim.responses import responses_to_traffic_array
from bridge_sim.traffic import normal_traffic, to_traffic_array


def plot_traffic(config: Config):
    max_time = 30
    traffic_scenario = normal_traffic(c=config, lam=5, min_d=2)
    traffic_sequence = traffic_scenario.traffic_sequence(
        bridge=config.bridge, max_time=max_time
    )
    traffic_array = to_traffic_array(
        c=config, traffic_sequence=traffic_sequence, max_time=max_time, warm_up=True
    )
    responses = responses_to_traffic_array(
        config,
        traffic_array,
        ResponseType.YTrans,
        points=[Point(x=51, z=-8.4)],
    )
    plt.plot(responses[0])
    plt.show()
