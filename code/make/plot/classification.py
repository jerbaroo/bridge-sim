import itertools

import numpy as np
from scipy.stats import ks_2samp
from sklearn.svm import OneClassSVM

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import HealthyBridge
from fem.responses import Responses
from fem.run.opensees import OSRunner
from make.plot.distribution import load_normal_traffic_array, pier_disp_scenarios
from model.bridge import Point
from model.response import ResponseType
from plot import plt
from plot.geom import top_view_bridge
from plot.responses import plot_contour_deck
from util import print_i


def oneclass(c: Config):
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)
    bridge_scenarios = [HealthyBridge()] + pier_disp_scenarios(c)
    response_type = ResponseType.YTranslation
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max / 2, 20),
            np.linspace(c.bridge.z_min, c.bridge.z_max / 2, 3),
        )
    ]
    results = []

    for b, bridge_scenario in enumerate(bridge_scenarios):
        print_i(f"One class: bridge scenario {bridge_scenario.name}")
        responses = responses_to_traffic_array(
            c=c,
            traffic_array=normal_traffic_array,
            response_type=response_type,
            bridge_scenario=bridge_scenario,
            points=points,
            fem_runner=OSRunner(c),
        ).T
        print(len(normal_traffic_array))
        print(responses.shape)

        # Fit on the healthy scenario.
        if b == 0:
            assert len(responses) == len(points)
            clfs = []
            for r, rs in enumerate(responses):
                print_i(f"Training classifier {r} / {len(responses)}")
                clfs.append(OneClassSVM().fit(rs.reshape(-1, 1)))

        scenario_results = []
        for p, _ in enumerate(points):
            print_i(f"Predicting points {p} / {len(points)}")
            prediction = clfs[p].predict(responses[p].reshape(-1, 1))
            print(prediction)
            print(len(prediction[prediction < 0]))
            print(len(prediction[prediction > 0]))


def joint_clustering_bridge(c: Config):
    """Compare distribution of pairs of sensors under HealthyScenario."""
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)
    response_type = ResponseType.YTranslation
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 20),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 2),
        )
    ]

    bridge_scenario = HealthyBridge()
    responses = responses_to_traffic_array(
        c=c,
        traffic_array=normal_traffic_array,
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        fem_runner=OSRunner(c),
    ).T
    assert len(responses) == len(points)

    ks_values_healthy = []
    for p0, point0 in enumerate(points):
        print_i(f"Point {p0 + 1} / {len(points)}")
        ks_values_healthy.append([])
        for p1, point1 in enumerate(points):
            ks = ks_2samp(responses[p0], responses[p1])
            ks_values_healthy[-1].append(ks[0])

    plt.landscape()
    plt.imshow(ks_values_healthy)
    plt.savefig(c.get_image_path("joint-clustering", "healthy-bridge"))
    plt.close()

    bridge_scenario = pier_disp_scenarios(c)[0]
    responses = responses_to_traffic_array(
        c=c,
        traffic_array=normal_traffic_array,
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        fem_runner=OSRunner(c),
    ).T
    assert len(responses) == len(points)

    ks_values_damage = []
    for p0, point0 in enumerate(points):
        print_i(f"Point {p0 + 1} / {len(points)}")
        ks_values_damage.append([])
        for p1, point1 in enumerate(points):
            ks = ks_2samp(responses[p0], responses[p1])
            ks_values_damage[-1].append(ks[0])

    plt.imshow(ks_values_damage)
    plt.savefig(c.get_image_path("joint-clustering", "damage-bridge"))
    plt.close()

    ks_values_comp = []
    for p0, point0 in enumerate(points):
        ks_values_comp.append([])
        for p1, point1 in enumerate(points):
            comp = abs(ks_values_healthy[p0][p1] - ks_values_damage[p0][p1])
            ks_values_comp[-1].append(comp)

    plt.landscape()
    plt.imshow(ks_values_comp)
    plt.savefig(c.get_image_path("joint-clustering", "damage-bridge-comp"))
    plt.close()

    responses = Responses.from_responses(
        response_type=response_type,
        responses=[(sum(ks_values_comp[p]), point) for p, point in enumerate(points)],
    )
    top_view_bridge(c.bridge, abutments=True, piers=True)
    plot_contour_deck(c=c, responses=responses)
    plt.savefig(c.get_image_path("joint-clustering", "damage-bridge-comp-contour"))
    plt.close()