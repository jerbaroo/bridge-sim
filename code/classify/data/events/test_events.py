"""Test events.py."""
import os
import pickle

import numpy as np

from classify.data.scenarios import (
    BridgeScenarioDisplacementCtrl,
    BridgeScenarioNormal,
    normal_traffic,
)
from classify.data.events import Events, events_from_mv_vehicles, save_events
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_3d, bridge_705_test_config
from model.load import PierSettlement, MvVehicle
from model.response import Event, ResponseType

c = bridge_705_test_config(bridge_705_3d)
c.il_num_loads = 10


def test_events_from_mv_vehicles():
    mv_vehicles_gen = normal_traffic(c).mv_vehicles(lane=0)
    mv_vehicles = [next(mv_vehicles_gen) for _ in range(2)]
    response_types = [ResponseType.YTranslation]
    at = [Point(x=c.bridge.x(x_frac)) for x_frac in np.linspace(0, 1, num=10)]
    events = list(
        events_from_mv_vehicles(
            c=c,
            mv_vehicles=mv_vehicles,
            bridge_scenario=None,
            response_types=response_types,
            fem_runner=OSRunner(c),
            at=at,
        )
    )
    shape = np.array(events).shape
    assert len(shape) == 3
    assert shape[0] == len(at)
    assert shape[1] == len(response_types)
    assert isinstance(events[0][0], list)
    assert isinstance(events[0][0][0], Event)


def test_events_class():
    events = Events(c)
    lane = 0
    num_vehicles = 2

    # Delete metadata.
    if os.path.exists(c.event_metadata_path):
        os.remove(c.event_metadata_path)

    # Loaded metadata should have no rows and not be saved to file.
    metadata = events.metadata.load()
    assert len(metadata) == 0
    assert not os.path.exists(c.event_metadata_path)

    # Check simulation numbers and length of metadata after adding rows.
    for i in range(10):
        (
            next_param_sim_num,
            next_traffic_sim_num,
            _file_path,
        ) = events.metadata.add_file_path(
            traffic_scenario=normal_traffic(c),
            bridge_scenario=BridgeScenarioNormal(),
            at=Point(x=1),
            response_type=ResponseType.XTranslation,
            fem_runner=OSRunner(c),
            lane=lane,
            num_events=0,
            get_sim_num=True,
        )
        assert next_param_sim_num == i
        assert next_traffic_sim_num == i
        assert len(events.metadata.load()) == i + 1

    # Create some events, not using the Events class.
    mv_vehicles_gen = normal_traffic(c).mv_vehicles(lane=lane)
    mv_vehicles = [next(mv_vehicles_gen) for _ in range(2)]
    some_events = list(
        events_from_mv_vehicles(
            c=c,
            mv_vehicles=mv_vehicles,
            bridge_scenario=None,
            response_types=[ResponseType.YTranslation],
            fem_runner=OSRunner(c),
            at=[Point(x=1)],
        )
    )[0][0]

    # Save and load the created events to a file.
    save_events(some_events, "./tmp")
    with open("./tmp", "rb") as f:
        some_loaded_events = pickle.load(f)
    assert len(some_loaded_events) == len(some_events)

    # Delete metadata.
    if os.path.exists(c.event_metadata_path):
        os.remove(c.event_metadata_path)

    # Make events using the Events.make_events method.
    at = [Point(x=1, y=0, z=0), Point(x=10, y=0, z=0)]
    response_types = [ResponseType.XTranslation, ResponseType.YTranslation]
    iterations = 3
    for _ in range(iterations):
        events.make_events(
            traffic_scenario=normal_traffic(c),
            bridge_scenarios=[BridgeScenarioNormal()],
            at=at,
            response_types=response_types,
            fem_runner=OSRunner(c),
            lane=lane,
            num_vehicles=num_vehicles,
        )
    metadata = events.metadata.load()
    assert len(metadata) == len(at) * len(response_types) * iterations
    for i in range(iterations):
        assert len([x for x in list(metadata["param-sim-num"]) if x == i]) == len(
            at
        ) * len(response_types)

    # Test events.num_events.
    for a in range(len(at)):
        for r in range(len(response_types)):
            num_events = events.num_events(
                traffic_scenario=normal_traffic(c),
                bridge_scenario=BridgeScenarioNormal(),
                at=at[a],
                response_type=response_types[r],
                fem_runner=OSRunner(c),
                lane=lane,
            )
            assert isinstance(num_events, list)
            assert len(num_events) == iterations

    # Get the previously made events using the Events class. There should be a
    # list of Event for each iteration of Event.make_events.
    got_events = events.get_events(
        traffic_scenario=normal_traffic(c),
        bridge_scenarios=[BridgeScenarioNormal()],
        at=at[0],
        response_type=response_types[0],
        fem_runner=OSRunner(c),
        lane=lane,
    )
    assert isinstance(got_events, dict)
    for _, list_of_list_of_event in got_events.items():
        assert len(list_of_list_of_event) == iterations
        assert isinstance(list_of_list_of_event, list)
        assert isinstance(list_of_list_of_event[0], list)
        assert isinstance(list_of_list_of_event[0][0], Event)

    # Test different bridge scenarios.
    assert len(set(events.metadata.load()["bridge-scenario"])) == 1
    events.make_events(
        traffic_scenario=normal_traffic(c),
        bridge_scenarios=[
            BridgeScenarioDisplacementCtrl(
                displacement_ctrl=PierSettlement(displacement=0.1, pier=1)
            )
        ],
        at=at,
        response_types=response_types,
        fem_runner=OSRunner(c),
        lane=lane,
        num_vehicles=num_vehicles,
    )
    assert len(set(events.metadata.load()["bridge-scenario"])) == 2
    assert "displacement-0.1m-pier-1" in set(events.metadata.load()["bridge-scenario"])
    print(events.metadata.load())
