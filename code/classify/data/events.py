"""Generate, save and load events."""
import itertools
import os
import pickle
from typing import List, Tuple, Union

import pandas as pd
import pickletools
import numpy as np

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
        c: Config, mv_loads: List[MovingLoad],
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


def file_path(c: Config, series: pd.Series):
    """Return a file path for a row from the _MetaData."""
    assert isinstance(series, pd.Series)
    return os.path.join(c.events_dir, (
        series["traffic-scenario"]
        + f"-{series['bridge-scenario']}"
        + f"-{series['at']}"
        + f"-{series['response-type']}"
        + f"-{series['fem-runner']}"
        + f"-{series['lane']}"
        + f"-{series['simulation']}"))


class _MetaData:
    """Metadata about stored events."""
    def __init__(self, c: Config):
        self.c = c

    def load(self) -> pd.DataFrame:
        """Return the metadata loaded from a file."""
        if os.path.exists(self.c.event_metadata_path):
            return pd.read_csv(self.c.event_metadata_path, index_col=0)
        else:
            return pd.DataFrame(columns=[
                "traffic-scenario", "bridge-scenario", "at",
                "response-type", "fem-runner", "lane", "simulation",
                "num-events"])

    def add_file_path(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int,
            num_events: int, get_sim_num: bool = False) -> Union[str, int]:
        """Add and return a file path to the metadata for given parameters.

        Args:
            traffic_scenario: TrafficScenario, the traffic scenario under which
                events are generated.
            bridge_scenario: BridgeScenario: the bridge scenario under which
                events are generated.
            at: Point, the sensor position at which events are recorded.
            response_type: ResponseType, the sensor type of recorded events.
            fem_runner: FEMRunner, the FE program used to simulate events.
            lane: int, the index of the lane on which traffic is driven.
            num_events: int, the the number of events from the simulation.
            get_sim_num: bool, if True return the next available simulation
                index instead of the file path that was added.

        """
        next_sim_num, df = self.file_paths(
            traffic_scenario=traffic_scenario, bridge_scenario=bridge_scenario,
            at=at, response_type=response_type, fem_runner=fem_runner,
            lane=lane, get_sim_num=True)
        row = pd.Series({
            "traffic-scenario": traffic_scenario.name,
            "bridge-scenario": bridge_scenario.name,
            "at": str(at),
            "response-type": response_type.name(),
            "fem-runner": fem_runner.name,
            "lane": lane,
            "simulation": next_sim_num,
            "num-events": num_events})
        df = df.append(row, ignore_index=True)
        df.to_csv(self.c.event_metadata_path)
        if get_sim_num:
            return next_sim_num
        return file_path(self.c, row)

    def file_paths(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int,
            get_sim_num: bool = False
            ) -> Union[List[Tuple[str, int]], Tuple[int, pd.DataFrame]]:
        """The file paths and number of events for given simulation parameters.

        Args:
            traffic_scenario: TrafficScenario, the traffic scenario under which
                events are generated.
            bridge_scenario: BridgeScenario: the bridge scenario under which
                events are generated.
            at: Point, the sensor position at which events are recorded.
            response_type: ResponseType, the sensor type of recorded events.
            fem_runner: FEMRunner, the FE program used to simulate events.
            lane: int, the index of the lane on which traffic is driven.
            get_sim_num: bool, if True instead return a tuple of, the next
                available simulation index, and the metadata DataFrame.

        """
        df = self.load()
        assert isinstance(df, pd.DataFrame)
        rows = df.loc[
            (df["traffic-scenario"] == traffic_scenario.name)
            & (df["bridge-scenario"] == bridge_scenario.name)
            & (df["at"] == str(at))
            & (df["response-type"] == response_type.name())
            & (df["fem-runner"] == fem_runner.name)
            & (df["lane"] == lane)]
        if get_sim_num:
            for sim_num in itertools.count(start=0):
                if sim_num not in set(rows["simulation"]):
                    return sim_num, df
        return [(file_path(self.c, row), row["num-events"])
                for _, row in rows.iterrows()]


def save_events(events: List[Event], events_file_path: str):
    """Save events for one simulation to the given file path."""
    s = pickletools.optimize(pickle.dumps(events))
    with open(events_file_path, "wb") as f:
        f.write(s)


class Events:
    """A class for generating, saving and loading events for scenarios."""
    def __init__(self, c: Config):
        self.c = c
        self.metadata = _MetaData(self.c)

    def num_events(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int,
            ) -> List[int]:
        """Number of events per simulation available for given parameters."""
        return list(map(lambda x: x[0], self.metadata.file_paths(
            traffic_scenario=traffic_scenario, bridge_scenario=bridge_scenario,
            at=at, response_type=response_type, fem_runner=fem_runner,
            lane=lane)))

    def get_events(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int
            ) -> List[List[Event]]:
        """Get events from a simulation of a bridge in a scenario.

        Returns a list of list of Event. Each inner list of Event is for a
        separate simulation.

        """
        events_file_paths = self.metadata.file_paths(
            traffic_scenario=traffic_scenario, bridge_scenario=bridge_scenario,
            at=at, response_type=response_type, fem_runner=fem_runner,
            lane=lane)

        def load_events(events_file_path):
            with open(events_file_path, "rb") as f:
                return pickle.load(f)

        return [load_events(events_file_path)
                for events_file_path, _ in events_file_paths]

    def make_events(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: List[Point],
            response_types: List[ResponseType], fem_runner: FEMRunner,
            lane: int, num_vehicles: int):
        """Make events from a simulation of a bridge in a scenario."""
        mv_loads = [
            MovingLoad.from_vehicle(
                x_frac=0, vehicle=traffic_scenario.vehicle(self.c), lane=lane)
            for _ in range(num_vehicles)]
        events = events_from_mv_loads(
            c=self.c, mv_loads=mv_loads, response_types=response_types,
            fem_runner=fem_runner, at=at)
        for a in range(len(at)):
            for r in range(len(response_types)):
                events_file_path = self.metadata.add_file_path(
                    traffic_scenario=traffic_scenario,
                    bridge_scenario=bridge_scenario, at=at[a],
                    response_type=response_types[r], fem_runner=fem_runner,
                    lane=lane, num_events=len(events[a][r]))
                save_events(
                    events=events[a][r], events_file_path=events_file_path)
