"""Scenarios for the traffic and bridge."""
from typing import Callable, List, NewType, Tuple

from config import Config
from model.bridge import Bridge
from model.load import MvVehicle


class BridgeScenario:
    """Base class for bridge scenarios. Do not construct directly."""
    def __init__(self, name: str):
        self.name = name


# A list of vehicles on a bridge for each time step of a traffic simulation.
Traffic = NewType("Traffic", List[List[MvVehicle]])


class TrafficScenario:
    """A named traffic scenario that generates moving vehicles.

    Args:
        name: str, the name of this traffic scenario.

        mv_vehicle_f: Callable[..., Tuple[MvVehicle, float]], function that
            returns a tuple of 'MvVehicle' and the distance in meters to the
            vehicle in front at time t = 0, note that the position ('lane' and
            'init_x_frac') of this 'MvVehicle' will be overridden. A keyword
            argument 'full_lanes: int' will be passed to this function, the full
            lengths of bridge 705 that have been driven by the first vehicles.

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

            def next_mv_vehicle(traffic: Traffic, time: float):
                """The function to generate the next vehicle."""
                nonlocal mv_vehicle; nonlocal inter_vehicle_dist
                mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f(
                    traffic=traffic, time=time)
                mv_vehicle.lane = lane
                mv_vehicle.init_x_frac = -bridge.x_frac(x=dist)
                return mv_vehicle

            yield next_mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length

    def traffic(
            self, bridge: Bridge, max_time: float, time_step: float
            ) -> Tuple[Traffic, List[int]]:
        """Generate 'Traffic' under this traffic scenario.

        Returns a tuple of the traffic per time step, and a list of the index of
        each simulation time step when a full lane of traffic has passed over
        the bridge. The first index of this list is when the simulation has
        "warmed up".

        Args:
            bridge: Bridge, the bridge the vehicles drive on.
            max_time: float, the time to generate traffic until.
            time_step: float, the time step to move traffic by.

        """
        # A vehicle generator for each traffic lane.
        mv_vehicle_gens = [
            self.mv_vehicles(bridge=bridge, lane=lane)
            for lane, _ in enumerate(bridge.lanes)]
        # The vehicles on the bridge at initial time t = 0.
        sim_vehicles = [[next(gen)(None, None) for gen in mv_vehicle_gens]]
        assert all(v.on_bridge(time=0, bridge=bridge) for v in sim_vehicles[-1])
        # The next vehicles ready to drive onto the bridge, per lane.
        next_vehicles = [next(gen)(None, None) for gen in mv_vehicle_gens]
        # The first vehicles on the bridge. This is updated over time to
        # calculate how many full lanes of traffic have passed over the bridge.
        first_vehicles = sim_vehicles[-1]
        full_lanes_at = []
        full_lanes = lambda: (
            sim_vehicles[-1][0].x_at(time=time, bridge=bridge)
            // bridge.length)
        # Remove/add vehicles for each additional time step.
        time = time_step
        while time <= max_time:
            # Keep the previous vehicles still on the bridge.
            sim_vehicles.append([
                vehicle for vehicle in sim_vehicles[-1]
                if vehicle.on_bridge(time=time, bridge=bridge)])
            # Add vehicles on the bridge, checking each lane in turn.
            for l, next_vehicle in enumerate(next_vehicles):
                # If the next vehicle is on the bridge at this time, add it to
                # the bridge traffic and get the next lane's vehicle ready.
                if next_vehicle.on_bridge(time=time, bridge=bridge):
                    sim_vehicles[-1].append(next_vehicle)
                    next_vehicles[l] = next(mv_vehicle_gens[l])(sim_vehicles, time)
            # Record if a full lane of traffic has crossed the bridge.
            if all(vehicle.passed_bridge(time=time, bridge=bridge)
                   for vehicle in first_vehicles):
                first_vehicles = [vehicle for vehicle in next_vehicles]
                if full_lanes() == 0:
                    print(f"full_lanes = {full_lanes()}")
                    max_time += time
                full_lanes_at += [len(sim_vehicles) - 1]
            time += time_step
        if full_lanes() == 0:
            raise ValueError("Traffic did not warm up, time = {time}")
        print(f"full lanes at = {full_lanes_at[0]}")
        return sim_vehicles, full_lanes_at[0]
