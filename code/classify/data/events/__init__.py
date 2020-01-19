"""Generate, save and load events."""
import itertools
import pickle
from typing import Dict, List

import pickletools
import numpy as np
from classify.data.events.metadata import Metadata

from classify.data.recorder import Recorder
from classify.data.responses import responses_to_traffic
from classify.data.trigger import Trigger, always_trigger
from config import Config
from fem.responses import Responses
from fem.run import FEMRunner
from model.bridge import Bridge, Point
from model.load import MvVehicle
from model.response import Event, ResponseType
from model.scenario import DamageScenario, Traffic, TrafficScenario


def events_from_traffic(
    c: Config,
    traffic: Traffic,
    bridge_scenario: DamageScenario,
    points: List[Point],
    response_types: List[ResponseType],
    fem_runner: FEMRunner,
    start_time: float,
    time_step: float,
    trigger: Trigger = always_trigger(),
) -> List[List[List[Event]]]:
    """Return events generated from traffic in a bridge scenario.

    The result has shape (len(points), len(response_types), #events).

    """
    # Construct a Recorder for each sensor position and response type.
    recorders = [
        [
            Recorder(c=c, trigger=trigger, response_type=response_type)
            for response_type in response_types
        ]
        for _ in points
    ]

    shape = np.array(recorders).shape
    assert len(shape) == 2
    assert shape[0] == len(points)
    assert shape[1] == len(response_types)

    # A list of Responses (one per simulation time step) for each response type.
    responses = [
        responses_to_traffic(
            c=c,
            traffic=traffic,
            bridge_scenario=bridge_scenario,
            start_time=start_time,
            time_step=time_step,
            points=points,
            response_type=response_type,
            fem_runner=fem_runner,
        )
        for response_type in response_types
    ]

    assert len(responses) == len(response_types)
    assert len(responses[0]) == len(traffic)
    assert isinstance(responses[0][0], Responses)

    # Events are recorded for each sensor position and response type.
    events = [[[] for _ in response_types] for _ in points]

    # Record the response at each time.
    for t in range(len(traffic)):
        for p, point in enumerate(points):
            for r in range(len(response_types)):
                recorders[p][r].receive(
                    responses[r][t].responses[0][point.x][point.y][point.z]
                )
                maybe_event = recorders[p][r].maybe_event()
                if maybe_event is not None:
                    events[p][r].append(maybe_event)
    return events


def save_events(events: List[Event], events_path: str):
    """Save events for one simulation to the given file path."""
    print(f"saving {len(events)} to {events_path}")
    s = pickletools.optimize(pickle.dumps(events))
    with open(events_path, "wb") as f:
        f.write(s)


class Events:
    """A class for generating, saving and loading events for scenarios."""

    def __init__(self, c: Config):
        self.c = c
        self.metadata = Metadata(self.c)

    def num_events(
        self,
        traffic_scenario: TrafficScenario,
        bridge_scenario: DamageScenario,
        at: Point,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        lane: int,
    ) -> List[int]:
        """Number of events per simulation available for given parameters."""
        return list(
            map(
                lambda x: x[1],
                self.metadata.file_paths(
                    traffic_scenario=traffic_scenario,
                    bridge_scenario=bridge_scenario,
                    at=at,
                    response_type=response_type,
                    fem_runner=fem_runner,
                    lane=lane,
                ),
            )
        )

    def get_events(
        self,
        traffic_scenario: TrafficScenario,
        bridge_scenarios: List[DamageScenario],
        point: Point,
        response_type: ResponseType,
        fem_runner: FEMRunner,
    ) -> Dict[DamageScenario, List[List[Event]]]:
        """Get events from a simulation of a bridge in a scenario.

        Returns a dictionary of DamageScenario to list of list of Event. Each
        inner list of Event is for a separate simulation. The lists for each
        DamageScenario correspond to the same simulations.

        """
        # A dictionary of 'DamageScenario' to list of tuples of, file path and
        # traffic simulation ID.
        events_dict = {
            bridge_scenario: list(
                map(
                    lambda x: [x[0], x[2]],  # Ignore number of events.
                    self.metadata.file_paths(
                        traffic_scenario=traffic_scenario,
                        bridge_scenario=bridge_scenario,
                        point=point,
                        response_type=response_type,
                        fem_runner=fem_runner,
                    ),
                )
            )
            for bridge_scenario in bridge_scenarios
        }
        # Traffic simulation IDs for each DamageScenario.
        traffic_dict = {
            bridge_scenario: set(map(lambda x: x[1], events_dict[bridge_scenario]))
            for bridge_scenario in bridge_scenarios
        }
        # Traffic simulation IDs used in all BridgeScenarios.
        traffic_nums = set(
            t
            for _, ts in traffic_dict.items()
            for t in ts
            if all(t in traffic_dict[bs] for bs in bridge_scenarios)
        )

        def load_events(events_file_path):
            with open(events_file_path, "rb") as f:
                return pickle.load(f)

        result = {
            bridge_scenario: [
                load_events(fp) for fp, t in file_paths if t in traffic_nums
            ]
            for bridge_scenario, file_paths in events_dict.items()
        }

        # Some assertions.
        _lists = [l for _, l in result.items()]
        if len(_lists) >= 1:
            for i in range(len(_lists)):
                assert len(_lists[i]) == len(_lists[0])
                for j in range(len(_lists[0])):
                    assert len(_lists[i][j]) == len(_lists[0][j])

        return result

    def make_events(
        self,
        bridge: Bridge,
        traffic_scenario: TrafficScenario,
        bridge_scenarios: List[DamageScenario],
        points: List[Point],
        response_types: List[ResponseType],
        fem_runner: FEMRunner,
        max_time: float,
        time_step: float,
    ):
        """Make events in one traffic scenario for many bridge scenarios.

        Args:
            bridge: Bridge, bridge on which traffic drives one.
            traffic_scenario: TrafficScenario, scenario of the traffic.
            bridge_scenarios: List[DamageScenario], bridge damage scenarios.
            points: List[Point], points at which to record responses.
            response_types: List[ResponseType], type of responses to record.
            fem_runner: FEMRunner, FE program to run simulations with.
            max_time: float, maximum time of the traffic simulation.
            time_step: time_step, time step of the traffic simulation.

        """
        # All events created will be run under the same traffic simulation and
        # have the same traffic simulation ID.
        traffic, start_index = traffic_scenario.traffic(
            bridge=bridge, max_time=max_time, time_step=time_step
        )
        print(len(traffic))
        traffic = traffic[start_index:]
        traffic_sim_id = None

        for bridge_scenario in bridge_scenarios:
            # Generate events under the traffic and bridge scenario.
            events = events_from_traffic(
                c=self.c,
                traffic=traffic,
                bridge_scenario=bridge_scenario,
                start_time=start_index * time_step,
                time_step=time_step,
                points=points,
                response_types=response_types,
                fem_runner=fem_runner,
            )

            # For each point and sensor type, save the events to disk.
            for p, r in itertools.product(
                range(len(points)), range(len(response_types))
            ):
                print(p, r)
                # Here we first update the metadata (record of where events are
                # saved), and then save events to disk at the specified path.
                # 'traffic_sim_id' will be assigned in the first iteration,
                # passed to 'add_file_path' in each subsequent iteration.
                _, traffic_sim_id, events_path = self.metadata.add_file_path(
                    traffic_scenario=traffic_scenario,
                    bridge_scenario=bridge_scenario,
                    point=points[p],
                    response_type=response_types[r],
                    fem_runner=fem_runner,
                    num_events=len(events[p][r]),
                    traffic_sim_id=traffic_sim_id,
                    get_sim_id=True,
                )
                save_events(events=events[p][r], events_path=events_path)
