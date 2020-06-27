from typing import List

import matplotlib.pyplot as plt
import numpy as np

from bridge_sim import crack, sim, traffic
from bridge_sim.model import Config, Point, ResponseType, Vehicle
from bridge_sim.util import flatten, print_i, print_w


def plot_crack_detection(config: Config, crack_x: float, length: float, healthy: bool):
    response_type = ResponseType.YTrans
    og_config = config
    if not healthy:
        config = crack.transverse_crack(length=length, at_x=crack_x).crack(config)
    ts, tr, ta = traffic.load_traffic(config, traffic.normal_traffic(config), time=60)

    # Calculate positions of sensors.
    support_xs = sorted(set((s.x for s in config.bridge.supports)))
    print_i(f"Support xs = {support_xs}")
    x_delta = 1
    mid0 = ((support_xs[0] + support_xs[1]) / 2) + x_delta
    mid1 = ((support_xs[-1] + support_xs[-2]) / 2) + x_delta
    point_0, point_1 = Point(x=mid0, z=-8.4), Point(x=mid1, z=-8.4)
    print(f"X positions = {mid0}, {mid1}")

    ##########################
    # Testing the positions. #
    ##########################

    # rs = sim.responses.load(
    #     config=config,
    #     response_type=response_type,
    #     point_loads=[PointLoad(x=mid0, z=-8.4, load=100), PointLoad(x=mid1, z=-8.4, load=100)],
    # )
    # plot.contour_responses(config, rs)
    # plot.top_view_bridge(config.bridge, piers=True)
    # plt.show()

    # Collect responses at times that vehicles cross sensors.
    vehicles: List[Vehicle] = [
        v for v in flatten(ts.vehicles_per_lane, Vehicle) if v.lane == 0
    ]
    print_i(f"Amount of vehicles = {len(vehicles)}")
    responses_0, responses_1 = [], []
    responses = sim.responses.to_traffic_array(
        config=config,
        traffic_array=ta,
        response_type=response_type,
        points=[point_0, point_1],
    )
    max_i = len(responses[0]) - 1
    total_time = np.round(ts.final_time - ts.start_time, 6)
    print_i(
        f"Total time, sensor_f, responses.shape = {total_time}, {config.sensor_freq}, {responses.shape}"
    )
    for v in vehicles:
        time_0, time_1 = v.time_at(mid0, config.bridge), v.time_at(mid1, config.bridge)
        print_i(f"Times = {time_0}, {time_1}")
        index_0 = int((time_0 - ts.start_time) // config.sensor_freq)
        index_1 = int((time_1 - ts.start_time) // config.sensor_freq)
        print_i(f"Indices = {index_0}, {index_1}")
        if 0 <= index_0 <= max_i and 0 <= index_1 <= max_i:
            responses_0.append(responses[0][index_0])
            responses_1.append(responses[1][index_1])
            print(responses_0[-1], responses_1[-1])
    responses_0 = np.array(responses_0)
    responses_1 = np.array(responses_1)
    plt.plot(responses_0)
    plt.plot(responses_1)
    plt.savefig(og_config.get_image_path("classify/crack", f"delta-{healthy}.pdf"))
    plt.close()
