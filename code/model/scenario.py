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
        mv_vehicle_F: Callable[[], Tuple[MvVehicle, float]], function that
            returns a tuple of 'MvVehicle' and the distance in meters to the
            vehicle in front at time t=0, note that the position ('lane' and
            'init_x_frac') of this 'MvVehicle' will be overridden.

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
            self, bridge: Bridge, max_time: float, time_step: float, after_warm_up: bool
            ) -> Traffic:
        """Generate 'Traffic' under this traffic scenario."""
        # A vehicle generator for each traffic lane.
        mv_vehicle_gens = [
            self.mv_vehicles(bridge=bridge, lane=l)
            for l, _ in enumerate(bridge.lanes)]
        # The vehicles on the bridge for the first time step.
        sim_vehicles = [[next(gen) for gen in mv_vehicle_gens]]
        # The next vehicles ready to drive onto the bridge, per lane.
        next_vehicles = [next(gen) for gen in mv_vehicle_gens]
        # Remove/add vehicles for each additional time step.
        time = time_step
        while time <= max_time:
            # Remove any vehicles that are off the bridge.
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
            time += time_step
        return sim_vehicles
