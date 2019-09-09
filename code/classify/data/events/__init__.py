"""Generate, save and load events."""
import pickle
from typing import Dict, List

import pickletools
import numpy as np
from classify.data.events.metadata import Metadata

from classify.data.recorder import Recorder
from classify.data.responses import responses_to_mv_loads
from classify.data.trigger import Trigger, always_trigger
from config import Config
from fem.run import FEMRunner
from model.bridge import Point
from model.load import MovingLoad
from model.response import Event, ResponseType
from model.scenario import BridgeScenario, TrafficScenario


def events_from_mv_loads(
        c: Config, mv_loads: List[MovingLoad], bridge_scenario: BridgeScenario,
        response_types: List[ResponseType], fem_runner: FEMRunner,
        at: List[Point], per_axle: bool = False,
        trigger: Trigger = always_trigger()) -> List[List[List[Event]]]:
    """Return events generated from moving loads.

    Each yielded result is of shape (len(at), len(response_type), #events), a
    list of Event for each sensor position and response type.

    """
    # Collect responses for each sensor position and response type.
    responses = responses_to_mv_loads(
        c=c, mv_loads=mv_loads, response_types=response_types,
        fem_runner=fem_runner, at=at, per_axle=per_axle)

    shape = np.array(responses).shape
    assert len(shape) == 3
    assert shape[1] == len(at)
    assert shape[2] == len(response_types)

    # Construct a Recorder for each sensor position and response type.
    recorders = [
        [Recorder(c=c, trigger=trigger, response_type=response_type)
         for response_type in response_types]
        for _ in range(len(at))]

    shape = np.array(recorders).shape
    assert len(shape) == 2
    assert shape[0] == len(at)
    assert shape[1] == len(response_types)

    # Events are collected for each sensor position and response type.
    events = [
        [[] for _r in range(len(response_types))]
        for _a in range(len(at))]

    # Record the response at each time.
    for response in responses:
        for a in range(len(at)):
            for r in range(len(response_types)):
                recorders[a][r].receive(response[a][r])
                maybe_event = recorders[a][r].maybe_event()
                if maybe_event is not None:
                    events[a][r].append(maybe_event)
    return events


def save_events(events: List[Event], events_file_path: str):
    """Save events for one simulation to the given file path."""
    s = pickletools.optimize(pickle.dumps(events))
    with open(events_file_path, "wb") as f:
        f.write(s)


class Events:
    """A class for generating, saving and loading events for scenarios."""
    def __init__(self, c: Config):
        self.c = c
        self.metadata = Metadata(self.c)

    def num_events(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int
            ) -> List[int]:
        """Number of events per simulation available for given parameters."""
        return list(map(lambda x: x[1], self.metadata.file_paths(
            traffic_scenario=traffic_scenario, bridge_scenario=bridge_scenario,
            at=at, response_type=response_type, fem_runner=fem_runner,
            lane=lane)))

    def get_events(
            self, traffic_scenario: TrafficScenario,
            bridge_scenarios: List[BridgeScenario], at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int
            ) -> Dict[BridgeScenario, List[List[Event]]]:
        """Get events from a simulation of a bridge in a scenario.

        Returns a dictionary of BridgeScenario to list of list of Event. Each
        inner list of Event is for a separate simulation. The lists for each
        BridgeScenario correspond to the same simulations.

        """
        # A list of tuples of file path and traffic simulation number, for each
        # BridgeScenario.
        events_dict = {
            bridge_scenario: list(map(
                lambda x: [x[0], x[2]],  # Ignore number of events.
                self.metadata.file_paths(
                    traffic_scenario=traffic_scenario,
                    bridge_scenario=bridge_scenario, at=at,
                    response_type=response_type, fem_runner=fem_runner,
                    lane=lane)))
            for bridge_scenario in bridge_scenarios
        }
        # Traffic simulation numbers for each BridgeScenario.
        traffic_dict = {
            bridge_scenario: set(map(
                lambda x: x[1], events_dict[bridge_scenario]))
            for bridge_scenario in bridge_scenarios
        }
        # Traffic simulation numbers used in all BridgeScenarios.
        traffic_nums = set(
            t for _, ts in traffic_dict.items() for t in ts
            if all(t in traffic_dict[bs] for bs in bridge_scenarios))

        def load_events(events_file_path):
            with open(events_file_path, "rb") as f:
                return pickle.load(f)

        return {
            bridge_scenario: [
                load_events(fp) for fp, t in file_paths if t in traffic_nums]
            for bridge_scenario, file_paths in events_dict.items()}

    def make_events(
            self, traffic_scenario: TrafficScenario,
            bridge_scenarios: List[BridgeScenario], at: List[Point],
            response_types: List[ResponseType], fem_runner: FEMRunner,
            lane: int, num_vehicles: int):
        """Make events via bridge simulation under different scenarios."""
        # Construct traffic under the traffic scenario.
        mv_loads = [
            MovingLoad.from_vehicle(
                x_frac=0, vehicle=traffic_scenario.vehicle(self.c), lane=lane)
            for _ in range(num_vehicles)]

        # Save events for each bridge scenario under the same traffic index.
        traffic_sim_num = None
        for bridge_scenario in bridge_scenarios:
            events = events_from_mv_loads(
                c=self.c, mv_loads=mv_loads, bridge_scenario=bridge_scenario,
                at=at, response_types=response_types, fem_runner=fem_runner)
            for a in range(len(at)):
                for r in range(len(response_types)):
                    # traffic_sim_num will be assigned, and the subsequently
                    # non-None value passed in to add_file_path each time.
                    _, traffic_sim_num, events_file_path = (
                        self.metadata.add_file_path(
                            traffic_scenario=traffic_scenario,
                            bridge_scenario=bridge_scenario, at=at[a],
                            response_type=response_types[r],
                            fem_runner=fem_runner,
                            lane=lane, num_events=len(events[a][r]),
                            traffic_sim_num=traffic_sim_num, get_sim_num=True))
                    save_events(
                        events=events[a][r], events_file_path=events_file_path)

