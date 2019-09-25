"""Vehicles and loads."""
from typing import List, Tuple

from config import Config
from model.bridge import Bridge
from util import print_d

# Print debug information for this file.
D: bool = False


class Vehicle:
    """Specification of a vehicle with speed."""
    def __init__(
            self, kmph: float, kn_per_axle: float, axle_distances: List[float],
            axle_width: float = 2, quadim: Tuple[float, float] = (0.4, 0.2)):
        self.kmph = kmph
        self.kn_per_axle = kn_per_axle
        self.axle_distances = axle_distances
        self.length = sum(self.axle_distances)
        self.axle_width = axle_width
        self.quadim = quadim


class Load:
    """A load to apply to a bridge, either a point or axle-based load.

    Args:
        x_frac: float, fraction of x position in [0 1].
        kn: float, point load intensity or force per axle, in kN.
        lane: int, 0 is the first lane.
        axle_distances: None or [float], distances between axles in meters.
        axle_width: None or float, width of an axle in meters.
        quadim: None or (float, float): length and width of wheel in meters.

    """
    def __init__(self, x_frac: float, kn: float, lane: int = 0,
                 axle_distances: List[float] = None, axle_width: float = 2,
                 quadim: Tuple[float, float] = (0.4, 0.2)):
        # assert x_frac >= 0 and x_frac <= 1
        self.x_frac = x_frac
        # TODO: z_frac.
        self.z_frac = 0.1
        self.kn = kn
        self.lane = lane
        self.axle_distances = axle_distances
        self.num_axles = (
            None if self.axle_distances is None
            else len(self.axle_distances) + 1)
        self.axle_width = axle_width
        self.quadim = quadim

    def is_point_load(self):
        """Whether this load is a point load."""
        return self.axle_distances is None

    def total_kn(self):
        """The total weight in kN of this load."""
        if self.is_point_load():
            return self.kn
        return sum(self.kn for _ in range(self.num_axles))

    def __repr__(self):
        """Human readable representation of this load."""
        load_type = (
            "point" if self.is_point_load() else f"{self.num_axles}-axle")
        units = "kN per axle" if self.is_point_load() else "kN"
        return (f"<Load type: {load_type}, kN: {self.total_kn():.2f} {units}"
                + f", lane: {self.lane}>")

    def __str__(self):
        """String uniquely respresenting this load."""
        return f"({self.x_frac:.2f}, {self.total_kn():.2f})"


class MovingLoad:
    """A load with a constant speed.

    Args:
        load: Load, the load that is moving.
        kmph: float, the load's initial speed in kilometers per hour.
        l_to_r: bool, the direction of the load on the bridge.

    """
    def __init__(self, load: Load, kmph: float, l_to_r: bool = True):
        print_d(D, f"Moving")
        self.load = load
        self.kmph = kmph
        self.mps = self.kmph / 3.6
        self.l_to_r = l_to_r

    def __repr__(self):
        return (
            f"<MovingLoad kmph: {self.kmph}, l_to_r: {self.l_to_r}"
            + f", load: {self.load}")

    @staticmethod
    def from_vehicle(
            x_frac: float, vehicle: Vehicle, lane: int, l_to_r: bool = True):
        """Construct a Load from a Vehicle."""
        load = Load(
            x_frac=x_frac, kn=vehicle.kn_per_axle, lane=lane,
            axle_distances=vehicle.axle_distances,
            axle_width=vehicle.axle_width, quadim=vehicle.quadim)
        return MovingLoad(load=load, kmph=vehicle.kmph, l_to_r=l_to_r)

    @staticmethod
    def sample(c: Config, x_frac: float, lane: int, l_to_r: bool = True):
        """Construct a moving load from a sampled vehicle."""
        from vehicles.sample import sample_vehicle
        return MovingLoad.from_vehicle(
            x_frac=x_frac, vehicle=sample_vehicle(c), lane=lane, l_to_r=l_to_r)

    def x_frac_at(self, time: float, bridge: Bridge):
        """Fraction of bridge length after given time.

        Args:
            time: float, time in seconds.

        """
        delta_frac = (self.mps * time) / bridge.length
        if not self.l_to_r:
            delta_frac *= -1
        return self.load.x_frac + delta_frac

    def x_at(self, time: float, bridge: Bridge):
        """X ordinate of bridge in meters after given time.

        Args:
            time: float, time in seconds.

        """
        return bridge.x(self.x_frac_at(time, bridge))

    def str_id(self):
        """String ID for this moving load."""
        return f"{str(self.load)}-{self.kmph:.2f}-{self.l_to_r}"


class DisplacementCtrl:
    """Apply a load in simulation until the displacement is reached.

    Args:
        displacement: float, displacement in meters.
        pier: int, index of the pier (fixed node) starting at 0.

    """
    def __init__(self, displacement: float, pier: int):
        self.displacement = displacement
        self.pier = pier
