"""Loads and vehicles"""
from typing import List, Optional, Tuple

import numpy as np
import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.colors as colors

from config import Config
from model.bridge import Bridge
from util import print_d

# Comment/uncomment to print debug statements for this file.
# D: str = "model.load"
D: bool = False


class DisplacementCtrl:
    """Apply a load to a pier until the displacement is reached.

    Args:
        displacement: float, displacement in meters.
        pier: int, index of a pier on a bridge.

    """
    def __init__(self, displacement: float, pier: int):
        self.displacement = displacement
        self.pier = pier


class PointLoad:
    """A load concentrated at a point.

    Args:
        x_frac: float, fraction of x position on bridge in [0 1].
        z_frac: float, fraction of z position on bridge in [0 1].
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
            vehicle or per axle, in kilo Newton. Not available as an attribute.
        axle_distances: List[float], distance between axles in meters.
        axle_width: float, width of the vehicle's axles in meters.

    Attrs:

        length: float, length of the vehicle in meters.
        num_axles: int, number of axles.
        total_kn: Callable[[], float], total load intensity in kilo Newton.
        kn_per_axle: Callable[[], [List[float]]], load intensity per axle in
            kilo Newton.

    """
    def __init__(
            self, kn: float, axle_distances: List[float], axle_width: float):
        self.axle_distances = axle_distances
        self.axle_width = axle_width
        self.length = sum(self.axle_distances)
        self.num_axles = len(self.axle_distances) + 1
        self.kn = kn
        if isinstance(self.kn, list):
            self.total_kn = lambda: sum(self.kn)
            self.kn_per_axle = lambda: self.kn
        else:
            self.total_kn = lambda: self.kn
            self.kn_per_axle = lambda: [
                (self.kn / self.num_axles) for _ in range(self.num_axles)]

    def cmap_norm(self, all_vehicles: List["Vehicle"], cmin=0, cmax=1):
        """The colormap and norm for coloring vehicles."""
        from plot import truncate_colormap
        cmap = truncate_colormap(cm.get_cmap("YlGn"), cmin, cmax)
        total_kns = [v.total_kn() for v in all_vehicles] + [self.total_kn()]
        norm = colors.Normalize(vmin=min(total_kns), vmax=max(total_kns))
        return cmap, norm

    def color(self, all_vehicles: List["Vehicle"]):
        """Color of this vehicle scaled based on given vehicles."""
        cmap, norm = self.cmap_norm(all_vehicles)
        if len(all_vehicles) == 0:
            return cmap(0.5)
        return cmap(norm(self.total_kn()))


class MvVehicle(Vehicle):
    """A moving vehicle, has a speed and position on a bridge.

    Position is determined by an initial position in the longitudinal direction
    of the bridge, by an index to a lane on that bridge and by a constant speed.

    NOTE: Arguments that determine initial position, 'lane' and 'init_x_frac',
        are optional and may be set later.

    Args:
        kn: Union[float, List[float]], load intensity, either for the entire
            vehicle or per axle, in kilo Newton.
        axle_distances: List[float], distance between axles in meters.
        axle_width: float, width of the vehicle's axles in meters.
        kmph: float, speed of the vehicle in kmph.
        lane: Optional[int], index of a lane on a bridge.
        init_x_frac: Optional[float], initial position on the lane as a fraction
            of x position of the bridge, may be negative but not greater than 1.
            Regardless of the direction of traffic on the lane, the position at
            0 is just as the vehicle is about to move onto the bridge.

    Attrs:
        mps: float, speed of the vehicle in mps.
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
        self.mps = self.kmph / 3.6  # Meters per second.
        self.lane = lane
        self.init_x_frac = init_x_frac
        if self.init_x_frac is not None:
            assert self.init_x_frac <= 1

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

    def x_frac_at(self, time: float, bridge: Bridge) -> List[float]:
        """Fraction of x position of bridge in meters at given time.

        Args:
            time: float, time passed from initial position, in seconds.
            bridge: Bridge, bridge the vehicle is moving on.

        """
        delta_x_frac = (self.mps * time) / bridge.length
        init_x_frac = self.init_x_frac
        if bridge.lanes[self.lane].ltr:
            return init_x_frac + delta_x_frac
        else:
            init_x_frac *= -1  # Make positive, move to right of bridge.
            init_x_frac += 1  # Move one bridge length to the right.
            return init_x_frac - delta_x_frac

    def x_at(self, time: float, bridge: Bridge):
        """X position of bridge in meters at given time.

        Returns a list of x position for each axle.

        Args:
            time: float, time passed from initial position, in seconds.
            bridge: Bridge, bridge the vehicle is moving on.

        """
        return bridge.x(self.x_frac_at(time=time, bridge=bridge))

    def xs_at(self, time: float, bridge: Bridge):
        """X position of bridge for each axle in meters at given time."""
        xs = [self.x_at(time=time, bridge=bridge)]
        for axle_distance in self.axle_distances:
            delta_x = axle_distance
            if bridge.lanes[self.lane].ltr:
                delta_x *= -1
            xs.append(xs[-1] + delta_x)
        return xs

    def x_fracs_at(self, time: float, bridge: Bridge):
        """Fraction of x position of bridge for each axle at given time."""
        return list(map(bridge.x_frac, self.xs_at(time=time, bridge=bridge)))

    def on_bridge(self, time: float, bridge: Bridge) -> bool:
        """Whether a moving load is on a bridge at a given time."""
        x_fracs = list(map(bridge.x_frac, self.xs_at(time=time, bridge=bridge)))
        # Left-most and right-most vehicle positions as fractions.
        xl_frac, xr_frac = min(x_fracs), max(x_fracs)
        return 0 <= xl_frac <= 1 or 0 <= xr_frac <= 1

    def full_lanes(self, time: float, bridge: Bridge) -> float:
        """The amount of bridge lanes travelled by this vehicle."""
        x_fracs = list(map(bridge.x_frac, self.xs_at(time=time, bridge=bridge)))
        # Left-most and right-most vehicle positions as fractions.
        xl_frac, xr_frac = min(x_fracs), max(x_fracs)
        if bridge.lanes[self.lane].ltr:
            return xl_frac
        else:
            return abs(xr_frac - 1)

    def passed_bridge(self, time: float, bridge: Bridge) -> bool:
        """Whether the current vehicle has travelled over the bridge."""
        return self.full_lanes(time=time, bridge=bridge) > 1
