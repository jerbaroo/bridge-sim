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
    return os.path.join(
        c.events_dir,
        (
            series["traffic-scenario"]
            + f"-{series['bridge-name']}"
            + f"-{series['bridge-scenario']}"
            + f"-{series['point']}"
            + f"-{series['response-type']}"
            + f"-{series['fem-runner']}"
            + f"-{series['param-sim-id']}"
            + f"-{series['traffic-sim-id']}"
            + f"-{series['num-events']}"
        ),
    )


class Metadata:
    """Metadata about stored events."""

    def __init__(self, c: Config):
        self.c = c

    def load(self) -> pd.DataFrame:
        """Return the metadata loaded from disk."""
        if os.path.exists(self.c.event_metadata_path):
            return pd.read_csv(self.c.event_metadata_path, index_col=0)
        else:
            return pd.DataFrame(
                columns=[
                    "traffic-scenario",
                    "bridge-name",
                    "bridge-scenario",
                    "point",
                    "response-type",
                    "fem-runner",
                    "param-sim-id",
                    "traffic-sim-id",
                    "num-events",
                ]
            )

    def add_file_path(
        self,
        traffic_scenario: TrafficScenario,
        bridge_scenario: BridgeScenario,
        point: Point,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        num_events: int,
        traffic_sim_id: Optional[int] = None,
        get_sim_id: bool = False,
    ) -> Union[str, Tuple[int, int, str]]:
        """Add and return a file path to the metadata for given parameters.

        Args:
            traffic_scenario: TrafficScenario, traffic scenario on the bridge.
            bridge_scenario: BridgeScenario: scenario of damage to the bridge.
            point: Point, sensor position at which events are recorded.
            response_type: ResponseType, sensor type of recorded events.
            fem_runner: FEMRunner, FE program used to simulate events.
            num_events: int, number of events recorded in the simulation.
            get_sim_id: bool, return a tuple of the next parameter-specific
                simulation index, next traffic simulation index and the file
                path where the events should be saved to disk.

        """
        next_param_sim_id, next_traffic_sim_id, df = self.file_paths(
            traffic_scenario=traffic_scenario,
            bridge_scenario=bridge_scenario,
            point=point,
            response_type=response_type,
            fem_runner=fem_runner,
            get_sim_id=True,
        )
        # Use given traffic simulation ID if given.
        if traffic_sim_id is not None:
            next_traffic_sim_id = traffic_sim_id
        row = pd.Series(
            {
                "traffic-scenario": traffic_scenario.name,
                "bridge-name": self.c.bridge.name,
                "bridge-scenario": bridge_scenario.name,
                "point": str(point),
                "response-type": response_type.name(),
                "fem-runner": fem_runner.name,
                "param-sim-id": next_param_sim_id,
                "traffic-sim-id": next_traffic_sim_id,
                "num-events": num_events,
            }
        )
        df = df.append(row, ignore_index=True)
        df.to_csv(self.c.event_metadata_path)
        if get_sim_id:
            return (
                next_param_sim_id,
                next_traffic_sim_id,
                file_path(self.c, row),
            )
        return file_path(self.c, row)

    def file_paths(
        self,
        traffic_scenario: TrafficScenario,
        bridge_scenario: BridgeScenario,
        point: Point,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        get_sim_id: bool = False,
    ) -> Union[List[Tuple[str, int, int]], Tuple[int, int, pd.DataFrame]]:
        """File paths, number of events, and traffic IDs for given parameters.

        Args:
            traffic_scenario: TrafficScenario, traffic scenario on the bridge.
            bridge_scenario: BridgeScenario: scenario of damage to the bridge.
            point: Point, the sensor position at which events are recorded.
            response_type: ResponseType, the sensor type of recorded events.
            fem_runner: FEMRunner, the FE program used to simulate events.
            lane: int, the index of the lane on which traffic is driven.
            get_sim_id: bool, return a tuple of the next parameter-specific
                simulation ID, next traffic simulation ID, and the metadata
                DataFrame.

        """
        df = self.load()
        assert isinstance(df, pd.DataFrame)
        rows = df.loc[
            (df["traffic-scenario"] == traffic_scenario.name)
            & (df["bridge-name"] == self.c.bridge.name)
            & (df["bridge-scenario"] == bridge_scenario.name)
            & (df["point"] == str(point))
            & (df["response-type"] == response_type.name())
            & (df["fem-runner"] == fem_runner.name)
        ]
        if get_sim_id:
            param_sim_ids = set(rows["param-sim-id"])
            for maybe_next_param_sim_id in itertools.count(start=0):
                if maybe_next_param_sim_id not in param_sim_ids:
                    next_param_sim_id = maybe_next_param_sim_id
                    break
            traffic_sim_ids = set(df["traffic-sim-id"])
            for maybe_next_traffic_sim_id in itertools.count(start=0):
                if maybe_next_traffic_sim_id not in traffic_sim_ids:
                    return next_param_sim_id, maybe_next_traffic_sim_id, df
        return [
            (file_path(self.c, row), row["num-events"], row["traffic-sim-id"])
            for _, row in rows.iterrows()
        ]
