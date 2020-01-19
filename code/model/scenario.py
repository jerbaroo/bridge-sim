"""Scenarios for the traffic and bridge."""
from collections import deque
from copy import deepcopy
from typing import Callable, List, NewType, Optional, Tuple, Union

import numpy as np
from scipy.interpolate import interp1d

from config import Config
from fem.params import SimParams
from model.bridge import Bridge
from model.load import MvVehicle
from util import print_i


class DamageScenario:
    """Base class for bridge scenarios. Do not construct directly."""

    def __init__(self, name: str, mod_bridge=lambda b: b, mod_sim_params=lambda s: s):
        self.name = name
        self.mod_bridge = mod_bridge
        self.mod_sim_params = mod_sim_params

    def use(
        self, c: Config, sim_params: Optional[SimParams] = None
    ) -> Union[Config, Tuple[Config, SimParams]]:
        """Copies of the given arguments modified for this damage scenario."""
        config_copy = deepcopy(c)
        config_copy.bridge = self.mod_bridge(config_copy.bridge)
        if sim_params is None:
            return config_copy
        sim_params_copy = self.mod_sim_params(deepcopy(sim_params))
        return config_copy, sim_params_copy


# A list of vehicle, time they enter/leave the bridge, and a boolean if they are
# entering (true) or leaving. This sequence should be time ordered. This is a
# memory efficient representation of traffic.
TrafficSequence = NewType("TrafficSequence", List[Tuple[MvVehicle, float, bool]])

# A list of vehicles per lane per time step. This representation naturally fits
# the semantics of real life traffic on a bridge.
Traffic = NewType("Traffic", List[List[List[MvVehicle]]])

# An array of time step (rows) * wheel position (columns). Each cell value is
# load in kilo Newton. This representation is useful for matrix multiplication.
# NOTE: a cell in a column is indexed as wheel track * x position.
TrafficArray = NewType("TrafficArray", np.ndarray)


class TrafficScenario:
    """A named traffic scenario that generates moving vehicles.

    Args:
        name: str, the name of this traffic scenario.

        mv_vehicle_f: Callable[..., Tuple[MvVehicle, float]], function that
            returns a tuple of 'MvVehicle' and the distance in meters to the
            vehicle in front at time t = 0, note that the position ('lane' and
            'init_x_frac') of this 'MvVehicle' will be overridden. A number of
            keyword arguments will be passed to this function, for details see
            the implementation of 'mv_vehicles'.

    """

    def __init__(self, name: str, mv_vehicle_f: Callable[..., Tuple[MvVehicle, float]]):
        self.name = name
        self.mv_vehicle_f = mv_vehicle_f

    def mv_vehicles(self, bridge: Bridge, lane: int):
        """Moving vehicles on one lane at time t = 0.

        This generator yields a function which returns the next vehicle on given
        lane, at time t = 0, from the current time and full lanes traveled.

        Remember that regardless of lane direction 'init_x_frac' of 0 indicates
        the point where the vehicles will enter on that lane.

        Args:
            bridge: Bridge, the bridge the vehicles drive on.
            lane: int, index of the lane on the bridge the vehicles drive on.

        """
        dist = 0  # Where the next vehicle is at time t = 0.
        mv_vehicle, inter_vehicle_dist = None, None
        while True:

            def next_mv_vehicle(time: float, full_lanes: int):
                """The function to generate the next vehicle."""
                nonlocal mv_vehicle
                nonlocal inter_vehicle_dist
                mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f(
                    time=time, full_lanes=full_lanes
                )
                mv_vehicle.lane = lane
                mv_vehicle.init_x_frac = -bridge.x_frac(x=dist)
                return mv_vehicle

            yield next_mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length

    def traffic_sequence(
        self, bridge: Bridge, max_time: float
    ) -> Tuple[Traffic, float]:
        """Generate a 'TrafficSequence' under this traffic scenario.

        Returns a tuple of 'Traffic' and time the simulation warmed up at.

        Args:
            bridge: Bridge, bridge the vehicles drive on.
            max_time: float, simulation time after warm up, in seconds.

        """
        result: TrafficSequence = []
        time: float = 0

        # Per lane, a vehicle generator.
        mv_vehicle_gens = [
            self.mv_vehicles(bridge=bridge, lane=lane)
            for lane, _ in enumerate(bridge.lanes)
        ]

        # Per lane, next vehicle ready to drive onto the lane.
        next_vehicles: List[MvVehicle] = [
            next(gen)(time=time, full_lanes=0) for gen in mv_vehicle_gens
        ]

        # All vehicles must start at x = 0, sanity check.
        if not all(v.init_x_frac == 0 for v in next_vehicles):
            raise ValueError("Initial vehicle not starting at x = 0")

        # Count the amount of full lanes traveled.
        first_vehicle: MvVehicle = next_vehicles[0]
        full_lanes = lambda: first_vehicle.full_lanes(time=time, bridge=bridge)

        # Increase simulation by time taken to warm up.
        warmed_up_at = first_vehicle.leaves_bridge(bridge)
        max_time += warmed_up_at

        # Time vehicles will leave the bridge, in order.
        time_leave: List[Tuple[MvVehicle, float]] = deque([])

        # Until maximum time is reached, see below..
        while True:
            vehicle, min_time, enter = None, np.inf, True

            # Find next enter/leave event.
            for v in next_vehicles:
                t = v.enters_bridge(bridge)
                if t < min_time:
                    vehicle, min_time = v, t
            for v, t in time_leave:
                if t < min_time:
                    vehicle, min_time, enter = v, t, False

            # Until maximum time is reached.
            if min_time > max_time:
                break
            time = min_time
            print_i(f"Generating 'TrafficSequence', time = {time} s", end="\r")

            # Add the enter/leave event to the sequence.
            result.append((vehicle, min_time, enter))

            # Update vehicles entering/leaving the bridge.
            if enter:
                time_leave.append((vehicle, vehicle.leaves_bridge(bridge)))
                next_vehicles[vehicle.lane] = next(mv_vehicle_gens[vehicle.lane])(
                    time=time, full_lanes=full_lanes()
                )
            else:
                time_leave.popleft()

        print_i(f"Generated {time} s of 'TrafficSequence'")
        return result, warmed_up_at


def to_traffic(
    bridge: Bridge,
    traffic_sequence: TrafficSequence,
    max_time: float,
    time_step: float,
) -> Traffic:
    """Convert a 'TrafficSequence' to 'Traffic'."""
    result = deque([])
    current = [deque([]) for _ in bridge.lanes]
    time = 0
    next_event_index = 0
    next_event_time = traffic_sequence[next_event_index][1]

    while time <= max_time:
        # Make a copy of the current traffic.
        current = [current_lane.copy() for current_lane in current]

        # While events have occurred update current traffic.
        while time >= next_event_time:
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

        # Append current traffic and update time.
        result.append(current)
        time += time_step

    return list(result)


def to_traffic_array(
    c: Config, traffic_sequence: TrafficSequence, max_time: float,
) -> Traffic:
    """Convert a 'TrafficSequence' to 'Traffic'.

    NOTE: If you are going to try understand the code in this function then
    start with looking at 'to_traffic', as that is almost a subset of this code.

    """
    print_i("Converting to 'TrafficArray")
    time_step = c.sensor_hz

    result = np.zeros(
        (
            # '+ 1' to account for time t = 0.
            int(max_time / time_step) + 1,
            # 2 wheel tracks per lane.
            len(c.bridge.lanes) * 2 * c.il_num_loads,
        )
    )
    current = [deque([]) for _ in c.bridge.lanes]
    time, t = 0, 0
    next_event_index = 0
    next_event_time = traffic_sequence[next_event_index][1]
    # Interpolate from x position to index of unit load simulation.
    bridge_length = c.bridge.length
    interp = interp1d([0, bridge_length], [0, c.il_num_loads - 1])

    # def vehicles_to_loads(
    #         c: Config, il_num_loads: Optional[float] = None,
    #         out: Optional[np.array] = None):
    #     """Decompile a list of vehicles into 'WheelTrackLoads'.

    #     TODO: Loading

    #     Args:
    #         c: Config, global configuration object.
    #         il_num_loads: Optional[float], number of unit load simulations per
    #             wheel track.

    #     """
    #     # Column index where each wheel track starts.
    #     j_indices = [
    #         (l * 2 * il_num_loads, (l * 2 * il_num_loads) + 1)
    #         for l, _ in enumerate(current)
    #     ]

    # Column index where each wheel track starts.
    j_indices = [
        (l * 2 * c.il_num_loads, (l * 2 * c.il_num_loads) + 1)
        for l, _ in enumerate(current)
    ]

    last_print_time = -np.inf
    while time <= max_time:
        if time - last_print_time > 1:
            print_i(f"Generating 'Traffic', time = {time} s", end="\r")
            last_print_time = time

        # While events have occurred update current traffic.
        while time >= next_event_time:
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

        # This bottom part of the loop can be parallelized.

        # For each lane.
        for (j0, j1), vehicles in zip(j_indices, current):
            # For each vehicle.
            for vehicle in vehicles:
                xs = vehicle.xs_at(time=time, bridge=c.bridge)
                kns = vehicle.kn_per_axle()
                # assert len(xs) == len(kns)
                # For each axle currently on the bridge.
                for x, kn in zip(xs, kns):
                    if x >= 0 and x <= bridge_length:
                        x_ind = int(interp(x))
                        # For each wheel.
                        for j in [j0, j1]:
                            # print(f"lane = {l}, w = {w}, x = {x}, x_interp = {x_interp(x)}, j = {j}, kn = {kn / 2}")
                            result[t][j + x_ind] = kn

        time += time_step
        t += 1

    print_i(f"Generated 'Traffic', time = {time} s")
    # We divide by 2 because the load per axle is shared by 2 wheels.
    return result / 2
