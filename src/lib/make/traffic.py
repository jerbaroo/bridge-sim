import matplotlib.pyplot as plt

from bridge_sim.model import Config, Point, ResponseType
from bridge_sim.sim.responses import responses_to_traffic_array
from bridge_sim.traffic import normal_traffic
from lib.plot.animate import animate_traffic as at
from lib.plot.animate import animate_traffic_array as ata


def animate_traffic(config: Config):
    time = 10
    config.sensor_hz = 1 / 10
    traffic_scenario = normal_traffic(config=config)
    traffic_sequence = traffic_scenario.traffic_sequence(config, time)
    traffic = traffic_sequence.traffic()
    at(
        config=config,
        traffic_sequence=traffic_sequence,
        traffic=traffic,
        save=config.get_image_path("verification/animate", "traffic.mp4"),
    )
    traffic_array = traffic_sequence.traffic_array()
    ata(
        config=config,
        traffic_sequence=traffic_sequence,
        traffic_array=traffic_array,
        save=config.get_image_path("verification/animate", "traffic_array.mp4"),
    )


def plot_responses(config: Config):
    max_time = 10
    traffic_scenario = normal_traffic(config=config, lam=5, min_d=2)
    traffic_sequence = traffic_scenario.traffic_sequence(config, max_time)
    traffic_array = traffic_sequence.traffic_array()
    responses = responses_to_traffic_array(
        config, traffic_array, ResponseType.YTrans, points=[Point(x=51, z=-8.4)],
    )
    plt.plot(responses[0])
    plt.show()
