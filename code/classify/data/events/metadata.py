"""Metadata for classify.data.events.Events."""
import itertools
import os
from typing import List, Optional, Tuple, Union

import pandas as pd

from config import Config
from fem.run import FEMRunner
from model import Point
from model.response import ResponseType
from model.scenario import BridgeScenario, TrafficScenario


def file_path(c: Config, series: pd.Series):
    """Return a file path for a row from the Metadata."""
    assert isinstance(series, pd.Series)
    return os.path.join(c.events_dir, (
            series["traffic-scenario"]
            + f"-{series['bridge-name']}"
            + f"-{series['bridge-scenario']}"
            + f"-{series['at']}"
            + f"-{series['response-type']}"
            + f"-{series['fem-runner']}"
            + f"-{series['lane']}"
            + f"-{series['param-sim-num']}"
            + f"-{series['traffic-sim-num']}"
            + f"-{series['num-events']}"))


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
                "traffic-scenario", "bridge-name", "bridge-scenario", "at",
                "response-type", "fem-runner", "lane", "param-sim-num",
                "traffic-sim-num", "num-events"])

    def add_file_path(
            self, traffic_scenario: TrafficScenario,
            bridge_scenario: BridgeScenario, at: Point,
            response_type: ResponseType, fem_runner: FEMRunner, lane: int,
            num_events: int, traffic_sim_num: Optional[int] = None,
            get_sim_num: bool = False) -> Union[str, Tuple[int, int]]:
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
            num_events: int, the number of events from the ran simulation.
            get_sim_num: bool, return a tuple of the next parameter-specific
                simulation index, next traffic simulation index and file path.

        """
        next_param_sim_num, next_traffic_sim_num, df = self.file_paths(
            traffic_scenario=traffic_scenario, bridge_scenario=bridge_scenario,
            at=at, response_type=response_type, fem_runner=fem_runner,
            lane=lane, get_sim_num=True)
        # Use given traffic simulation number if given.
        if traffic_sim_num is not None:
            next_traffic_sim_num = traffic_sim_num
        row = pd.Series({
            "traffic-scenario": traffic_scenario.name,
            "bridge-name": self.c.bridge.name,
            "bridge-scenario": bridge_scenario.name,
            "at": str(at),
            "response-type": response_type.name(),
            "fem-runner": fem_runner.name,
            "lane": lane,
            "param-sim-num": next_param_sim_num,
            "traffic-sim-num": next_traffic_sim_num,
            "num-events": num_events})
        df = df.append(row, ignore_index=True)
        df.to_csv(self.c.event_metadata_path)
        if get_sim_num:
            return (
                next_param_sim_num,
                next_traffic_sim_num,
                file_path(self.c, row))
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
            get_sim_num: bool, return a tuple of the next parameter-specific
                simulation index, next traffic simulation index, and the
                metadata DataFrame.

        """
        df = self.load()
        assert isinstance(df, pd.DataFrame)
        rows = df.loc[
            (df["traffic-scenario"] == traffic_scenario.name)
            & (df["bridge-name"] == self.c.bridge.name)
            & (df["bridge-scenario"] == bridge_scenario.name)
            & (df["at"] == str(at))
            & (df["response-type"] == response_type.name())
            & (df["fem-runner"] == fem_runner.name)
            & (df["lane"] == lane)]
        if get_sim_num:
            param_sim_nums = set(rows["param-sim-num"])
            for maybe_next_param_sim_num in itertools.count(start=0):
                if maybe_next_param_sim_num not in param_sim_nums:
                    next_param_sim_num = maybe_next_param_sim_num
                    break
            traffic_sim_nums = set(df["traffic-sim-num"])
            for maybe_next_traffic_sim_num in itertools.count(start=0):
                if maybe_next_traffic_sim_num not in traffic_sim_nums:
                    return next_param_sim_num, maybe_next_traffic_sim_num, df
        return [
            (file_path(self.c, row), row["num-events"], row["traffic-sim-num"])
            for _, row in rows.iterrows()]
