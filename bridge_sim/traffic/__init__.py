"""Generate time series of traffic."""

import os
from typing import NewType, List, Tuple, Callable, Optional

import dill
import numpy as np
from bridge_sim.vehicles.sample import sample_vehicle

from bridge_sim.model import Config, Vehicle
from bridge_sim.util import print_i, st, safe_str, flatten


class TrafficScenario:
    def __init__(self, name: str, mv_vehicle_f: Callable[[], Vehicle]):
        """A named traffic scenario that generates moving vehicles.

        Args:
            name: str, the name of this traffic scenario.
            mv_vehicle_f: Callable[[], Tuple[MvVehicle, float]], function that
                returns a tuple of 'Vehicle' and distance in meters to the
                vehicle in front at time t = 0, note that the position ('lane'
                and 'init_x') attributes of the 'Vehicle' will be overridden.

        """
        self.name = name
        self.mv_vehicle_f = mv_vehicle_f

    def mv_vehicles(self, lane: int):
        """Yields sequential vehicles on one lane at time 0.

        Args:
            lane: lane index of vehicles on the bridge.

        """
        dist = 0  # Where the next vehicles is at time t = 0.
        mv_vehicle, inter_vehicle_dist = None, None
        while True:

            mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f()
            mv_vehicle.lane = lane
            mv_vehicle.init_x = -dist
            yield mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length

    def traffic_sequence(self, config: Config, time: float) -> "TrafficSequence":
        """Generate a "TrafficSequence" under this traffic scenario.

        Args:
            config: simulation configuration object.
            time: simulation time in seconds.

        """
        bridge = config.bridge
        mv_vehicle_gens = [
            self.mv_vehicles(lane=lane) for lane, _ in enumerate(bridge.lanes)
        ]
        vehicles_per_lane = [
            [next(mv_vehicle_gens[lane])] for lane, _ in enumerate(bridge.lanes)
        ]
        warmed_up_at = max([vs[0].time_left_bridge(bridge) for vs in vehicles_per_lane])
        print_i(f"Warmed up at {warmed_up_at:.2f} s")
        final_time = time + warmed_up_at
        print_i(f"Final time at {final_time:.2f} s")
        for lane, _ in enumerate(bridge.lanes):
            while True:
                v = next(mv_vehicle_gens[lane])
                entering_time = v.time_entering_bridge(bridge)
                print_i(
                    f"Lane {lane}: entering time at {entering_time:.2f} s", end="\r"
                )
                if entering_time > final_time:
                    break
                vehicles_per_lane[lane].append(v)
        print_i("Generated TrafficSequence")
        return TrafficSequence(
            config=config,
            vehicles_per_lane=vehicles_per_lane,
            warmed_up_at=warmed_up_at,
            final_time=final_time,
        )


Traffic = NewType("Traffic", List[List[List[Vehicle]]])
"""Vehicles indexed first by timestep then by lane.

This representation naturally fits the semantics of real life traffic on a
bridge. A representation that is useful for plotting.

"""


TrafficArray = NewType("TrafficArray", np.ndarray)
"""Loads in array of time step (rows) * wheel track positions (columns).

Each cell value is load in kilo Newton. This representation is useful for matrix
multiplication. NOTE: a cell is indexed as wheel track * x position.

"""


class TrafficSequence:
    def __init__(
        self,
        config: Config,
        vehicles_per_lane: List[List[Vehicle]],
        warmed_up_at: float,
        final_time: float,
    ):
        """A list of "Vehicle" for each lane."""
        self.config = config
        self.vehicles_per_lane = vehicles_per_lane
        self.start_time = warmed_up_at
        self.final_time = final_time
        self.times = np.arange(
            self.start_time,
            self.final_time + (self.config.sensor_freq / 2),
            self.config.sensor_freq,
        )
        assert self.times[0] == self.start_time

    def traffic(self) -> Traffic:
        """Convert this "TrafficSequence" to "Traffic"."""
        bridge = self.config.bridge
        result = [[[] for _ in bridge.lanes] for _ in self.times]
        print_i("Generating Traffic")
        for t, time in enumerate(self.times):
            print_i(f"Generating Traffic: time {time:.2f} s", end="\r")
            for l, vehicles in enumerate(self.vehicles_per_lane):
                for vehicle in vehicles:
                    if vehicle.on_bridge(time=time, bridge=bridge):
                        result[t][l].append(vehicle)
        return result

    def traffic_array(self) -> Traffic:
        """Convert this "TrafficSequence" to "Traffic"."""
        result = np.zeros(
            (len(self.times), len(self.config.bridge.lanes) * self.config.il_num_loads,)
        )
        vehicles = set(flatten(self.vehicles_per_lane, Vehicle))
        total_vehicles = len(vehicles)
        print_i("Generating TrafficArray")
        # For each vehicle..
        for v_i, vehicle in enumerate(vehicles):
            print_i(
                f"Generating TrafficArray: vehicle {v_i} / {total_vehicles}", end="\r"
            )
            # ..find the times on the bridge in the simulation..
            v_time_indices, v_times = vehicle._times_on_bridge(self.config, self.times,)
            # ..then for each time fill in the traffic array.
            for v_time_index, loads in zip(
                v_time_indices, vehicle._axle_track_indices(self.config, v_times),
            ):
                for (lo, load_lo), (hi, load_hi) in loads:
                    result[v_time_index][lo] = load_lo
                    if hi is not None:
                        result[v_time_index][hi] = load_hi
        return result


def _poisson_arrival(beta: float, min_d: float):
    """Poisson inter-arrival times of vehicles to a bridge."""
    result = np.random.exponential(beta)
    assert isinstance(result, float)
    if result < min_d:
        return _poisson_arrival(beta=beta, min_d=min_d)
    return result


def normal_traffic(config: Config, lam: float = 5, min_d: float = 2):
    """Normal traffic scenario, arrives according to poisson process."""

    def mv_vehicle_f():
        return sample_vehicle(config), _poisson_arrival(beta=lam, min_d=min_d)

    return TrafficScenario(name=f"normal-lam-{lam}", mv_vehicle_f=mv_vehicle_f)


def _traffic_name(c: Config, traffic_scenario: TrafficScenario, time: float):
    return safe_str(f"{traffic_scenario.name} {c.il_num_loads} {time} {c.sensor_freq}")


def load_traffic(
    config: Config,
    traffic_scenario: TrafficScenario,
    time: float,
    add: Optional[str] = None,
) -> Tuple[TrafficSequence, Traffic, TrafficArray]:
    """Load traffic from disk, generated if necessary."""
    path = (
        config.get_data_path(
            "traffic",
            _traffic_name(c=config, traffic_scenario=traffic_scenario, time=time),
            acc=False,
        )
        + ".npy"
    )
    if add is not None:
        path += add
    # Create the traffic if it doesn't exist.
    if not os.path.exists(path + ".arr"):
        traffic_sequence = traffic_scenario.traffic_sequence(config=config, time=time)
        traffic = traffic_sequence.traffic()
        traffic_array = traffic_sequence.traffic_array()
        with open(path + ".seq", "wb") as f:
            dill.dump(traffic_sequence, f)
        with open(path + ".tra", "wb") as f:
            dill.dump(traffic, f)
        with open(path + ".arr", "wb") as f:
            np.save(f, traffic_array)
    with open(path + ".seq", "rb") as f:
        traffic_sequence = dill.load(f)
    with open(path + ".tra", "rb") as f:
        traffic = dill.load(f)
    with open(path + ".arr", "rb") as f:
        traffic_array = np.load(f)
    return traffic_sequence, traffic, traffic_array
