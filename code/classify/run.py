"""Classify events."""

from plot import plt

from classify.data.events import Events
from classify.data.scenarios import BridgeScenarioDisplacementCtrl, BridgeScenarioNormal, normal_traffic
from fem.run.opensees import os_runner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_config
from model.load import DisplacementCtrl
from model.response import ResponseType


if __name__ == "__main__":
    c = bridge_705_config()
    events = Events(c=c)
    point = Point(x=0.1, y=1, z=0)
    bridge_scenarios=[
        BridgeScenarioNormal(),
        BridgeScenarioDisplacementCtrl(
            displacement_ctrl=DisplacementCtrl(displacement=0.1, pier=1))]
    response_type = ResponseType.XTranslation
    fem_runner = os_runner(c)
    lane = 0
    num_vehicles = 5

    # Each time make some more events.
    events_per_bridge = events.make_events(
        traffic_scenario=normal_traffic,
        bridge_scenarios=bridge_scenarios, at=[point],
        response_types=[response_type], fem_runner=fem_runner, lane=lane,
        num_vehicles=num_vehicles)

    # Get events for each bridge scenario.
    events_per_bridge_scenario = events.get_events(
        traffic_scenario=normal_traffic,
        bridge_scenarios=bridge_scenarios, at=point,
        response_type=response_type, fem_runner=fem_runner, lane=lane)

    # Plot corresponding events for each scenario.
    for i, (bridge_scenario, b_events) in enumerate(events_per_bridge_scenario.items()):
        plt.close()
        plt.plot(b_events[0][0].get_time_series(noise=False))
        plt.title(bridge_scenario.name)
        plt.savefig(f"test-image-{i}")
