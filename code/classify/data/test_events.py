"""Test events.py."""
import os
import pickle

import numpy as np

from classify.data.scenarios import normal_traffic
from classify.data.events import Events, events_from_mv_loads
from fem.run.opensees import os_runner
from model.bridge import Point
from model.bridge.bridge_705 import bridge_705_config
from model.load import MovingLoad
from model.response import Event, ResponseType
from model.scenario import BridgeScenarioNormal


def test_events_from_mv_loads():
    c = bridge_705_config()
    mv_loads = [MovingLoad.sample(c=c, x_frac=0, lane=0) for _ in range(2)]
    response_types = [ResponseType.Strain, ResponseType.Stress]
    at = [Point(x=c.bridge.x(x_frac)) for x_frac in np.linspace(0, 1, num=10)]
    events = list(events_from_mv_loads(
        c=c, mv_loads=mv_loads, response_types=response_types,
        fem_runner=os_runner(c), at=at))
    shape = np.array(events).shape
    assert len(shape) == 3
    assert shape[0] == len(at)
    assert shape[1] == len(response_types)
    assert isinstance(events[0][0], list)
    assert isinstance(events[0][0][0], Event)


def test_events_class():
    c = bridge_705_config()
    c.event_metadata_path += ".test"
    events = Events(c)

    # Delete metadata.
    if os.path.exists(c.event_metadata_path):
        os.remove(c.event_metadata_path)

    # Loaded metadata should have no rows and not be saved to file.
    metadata = events.metadata.load()
    assert len(metadata) == 0
    assert not os.path.exists(c.event_metadata_path)

    # Check simulation numbers and length of metadata after adding rows.
    for i in range(10):
        highest_sim_num = events.metadata.add_filepath(
            traffic_scenario=normal_traffic,
            bridge_scenario=BridgeScenarioNormal(), at=Point(x=1),
            response_type=ResponseType.XTranslation, fem_runner=os_runner(c),
            lane=0, highest_sim=True)
        assert highest_sim_num == i + 1
        assert len(events.metadata.load()) == i + 1

    # Create some events, not using the Events class.
    mv_loads = [MovingLoad.sample(c=c, x_frac=0, lane=0) for _ in range(2)]
    some_events = list(events_from_mv_loads(
        c=c, mv_loads=mv_loads, response_types=[ResponseType.Strain],
        fem_runner=os_runner(c), at=[Point(x=1)]))[0][0]

    # Save and load the created events to a file.
    events.save_events(some_events, "./tmp")
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
            traffic_scenario=normal_traffic,
            bridge_scenario=BridgeScenarioNormal(), at=at,
            response_types=response_types, fem_runner=os_runner(c), lane=0,
            num_vehicles=2)
    metadata = events.metadata.load()
    assert len(metadata) == len(at) * len(response_types) * iterations

    # Get the previously made events using the Events class. There should be a
    # list of Event for each iteration of Event.make_events.
    got_events = events.get_events(
        traffic_scenario=normal_traffic,
        bridge_scenario=BridgeScenarioNormal(), at=at[0],
        response_type=response_types[0], fem_runner=os_runner(c), lane=0)
    assert len(np.array(got_events).shape) == 2
    assert len(got_events) == iterations
    assert isinstance(got_events[0][0], Event)
