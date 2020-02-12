"""Loads and vehicles"""
from itertools import chain
from typing import List, Optional, Tuple, Union

import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors

from config import Config
from model.bridge import Bridge, Point
from util import assert_sorted, flatten, round_m, safe_str

# Comment/uncomment to print debug statements for this file.
# D: str = "model.load"
D: bool = False


class PierSettlement:
    """Apply a load to a pier until a displacement is reached.

    Args:
        displacement: float, displacement in meters.
        pier: int, index of a pier on a bridge.

    """

    def __init__(self, displacement: float, pier: int):
        self.displacement = displacement
        self.pier = pier

    def id_str(self):
        return safe_str(f"{self.displacement:.3f}-{self.pier}")


class PointLoad:
    """A load concentrated at a point on the deck.

    Args:
        x_frac: float, fraction of x position on bridge in [0 1].
        z_frac: float, fraction of z position on bridge in [0 1].
        kn: float, load intensity in kilo Newton.

    """

    def __init__(self, x_frac: float, z_frac: float, kn: float):
        self.x_frac = x_frac
        self.z_frac = z_frac
        self.kn = kn

    def id_str(self):
        """String uniquely representing this load."""
        return f"({self.x_frac:.4f}, {self.z_frac:.4f}, {self.kn:.3f})"

    def repr(self, bridge: Bridge):
        x = round_m(bridge.x(self.x_frac))
        z = round_m(bridge.z(self.z_frac))
        return f"x={x}, z={z}, kN={self.kn}"

    def point(self, bridge: Bridge) -> Point:
        """A 'Point' on the deck from this 'PointLoad'."""
        return Point(x=bridge.x(self.x_frac), y=0, z=bridge.z(self.z_frac))


class Vehicle:
    """A vehicle's geometry.

    Args:
        kn: Union[float, List[float], List[Tuple[float, float]]], load
            intensity, either for the entire vehicle or per axle, or as a list
            of tuple (per wheel, each tuple is left then right wheel), in kilo
            Newton.
        axle_distances: List[float], distance between axles in meters.
        axle_width: float, width of the vehicle's axles in meters.

    Attrs:

        length: float, length of the vehicle in meters.
        num_axles: int, number of axles.
        total_kn: Callable[[], float], total load intensity in kilo Newton.
        kn_per_axle: Callable[[], [List[float]]], load intensity per axle in
            kilo Newton.
        # wheel_length: float, length of each wheel in meters, default 0.31 m.

    """

    def __init__(
        self,
        kn: Union[float, List[float], List[Tuple[float, float]]],
        axle_distances: List[float],
        axle_width: float,
    ):
        self.axle_distances = axle_distances
        self.axle_width = axle_width
        self.length = sum(self.axle_distances)
        self.num_axles = len(self.axle_distances) + 1
        self.num_wheels = self.num_axles * 2
        self.kn = kn
        # self.wheel_length = 0.31

        def total_kn():
            if isinstance(self.kn, list):
                if isinstance(self.kn[0], tuple):
                    return sum(chain.from_iterable(self.kn))
                return sum(self.kn)
            return self.kn

        def kn_per_axle():
            if isinstance(self.kn, list):
                if isinstance(self.kn[0], tuple):
                    return list(map(sum, self.kn))
                return self.kn
            return [(self.kn / self.num_axles) for _ in range(self.num_axles)]

        def kn_per_wheel():
            if isinstance(self.kn, list):
                if isinstance(self.kn[0], tuple):
                    return self.kn
                return list(map(lambda kn: (kn / 2, kn / 2), self.kn))
            wheel_kn = self.kn / self.num_wheels
            return [(wheel_kn, wheel_kn) for _ in range(self.num_axles)]

        self.total_kn = total_kn
        self.kn_per_axle = kn_per_axle
        self.kn_per_wheel = kn_per_wheel

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
        kn: Union[float, List[float], List[Tuple[float, float]]], load
            intensity, either for the entire vehicle or per axle, or as a list
            of tuple (per wheel, each tuple is left then right wheel), in kilo
            Newton.
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
        self,
        kn: Union[float, List[float], List[Tuple[float, float]]],
        axle_distances: List[float],
        axle_width: float,
        kmph: float,
        lane: Optional["Lane"] = None,
        init_x_frac: Optional[float] = None,
    ):
        super().__init__(kn=kn, axle_distances=axle_distances, axle_width=axle_width)
        self.kmph = kmph
        self.mps = self.kmph / 3.6  # Meters per second.
        self.lane = lane
        self.init_x_frac = init_x_frac
        if self.init_x_frac is not None:
            assert self.init_x_frac <= 1

    def wheel_tracks_zs(self, bridge: Bridge, meters: bool) -> Tuple[float, float]:
        """Positions of the vehicle's wheels in transverse direction.

        Args:
            bridge: Bridge, the bridge on which the vehicle is moving.
            meters: bool, whether to return positions in meters (True) or
                fractions (False) of the bridge width in [0 1].

        """
        lane = bridge.lanes[self.lane]
        tracks = [
            lane.z_center - (self.axle_width / 2),
            lane.z_center + (self.axle_width / 2),
        ]
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
            init_x_frac *= -1  # Make positive, move to right of bridge start.
            init_x_frac += 1  # Move one bridge length to the right.
            return init_x_frac - delta_x_frac

    def x_at(self, time: float, bridge: Bridge):
        """X position of front axle on bridge at given time, in meters.

        Args:
            time: float, time passed from initial position, in seconds.
            bridge: Bridge, bridge the vehicle is moving on.

        """
        return bridge.x(self.x_frac_at(time=time, bridge=bridge))

    def xs_at(self, time: float, bridge: Bridge):
        """X position of bridge for each axle in meters at given time."""
        xs = [self.x_at(time=time, bridge=bridge)]
        if not hasattr(self, "_delta_xs"):
            self._delta_xs = np.array(self.axle_distances)
            if bridge.lanes[self.lane].ltr:
                self._delta_xs *= -1
        for delta_x in self._delta_xs:
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

    def time_at(self, x, bridge: Bridge):
        """Time the front axle is at the given x position."""
        if not bridge.lanes[self.lane].ltr:
            raise NotImplementedError()
        init_x = bridge.x(self.init_x_frac)
        assert init_x < x
        return float(abs(init_x - x)) / self.mps

    def time_entering_bridge(self, bridge: Bridge):
        """Time the vehicle begins to enter the bridge."""
        init_x = bridge.x(self.init_x_frac)
        assert init_x <= 0
        return float(abs(init_x)) / self.mps

    def time_entered_bridge(self, bridge: Bridge):
        """Time the vehicle has entered the bridge."""
        init_x = bridge.x(self.init_x_frac)
        assert init_x <= 0
        return float(abs(init_x) + self.length) / self.mps

    def time_leaving_bridge(self, bridge: Bridge):
        """Time the vehicle begins to leave the bridge."""
        init_x = bridge.x(self.init_x_frac)
        assert init_x <= 0
        return float(abs(init_x) + bridge.length) / self.mps

    def time_left_bridge(self, bridge: Bridge):
        """Time the vehicle has left the bridge."""
        init_x = bridge.x(self.init_x_frac)
        assert init_x <= 0
        return float(abs(init_x) + bridge.length + self.length) / self.mps

    def wheel_to_wheel_track_xs(
        self, c: Config, wheel_load: PointLoad
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """X positions (and weighting) of unit loads for a given point load.

        This implements wheel track bucketing!

        """
        wheel_load_x = round_m(c.bridge.x(wheel_load.x_frac))
        wheel_track_xs = c.bridge.wheel_track_xs(c)
        unit_load_x_ind = np.searchsorted(wheel_track_xs, wheel_load_x)
        unit_load_x = lambda: wheel_track_xs[unit_load_x_ind]
        if unit_load_x() > wheel_load_x:
            unit_load_x_ind -= 1
        assert unit_load_x() <= wheel_load_x
        # If the unit load is an exact match just return it.
        if np.isclose(wheel_load_x, unit_load_x()):
            return ((wheel_load_x, 1), (0, 0))
        # Otherwise, return a combination of two unit loads. In this case the
        # unit load's position is less than the wheel.
        unit_load_x_lo = unit_load_x()
        unit_load_x_hi = wheel_track_xs[unit_load_x_ind + 1]
        assert unit_load_x_hi > wheel_load_x
        dist_lo = abs(unit_load_x_lo - wheel_load_x)
        dist_hi = abs(unit_load_x_hi - wheel_load_x)
        dist = dist_lo + dist_hi
        return ((unit_load_x_lo, dist_hi / dist), (unit_load_x_hi, dist_lo / dist))

    def to_wheel_track_loads(
        self, c: Config, time: float, flat: bool = False
    ) -> List[Tuple[Tuple[PointLoad, PointLoad], Tuple[PointLoad, PointLoad]]]:
        """Point loads per wheel, per axle. "Bucketed" based on unit loads.

        NOTE: In each tuple of two point loads, one tuple per wheel, each point
        load is for a unit load position in the wheel track. Each point load is
        weighted by the distance to the unit load.

        """
        result = []
        for axle_loads in self.to_point_load_pw(time=time, bridge=c.bridge):
            result.append([])
            # Each 'wheel_load' is directly under the wheel center.
            for wheel_load in axle_loads:
                result[-1].append([])
                # Split that wheel load up, into one load per bin.
                for (load_x, load_frac) in self.wheel_to_wheel_track_xs(
                    c=c, wheel_load=wheel_load
                ):
                    if load_frac > 0:
                        result[-1][-1].append(
                            PointLoad(
                                x_frac=c.bridge.x_frac(load_x),
                                z_frac=wheel_load.z_frac,
                                kn=wheel_load.kn * load_frac,
                            )
                        )
        if flat:
            return flatten(result, PointLoad)
        return result

    def to_point_load_pw(
        self, time: float, bridge: Bridge, flat: bool = False
    ) -> List[Tuple[PointLoad, PointLoad]]:
        """A tuple of point load per axle, one point load per wheel.

        TODO: Multiply wheel by amount on the bridge. Or maybe just ignore the
        wheel print altogether?

        wheel_x_center = c.bridge.x(wheel_load.x_frac)
        wheel_x_lo, wheel_x_hi = [
            wheel_x_center - (self.wheel_length / 2),
            wheel_x_center + (self.wheel_length / 2),
        ]

        """
        z0, z1 = self.wheel_tracks_zs(bridge=bridge, meters=False)
        assert z0 < z1
        if bridge.lanes[self.lane].ltr:
            z0, z1 = z1, z0
        kn_per_wheel = list(chain.from_iterable(self.kn_per_wheel()))

        i = 0

        def next_kn():
            nonlocal i
            i += 1
            return kn_per_wheel[i - 1]

        result = []
        # For each axle..
        for x in self.xs_at(time=time, bridge=bridge):
            if x < bridge.x_min or x > bridge.x_max:
                continue
            # ..two wheel load intensities.
            kn0, kn1 = next_kn(), next_kn()
            x_frac = bridge.x_frac(x)
            result.append(
                (
                    PointLoad(x_frac=x_frac, z_frac=z0, kn=kn0),
                    PointLoad(x_frac=x_frac, z_frac=z1, kn=kn1),
                )
            )
        if flat:
            return flatten(result, PointLoad)
        return result
