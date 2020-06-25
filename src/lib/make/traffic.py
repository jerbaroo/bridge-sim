import matplotlib.pyplot as plt
from bridge_sim import temperature

from bridge_sim.model import Config, Point, ResponseType, PierSettlement
from bridge_sim.sim.responses import to_traffic_array
from bridge_sim.traffic import normal_traffic
from bridge_sim.plot.animate import animate_traffic as at
from bridge_sim.plot.animate import animate_traffic_array as ata
from bridge_sim.plot.animate import animate_responses as ar


def animate_traffic(config: Config):
    time = 10
    config.sensor_freq = 1 / 10
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
    time = 60
    config.sensor_freq = 1 / 10  # 10 samples per second.
    traffic_scenario = normal_traffic(config=config)
    traffic_sequence = traffic_scenario.traffic_sequence(config, time)
    weather = temperature.load("holly-springs")
    weather["temp"] = temperature.resize(weather["temp"], year=2019)
    ps = PierSettlement(4, 1.2 / 1e3)
    ar(
        config=config,
        traffic_sequence=traffic_sequence,
        response_type=ResponseType.YTrans,
        units="mm",
        save=config.get_image_path("verification/animate", "traffic-responses.mp4"),
        with_creep=True,
        pier_settlement=[(ps, ps)],
        weather=weather,
        start_date="01/05/2019 00:00",
        end_date="02/05/2019 00:00",
        install_day=37,
        start_day=366 * 10,
        end_day=366 * 10 + 1,
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
