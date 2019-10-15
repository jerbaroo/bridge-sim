"""Vehicles and loads."""
from typing import List, Optional, Tuple

from config import Config
from model.bridge import Bridge
from util import print_d

# Comment/uncomment to print debug statements for this file.
# D: str = "model.load"
D: bool = False


class DisplacementCtrl:
    """Apply a load in simulation until the displacement is reached.

    Args:
        displacement: float, displacement in meters.
        pier: int, index of the pier (fixed node) starting at 0.

    """
    def __init__(self, displacement: float, pier: int):
        self.displacement = displacement
        self.pier = pier


class PointLoad:
    """A load conentrated at a point.

    Args:
        x_frac: float, fraction of x position on bridge, in [0 1].
        z_frac: float, fraction of z position on bridge, in [0 1].
        kn: float, load intensity in kilo Newton.

    """
    def __init__(self, x_frac: float, z_frac: float, kn: float):
        self.x_frac = x_frac
        self.z_frac = z_frac
        self.kn = kn

    def __str__(self):
        """String uniquely respresenting this load."""
        return f"({self.x_frac}, {self.z_frac}, {self.kn})"


class Vehicle:
    """A vehicle's geometry.

    Args:
        kn: Union[float, List[float]], load intensity, either for the entire
            vehicle or per axle, in kilo Newton.
        axle_distances: List[float], distance between axles in meters.
        axle_width: float, width of the vehicle's axles in meters.

    Attrs:
        length: float, length of the vehicle in meters.
        num_axles: int, number of axles.

    """
    def __init__(
            self, kn: float, axle_distances: List[float], axle_width: float):
        self.kn = kn
        self.axle_distances = axle_distances
        self.axle_width = axle_width
        self.length = sum(self.axle_distances)
        self.num_axles = len(self.axle_distances) + 1


class MvVehicle(Vehicle):
    """A moving vehicle, with position and speed.

    Position is determined by an initial position in the longitudinal direction
    of the bridge, by an index to a lane on that bridge and by a constant speed.

    NOTE: Arguments that determine position 'lane' and 'init_x_frac' are
        optional, position may be set later.

    Args:
        kn: Union[float, List[float]], load intensity, either for the entire
            vehicle or per axle, in kilo Newton.
        axle_distances: List[float], distance between axles in meters.
        axle_width: float, width of the vehicle's axles in meters.
        kmph: float, speed of the vehicle in kmph.
        lane: Optional[int], index of a lane on a bridge.
        init_x_frac: Optional[float], initial position on the lane as a fraction
            of x position of the bridge, may be negative.

    Attrs:
        length: float, length of the vehicle in meters.
        num_axles: int, number of axles.

    """
    def __init__(
            self, kn: float, axle_distances: List[float], axle_width: float,
            kmph: float, lane: Optional["Lane"] = None,
            init_x_frac: Optional[float] = None):
        super().__init__(
            kn=kn, axle_distances=axle_distances, axle_width=axle_width)
        self.kmph = kmph
        self.lane = lane
        self.init_x_frac = init_x_frac

    def wheel_tracks(
            self, bridge: Bridge, meters: bool) -> Tuple[float, float]:
        """Positions of the vehicle's wheels in transverse direction.

        Args:
            bridge: Bridge, the bridge on which the vehicle is moving.
            meters: bool, whether to return positions in meters (True) or
                fractions (False) of the bridge width in [0 1].

        """
        lane = bridge.lanes[self.lane]
        tracks = [
            lane.z_center() - (self.axle_width / 2),
            lane.z_center() + (self.axle_width + 2)]
        if meters:
            return tracks
        return list(map(lambda z: bridge.z_frac(z), tracks))

    def x_frac_at(self, time: float, bridge: Bridge):
        """Fraction of x position of bridge in meters at given time.

        Args:
            time: float, time passed from initial position, in seconds.
            bridge: Bridge, bridge the vehicle is moving on.

        """
        mps = self.kmph / 3.6  # Meters per second.
        delta_frac = (mps * time) / bridge.length
        if not bridge.lanes[self.lane].ltr:
            delta_frac *= -1
        return self.init_x_frac + delta_frac

    def x_at(self, time: float, bridge: Bridge):
        """x position of bridge in meters at given time.

        Args:
            time: float, time passed from initial position, in seconds.
            bridge: Bridge, bridge the vehicle is moving on.

        """
        return bridge.x(self.x_frac_at(time, bridge))
