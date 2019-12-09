"""Classify events."""

from plot import plt

from classify.data.events import Events
from classify.data.scenarios import (
    BridgeScenarioDisplacementCtrl,
    BridgeScenarioNormal,
    normal_traffic,
)
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_debug_config
from model.load import DisplacementCtrl
from model.response import ResponseType


if __name__ == "__main__":
    c = bridge_705_debug_config(bridge_705_3d)
    events = Events(c)
    point = Point(x=35, y=0, z=8.4)
    traffic_scenario = normal_traffic(c, 5, 2)
    bridge_scenarios = [BridgeScenarioNormal()]
    # BridgeScenarioDisplacementCtrl(DisplacementCtrl(
    #     displacement=0.1, pier=1))]
    response_type = ResponseType.YTranslation
    fem_runner = OSRunner(c)

    # Each time this script is run, make some more events.
    events_per_bridge = events.make_events(
        bridge=c.bridge,
        traffic_scenario=traffic_scenario,
        bridge_scenarios=bridge_scenarios,
        points=[point],
        response_types=[response_type],
        fem_runner=fem_runner,
        max_time=10,
        time_step=c.time_step,
    )

    # Get events for each bridge scenario.
    events_per_bridge_scenario = events.get_events(
        traffic_scenario=traffic_scenario,
        bridge_scenarios=bridge_scenarios,
        point=point,
        response_type=response_type,
        fem_runner=fem_runner,
    )

    # # Plot corresponding events for each scenario.
    for i, (bridge_scenario, b_events) in enumerate(events_per_bridge_scenario.items()):
        for t, events in enumerate(b_events):
            for e, event in enumerate(events):
                plt.close()
                plt.plot(event.get_time_series(noise=False))
                plt.title(bridge_scenario.name)
                plt.savefig(f"test-image-{i}-{t}-{e}")
