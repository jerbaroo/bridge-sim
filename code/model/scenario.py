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
        mv_vehicle_F: Callable[[int], Tuple[MvVehicle, float]], function that
            returns a tuple of 'MvVehicle' and the distance in meters to the
            vehicle in front, note that the position ('lane' and 'init_x_frac')
            of this 'MvVehicle' will be overridden. The int 'full_lanes' passed
            to this function represents the amount of times traffic has crossed
            the bridge, when a vehicle has crossed each lane this becomes 1.
            When vehicles have again crossed each lane that had not entered the
            bridge when 'full_lanes' became 1 this becomes 2.

    """
    def __init__(
            self, name: str, mv_vehicle_f: Callable[[], Tuple[MvVehicle, float]]):
        self.name = name
        self.mv_vehicle_f = mv_vehicle_f

    def mv_vehicles(self, bridge: Bridge, lane: int):
        """Yield moving vehicles on one lane under this traffic scenario.

        Remember that regardless of lane direction 'init_x_frac' of 0 indicates
        the point where the vehicles will enter on that line.

        Args:
            bridge: Bridge, the bridge the vehicles drive on.
            lane: int, index of the lane on the bridge the vehicles drive on.

        """
        dist = 0  # In meters.
        while True:
            mv_vehicle, inter_vehicle_dist = self.mv_vehicle_f()
            mv_vehicle.lane = lane
            mv_vehicle.init_x_frac = -bridge.x_frac(x=dist)
            yield mv_vehicle
            dist += inter_vehicle_dist
            dist += mv_vehicle.length

    def traffic(
            self, bridge: Bridge, max_time: float, time_step: float
            ) -> Tuple[Traffic, int]:
        """Generate 'Traffic' under this traffic scenario.

        Returns a tuple of the traffic per time step, and the index of the first
        time step when traffic has passed across each lane, when the simulation
        has "warmed up".

        Args:
            bridge: Bridge, the bridge the vehicles drive on.
            max_time: float, the time to generate traffic until.
            time_step: float, the time step to move traffic by.

        """
        # A vehicle generator for each traffic lane.
        mv_vehicle_gens = [
            self.mv_vehicles(bridge=bridge, lane=l)
            for l, _ in enumerate(bridge.lanes)]
        # The vehicles on the bridge at initial time t = 0.
        sim_vehicles = [[next(gen) for gen in mv_vehicle_gens]]
        assert all(v.on_bridge(time=0, bridge=bridge) for v in sim_vehicles[-1])
        # The next vehicles ready to drive onto the bridge, per lane.
        next_vehicles = [next(gen) for gen in mv_vehicle_gens]
        # The first vehicles on the bridge. This is updated over time to
        # calculate how many full lanes of traffic have passed over the bridge.
        first_vehicles = sim_vehicles[-1]
        full_lanes = lambda: len(first_vehicles) - 1
        warmed_up_at = None
        # Remove/add vehicles for each additional time step.
        time = time_step
        while time <= max_time:
            # At next time step keep only the vehicles still on the bridge.
            sim_vehicles.append([
                vehicle for vehicle in sim_vehicles[-1]
                if vehicle.on_bridge(time=time, bridge=bridge)])
            # Add vehicles on the bridge, checking each lane in turn.
            for l, next_vehicle in enumerate(next_vehicles):
                # If the next vehicle is on the bridge at this time, add it to
                # the bridge traffic and get the next lane's vehicle ready.
                if next_vehicle.on_bridge(time=time, bridge=bridge):
                    sim_vehicles[-1].append(next_vehicle)
                    next_vehicles[l] = next(mv_vehicle_gens[l])
            # Record if a full lane of traffic has crossed the bridge.
            if all(vehicle.passed_bridge(time=time, bridge=bridge)
                   for vehicle in first_vehicles):
                first_vehicles = [vehicle for vehicle in next_vehicles]
                if warmed_up_at is None:
                    warmed_up_at = len(sim_vehicles) - 1
                    max_time += time
            time += time_step
        if warmed_up_at is None:
            raise ValueError("Traffic did not warm up, time = {time}")
        return sim_vehicles, warmed_up_at
