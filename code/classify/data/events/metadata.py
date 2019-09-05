"""Metadata for classify.data.events.Events."""
import itertools
import os
from typing import Union, List, Tuple

import pandas as pd

from config import Config
from fem.run import FEMRunner
from model import Point
from model.response import ResponseType
from model.scenario import BridgeScenario, TrafficScenario


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


class Metadata:
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
