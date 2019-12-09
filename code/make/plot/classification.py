import itertools

import numpy as np
from sklearn.svm import OneClassSVM

from config import Config
from classify.data.responses import responses_to_traffic_array
from classify.scenario.bridge import HealthyBridge
from fem.run.opensees import OSRunner
from make.plot.distribution import load_normal_traffic_array, pier_disp_scenarios
from model.bridge import Point
from model.response import ResponseType
from util import print_i


def oneclass(c: Config):
    normal_traffic_array, traffic_scenario = load_normal_traffic_array(c)
    bridge_scenarios = [HealthyBridge()] + pier_disp_scenarios(c)
    response_type = ResponseType.YTranslation
    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max / 2, 1),
            np.linspace(c.bridge.z_min, c.bridge.z_max / 2, 1),
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
        )
        # Fit on the healthy scenario.
        if b == 0:
            assert len(responses) == len(points)
            clfs = [OneClassSVM().fit(rs) for rs in responses]
        scenario_results = []
        for p, _ in enumerate(points):
            prediction = clfs[p].predict(responses[p])
            print(prediction)
            print(len(prediction[prediction < 0]))
            print(len(prediction[prediction > 0]))
