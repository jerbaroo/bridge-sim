"""Generate time series of traffic."""

import os
from collections import deque
from timeit import default_timer as timer
from typing import NewType, List, Tuple, Callable, Optional

import dill
import numpy as np
from bridge_sim.vehicles.sample import sample_vehicle

from bridge_sim.model import Bridge, Config, Vehicle
from bridge_sim.util import print_i, st, safe_str

D = False


Traffic = NewType("Traffic", List[List[List[Vehicle]]])
"""Vehicles per lane per time step.

This representation naturally fits the semantics of real life traffic on a
bridge. A representation that is useful for plotting.

"""

TrafficArray = NewType("TrafficArray", np.ndarray)
"""Loads in array of time step (rows) * wheel track positions (columns).

Each cell value is load in kilo Newton. This representation is useful for matrix
multiplication. NOTE: a cell is indexed as wheel track * x position.

"""


class TrafficScenario:
    """A named traffic scenario that generates moving vehicles.

    Args:
        name: str, the name of this traffic scenario.

        mv_vehicle_f: Callable[..., Tuple[MvVehicle, float]], function that
            returns a tuple of 'MvVehicle' and the distance in meters to the
            vehicles in front at time t = 0, note that the position ('lane' and
            'init_x_frac') of this 'MvVehicle' will be overridden. A number of
            keyword arguments will be passed to this function, for details see
            the implementation of 'mv_vehicles'.

    """

    def __init__(self, name: str, mv_vehicle_f: Callable[[], Vehicle]):
        self.name = name
        self.mv_vehicle_f = mv_vehicle_f

    def mv_vehicles(self, bridge: Bridge, lane: int):
        """Moving vehicles on one lane at time t = 0.

        This generator yields a function which returns the next vehicles on given
        lane, at time t = 0, from the current time and full lanes traveled.

        Args:
            bridge: the bridge the vehicles drive on.
            lane: index of the lane on the bridge the vehicles drive on.

        """
        dist = 0  # Where the next vehicles is at time t = 0.
        mv_vehicle, inter_vehicle_dist = None, None
        while True:

            def next_mv_vehicle(time: float, full_lanes: int):
                """The function to generate the next vehicles."""
                nonlocal mv_vehicle
                nonlocal inter_vehicle_dist
                mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f()
                mv_vehicle.lane = lane
                mv_vehicle.init_x = -bridge.x(x=dist)
                return mv_vehicle

            yield next_mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length

    def traffic_sequence(self, bridge: Bridge, max_time: float) -> "TrafficSequence":
        """Generate a 'TrafficSequence' under this traffic scenario.

        Returns a sequence of traffic events such that there is at least
        'max_time' of traffic from when the traffic sequence has warmed up.
        There is one additional event after 'max_time' is reached.

        Args:
            bridge: Bridge, bridge the vehicles drive on.
            max_time: float, simulation time after warm up, in seconds.

        """
        result: TrafficSequence = []
        # Per lane, a vehicles generator.
        mv_vehicle_gens = [
            self.mv_vehicles(bridge=bridge, lane=lane)
            for lane, _ in enumerate(bridge.lanes)
        ]
        # Per lane, next vehicles ready to drive onto the lane.
        next_vehicles: List[Vehicle] = [next(gen)() for gen in mv_vehicle_gens]
        # All vehicles must start at x = 0, sanity check.
        if not all(v.init_x == 0 for v in next_vehicles):
            raise ValueError("Initial vehicles not starting at x = 0")
        # Time vehicles will leave the bridge, in order.
        time_leave: List[Tuple[Vehicle, float]] = deque([])
        # Until maximum time is reached, see below..
        while True:
            # The next event's vehicles, time, and event type (enter/leave).
            vehicle, event_time, enter = None, np.inf, True
            # Find next enter/leave event.
            for v in next_vehicles:
                t = v.time_entering_bridge(bridge)
                if t < event_time:
                    vehicle, event_time = v, t
            assert enter
            # Check if the next leave event is ready.
            if len(time_leave) > 0 and time_leave[0][1] < event_time:
                vehicle, event_time, enter = time_leave[0][0], time_leave[0][1], False
            # Add the enter/leave event to the sequence.
            result.append((vehicle, event_time, enter))
            time = event_time
            # Stop if maximum time is reached.
            if time > max_time:
                break
            print_i(f"Generating 'TrafficSequence', time = {time:.3f} s", end="\r")
            # Update vehicles entering/leaving the bridge.
            if enter:
                time_leave.append((vehicle, vehicle.time_left_bridge(bridge)))
                next_vehicles[vehicle.lane] = next(mv_vehicle_gens[vehicle.lane])()
            else:
                time_leave.popleft()
        print_i(f"Generated {time:.3f} s of 'TrafficSequence'")
        return result


class TrafficSequence:
    def __init__(self, config: Config, contents):
        """Vehicles and times when they enter/leave a bridge.

         A list of (vehicle, enter/leave time, E), where E is a boolean if they are
         entering (true) or leaving. This sequence should be time ordered. This is a
         memory efficient representation of traffic.

        """
        self.config = config
        self.contents = contents

    def traffic(self,  max_time: float) -> Traffic:
        """Convert this "TrafficSequence" to "Traffic"."""
        c = self.config
        traffic_sequence = self.contents
        result = deque([])
        current = [deque([]) for _ in c.bridge.lanes]
        time, next_event_index = 0, 0
        next_event_time = traffic_sequence[next_event_index][1]
        while len(result) < int(max_time / c.sensor_hz) + 1:
            # Make a copy of the current traffic.
            current = [current_lane.copy() for current_lane in current]
            # While events have occurred update current traffic.
            while time > next_event_time or np.isclose(time, next_event_time):
                vehicle, _, enter = traffic_sequence[next_event_index]
                if enter:
                    current[vehicle.lane].append(vehicle)
                else:
                    current[vehicle.lane].popleft()
                # Find the next event, if there is one.
                next_event_index += 1
                try:
                    next_event_time = traffic_sequence[next_event_index][1]
                except IndexError:
                    next_event_time = np.inf
            time += c.sensor_hz
        return list(result)


    def traffic_array(self, max_time: float) -> Traffic:
        """Convert this "TrafficSequence" to "Traffic"."""
        vehicles = set(v for v, _0, _1 in self.contents)
        result = np.zeros(
            (
                # '+ 1' to account for time t = 0.
                int(max_time / self.config.sensor_hz) + 1,
                # 2 wheel tracks per lane.
                len(self.config.bridge.lanes) * 2 * self.config.il_num_loads,
            )
        )
        for vehicle in vehicles:
            times = np
            for wheel_track_info in vehicle._wheel_track_indices():

def arrival(beta: float, min_d: float):
    """Inter-arrival times of vehicles to a bridge."""
    result = np.random.exponential(beta)
    assert isinstance(result, float)
    if result < min_d:
        return arrival(beta=beta, min_d=min_d)
    return result


def normal_traffic(c: Config, lam: float, min_d: float):
    """Normal traffic scenario, arrives according to poisson process."""
    count = 0

    def mv_vehicle_f():
        start = timer()
        vehicle = sample_vehicle(c), arrival(beta=lam, min_d=min_d)
        nonlocal count
        count += 1
        print_i(f"{count}{st(count)} sampled vehicles took {timer() - start}")
        return vehicle

    return TrafficScenario(name=f"normal-lam-{lam}", mv_vehicle_f=mv_vehicle_f)


def _traffic_name(c: Config, traffic_scenario: TrafficScenario, max_time: float):
    return safe_str(
        f"{traffic_scenario.name} {c.il_num_loads} {max_time} {c.sensor_hz}"
    )


def load_traffic(
    c: Config,
    traffic_scenario: TrafficScenario,
    max_time: float,
    add: Optional[str] = None,
) -> Tuple[TrafficSequence, Traffic, TrafficArray]:
    """Load traffic from disk, generated if necessary."""
    path = (
        c.get_data_path(
            "traffic",
            _traffic_name(c=c, traffic_scenario=traffic_scenario, max_time=max_time),
            acc=False,
        )
        + ".npy"
    )
    print(path)
    if add is not None:
        path += add
    # Create the traffic if it doesn't exist.
    if not os.path.exists(path + ".arr"):
        traffic_sequence = traffic_scenario.traffic_sequence(
            bridge=c.bridge, max_time=max_time
        )
        traffic = traffic_sequence.to_traffic(
            c=c, traffic_sequence=traffic_sequence, max_time=max_time
        )
        traffic_array = traffic_sequence.to_traffic_array(
            c=c, traffic_sequence=traffic_sequence, max_time=max_time
        )
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

