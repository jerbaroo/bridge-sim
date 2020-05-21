"""Scenarios for the traffic and bridge."""
from collections import deque
from copy import copy, deepcopy
from typing import Callable, List, NewType, Tuple

import numpy as np
from scipy.interpolate import interp1d

# from classify.data.responses.convert import loads_to_traffic_array
from bridge_sim.model.config import Config
from lib.fem.params import SimParams
from lib.model.bridge import Bridge
from lib.model.load import MvVehicle
from util import print_i


class DamageScenario:
    """Base class for bridge scenarios. Do not construct directly."""

    def __init__(
        self,
        name: str,
        mod_bridge: Callable[[Bridge], Bridge] = lambda b: b,
        mod_sim_params: Callable[[SimParams], SimParams] = lambda s: s,
    ):
        self.name = name
        self.mod_bridge = mod_bridge
        self.mod_sim_params = mod_sim_params

    def use(
        self, c: Config, sim_params: SimParams = SimParams(),
    ) -> Tuple[Config, SimParams]:
        """Copies of the given arguments modified for this damage scenario."""
        config_copy = copy(c)
        config_copy.bridge = self.mod_bridge(deepcopy(config_copy.bridge))
        sim_params_copy = self.mod_sim_params(deepcopy(sim_params))
        return config_copy, sim_params_copy


# A list of vehicle, time they enter/leave the bridge, and a boolean if they are
# entering (true) or leaving. This sequence should be time ordered. This is a
# memory efficient representation of traffic.
TrafficSequence = NewType("TrafficSequence", List[Tuple[MvVehicle, float, bool]])

# A list of vehicles per lane per time step. This representation naturally fits
# the semantics of real life traffic on a bridge. Useful for plotting.
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
        self, bridge: Bridge, max_time: float, adjust: bool = True
    ) -> TrafficSequence:
        """Generate a 'TrafficSequence' under this traffic scenario.

        Returns a sequence of traffic events such that there is at least
        'max_time' of traffic from when the traffic sequence has warmed up.
        There is one additional event after 'max_time' is reached.

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
        warmed_up_at = first_vehicle.time_left_bridge(bridge)
        print(f"Trafic warmed up at = {warmed_up_at}")
        max_time += warmed_up_at
        print(f"max_time = {max_time}")

        # Time vehicles will leave the bridge, in order.
        time_leave: List[Tuple[MvVehicle, float]] = deque([])

        # Until maximum time is reached, see below..
        while True:
            # The next event's vehicle, time, and event type (enter/leave).
            vehicle, event_time, enter = None, np.inf, True

            # Find next enter/leave event.
            for v in next_vehicles:
                t = v.time_entering_bridge(bridge)
                if t < event_time:
                    vehicle, event_time = v, t
            assert enter == True
            # for v, t in time_leave:
            # Check if the next leave event is ready.
            if len(time_leave) > 0 and time_leave[0][1] < event_time:
                vehicle, event_time, enter = time_leave[0][0], time_leave[0][1], False

            # Add the enter/leave event to the sequence.
            result.append((vehicle, event_time, enter))
            time = event_time

            # Stop if maximum time is reached.
            if event_time > max_time:
                break
            print_i(f"Generating 'TrafficSequence', time = {time:.3f} s", end="\r")

            # Update vehicles entering/leaving the bridge.
            if enter:
                time_leave.append((vehicle, vehicle.time_left_bridge(bridge)))
                next_vehicles[vehicle.lane] = next(mv_vehicle_gens[vehicle.lane])(
                    time=time, full_lanes=full_lanes()
                )
            else:
                time_leave.popleft()

        print_i(
            f"Generated {time:.3f} - {warmed_up_at:.3f} = {time - warmed_up_at:.3f} s of 'TrafficSequence'"
        )
        return result


def to_traffic(
    c: Config, traffic_sequence: TrafficSequence, max_time: float, warm_up: bool = True,
) -> Traffic:
    """Convert a 'TrafficSequence' to 'Traffic'."""
    result = deque([])
    current = [deque([]) for _ in c.bridge.lanes]
    time = 0
    next_event_index = 0
    next_event_time = traffic_sequence[next_event_index][1]

    # If it is requested that traffic warm up first, then until time
    # 'warmed_up_at' is reached, nothing will be added to the 'TrafficArray'.
    warmed_up_at = traffic_sequence[0][0].time_left_bridge(c.bridge)
    print(f"warmed up at = {warmed_up_at}")

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

        # Append current traffic and update time.
        if not warm_up or time > warmed_up_at or np.isclose(time, warmed_up_at):
            result.append(current)
        time += c.sensor_hz

    return list(result)


def to_traffic_array(
    c: Config,
    traffic_sequence: TrafficSequence,
    max_time: float,
    warm_up: bool = True,
    new: bool = True,
) -> Traffic:
    """Convert a 'TrafficSequence' to 'Traffic'.

    Args:
        c: Config, global configuration object.
        traffic_sequence: TrafficSequence, the sequence of traffic to convert
            into a 'TrafficArray'.
        max_time: float, maximum time of 'TrafficArray' to generate.
        warm_up: bool, if true then begin generating the 'TrafficArray' once the
            first vehicle has passed over the bridge (traffic has warmed up).
        new: bool, use the new "bucketing" method instead of the old method.

    """

    # NOTE: If you are going to try understand the code in this function then
    # start with looking at 'to_traffic', as that is almost a subset of this
    # code.

    print_i("Converting 'TrafficSequence' to 'TrafficArray'")
    time_step = c.sensor_hz
    print(
        f"array size = {int(max_time / time_step)}, {len(c.bridge.lanes) * 2 * c.il_num_loads}"
    )
    # Initial traffic array, to be filled in.
    result = np.zeros(
        (
            # '+ 1' to account for time t = 0.
            int(max_time / time_step) + 1,
            # 2 wheel tracks per lane.
            len(c.bridge.lanes) * 2 * c.il_num_loads,
        )
    )
    # Current traffic per lane.
    current = [deque([]) for _ in c.bridge.lanes]
    # Current time and timestep index.
    time, time_i = 0, 0
    # The next event and time the next event occurs.
    next_event_index = 0
    next_event_time = traffic_sequence[next_event_index][1]
    # Interpolate from x position to wheel track bucket.
    _interp = interp1d([c.bridge.x_min, c.bridge.x_max], [0, c.il_num_loads - 1])

    def interp(x):
        return int(np.around(_interp(x), 0))

    wheel_track_xs = c.bridge.wheel_track_xs(c)
    # Column index where each wheel track starts.
    j_indices = [
        (l * 2 * c.il_num_loads, ((l * 2) + 1) * c.il_num_loads)
        for l, _ in enumerate(current)
    ]

    # If it is requested that traffic warm up first, then until time
    # 'warmed_up_at' is reached, nothing will be added to the 'TrafficArray'.
    warmed_up_at = traffic_sequence[0][0].time_left_bridge(c.bridge)

    last_print_time, start_time = -np.inf, None
    while time_i < result.shape[0]:
        # Print an update when at least 1 second has passed.
        if time - last_print_time > 1:
            print_i(f"Generating 'TrafficArray', time = {time:.4f} s", end="\r")
            last_print_time = time

        # While events have occurred, update current traffic.
        while time > next_event_time or np.isclose(time, next_event_time):
            vehicle, _, enter = traffic_sequence[next_event_index]
            if enter:
                current[vehicle.lane].append(vehicle)
                print(
                    f"Vehicle entered {vehicle.lane} at t = {time:.3f}, sum = {len(current[vehicle.lane])}",
                    end="\r",
                )
            else:
                current[vehicle.lane].popleft()
                print(
                    f"Vehicle left {vehicle.lane} at t = {time:.3f}, sum = {len(current[vehicle.lane])}"
                )
            # Find the next event, if there is one.
            next_event_index += 1
            try:
                next_event_time = traffic_sequence[next_event_index][1]
            except IndexError:
                next_event_time = np.inf

        # Only add to the 'TrafficArray' if the traffic is not required to warm
        # up, or the traffic has already warmed up.
        if not warm_up or time > warmed_up_at or np.isclose(time, warmed_up_at):
            # TODO: This bottom part of the loop should be parallelized!
            if start_time is None:
                start_time = time
            # For each vehicle, find the lane it's on, and indices into the ULM.
            if new:
                for js, vehicles in zip(j_indices, current):
                    for vehicle in vehicles:
                        # Here the wheel track bucketing is implemented.
                        for axle_loads in vehicle.to_wheel_track_loads_(
                            c=c, time=time, wheel_track_xs=wheel_track_xs,
                        ):
                            # The x indices are equal per axle.
                            x_inds = [interp(x) for x, _ in axle_loads[0]]
                            for j, wheel_loads in zip(js, axle_loads):
                                for x_ind, (load_x, load_kn) in zip(
                                    x_inds, wheel_loads
                                ):
                                    result[time_i][j + x_ind] += load_kn
            # The old method.
            else:
                # For each lane.
                for (j0, j1), vehicles in zip(j_indices, current):
                    # For each vehicle.
                    for vehicle in vehicles:
                        xs = vehicle.xs_at(time=time, bridge=c.bridge)
                        kns = vehicle.kn_per_axle()
                        # assert len(xs) == len(kns)
                        # For each axle currently on the bridge.
                        for x, kn in zip(xs, kns):
                            if x >= c.bridge.x_min and x <= c.bridge.x_max:
                                x_ind = interp(x)
                                # For each wheel.
                                for j in [j0, j1]:
                                    # print(f"lane = {l}, w = {w}, x = {x}, x_interp = {x_interp(x)}, j = {j}, kn = {kn / 2}")
                                    result[time_i][j + x_ind] = kn / 2
            time_i += 1
        time += time_step

    print_i(
        f"Generated {time - start_time - time_step:.4f} s of 'TrafficArray' from 'TrafficSequence'"
    )
    return result
