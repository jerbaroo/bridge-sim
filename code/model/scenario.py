"""Scenarios for the traffic and bridge."""
from typing import Callable, List, NewType, Tuple

from config import Config
from model.bridge import Bridge
from model.load import MvVehicle
from util import print_i


class BridgeScenario:
    """Base class for bridge scenarios. Do not construct directly."""
    def __init__(self, name: str):
        self.name = name


# A list of vehicles on a bridge per time step.
Traffic = NewType("Traffic", List[List[MvVehicle]])


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
    def __init__(
            self, name: str, mv_vehicle_f: Callable[..., Tuple[MvVehicle, float]]):
        self.name = name
        self.mv_vehicle_f = mv_vehicle_f

    def mv_vehicles(self, bridge: Bridge, lane: int):
        """Moving vehicles on one lane at time t = 0.

        This generator yields a function which returns the next vehicle on given
        lane, at time t = 0, from the current simulation 'Traffic' and time.

        Remember that regardless of lane direction 'init_x_frac' of 0 indicates
        the point where the vehicles will enter on that lane.

        Args:
            bridge: Bridge, the bridge the vehicles drive on.
            lane: int, index of the lane on the bridge the vehicles drive on.

        """
        dist = 0  # Where the next vehicle is at time t = 0.
        mv_vehicle, inter_vehicle_dist = None, None
        while True:

            def next_mv_vehicle(traffic: Traffic, time: float, full_lanes: int):
                """The function to generate the next vehicle."""
                nonlocal mv_vehicle; nonlocal inter_vehicle_dist
                mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f(
                    traffic=traffic, time=time, full_lanes=full_lanes)
                mv_vehicle.lane = lane
                mv_vehicle.init_x_frac = -bridge.x_frac(x=dist)
                return mv_vehicle

            yield next_mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length

    def traffic(
            self, bridge: Bridge, max_time: float, time_step: float
            ) -> Tuple[Traffic, int]:
        """Generate 'Traffic' under this traffic scenario.

        Returns a tuple of 'Traffic' and time index the simulation warmed up at.

        Args:
            bridge: Bridge, the bridge the vehicles drive on.
            max_time: float, simulation time after warm up, in seconds.
            time_step: float, the time step to move traffic by, in seconds.

        """
        # A vehicle generator for each traffic lane.
        mv_vehicle_gens = [
            self.mv_vehicles(bridge=bridge, lane=lane)
            for lane, _ in enumerate(bridge.lanes)]

        sim_vehicles: Traffic = []  # Vehicles per time step, to return.
        time: float = 0  # Time step of current iteration of the loop.

        # Per lane, next vehicles ready to drive onto the bridge.
        next_vehicles = [
            next(gen)(traffic=sim_vehicles, time=time, full_lanes=0)
            for gen in mv_vehicle_gens]
        if not all(vehicle.init_x_frac == 0 for vehicle in next_vehicles):
            raise ValueError("Initial vehicles not starting at x = 0")

        # Full bridge lanes travelled by the first vehicle on the bridge.
        first_vehicle: MvVehicle = next_vehicles[0]
        full_lanes = lambda: first_vehicle.full_lanes(time=time, bridge=bridge)

        # Time the simulation has warmed up at.
        warmed_up_at: Optional[float] = None

        # Record the vehicles at each time step.
        while warmed_up_at is None or time <= max_time:
            # Keep the previous vehicles that are still on the bridge.
            sim_vehicles.append([
                vehicle for vehicle in
                (sim_vehicles[-1] if len(sim_vehicles) > 0 else [])
                if vehicle.on_bridge(time=time, bridge=bridge)])

            # Per lane, add the next vehicle if its on the bridge.
            lanes_added = []
            for lane, next_vehicle in enumerate(next_vehicles):
                if next_vehicle.on_bridge(time=time, bridge=bridge):
                    sim_vehicles[-1].append(next_vehicle)
                    lanes_added.append(lane)

            # Per lane, get the next vehicle ready to drive on the bridge.
            for lane in lanes_added:
                next_vehicles[lane] = next(mv_vehicle_gens[lane])(
                    traffic=sim_vehicles, time=time,
                    full_lanes=full_lanes())

            # Once warmed up, increase the simulation time by warm up time.
            if warmed_up_at is None and full_lanes() > 1:
                warmed_up_at = int(time / time_step)
                max_time += time

            print_i(f"time = {time}")
            time += time_step

        return sim_vehicles, warmed_up_at
