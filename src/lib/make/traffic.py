import matplotlib.pyplot as plt

from bridge_sim.model import Config, Point, ResponseType, PierSettlement
from bridge_sim.sim.responses import to_traffic_array
from bridge_sim.traffic import normal_traffic
from bridge_sim.plot.animate import animate_traffic as at
from bridge_sim.plot.animate import animate_traffic_array as ata
from bridge_sim.plot.animate import animate_responses as ar


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


def animate_responses(config: Config):
    time = 1
    config.sensor_hz = 1 / 10
    traffic_scenario = normal_traffic(config=config)
    traffic_sequence = traffic_scenario.traffic_sequence(config, time)
    ar(
        config=config,
        traffic_sequence=traffic_sequence,
        response_type=ResponseType.YTrans,
        units="mm",
        save=config.get_image_path("verification/animate", "traffic-responses.mp4"),
        pier_settlement=[(PierSettlement(4, 1.2), PierSettlement(4, 2))],
    )


def plot_responses(config: Config):
    max_time = 10
    traffic_scenario = normal_traffic(config=config, lam=5, min_d=2)
    traffic_sequence = traffic_scenario.traffic_sequence(config, max_time)
    traffic_array = traffic_sequence.traffic_array()
    responses = to_traffic_array(
        config, traffic_array, ResponseType.YTrans, points=[Point(x=51, z=-8.4)],
    )
    plt.plot(responses[0])
    plt.show()
