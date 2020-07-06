"""Add crack zones to bridges."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, List, Tuple, Optional

import numpy as np

from bridge_sim.model import Bridge, Material, Point, Config
from bridge_sim.util import print_i, safe_str


@dataclass
class CrackZone:
    """An area of cracking on a bridge deck."""

    x_min: float
    z_min: float
    x_max: float
    z_max: float


class CrackDeck:
    def __init__(
        self,
        name: str,
        crack_zone: Callable[[Bridge], CrackZone],
        add_xs: List[float] = np.arange(start=0, stop=2, step=0.05),
    ):
        """A function to add a crack zone to a bridge.

        Args:
            name: identifying name for the type of cracking.
            crack_zone: function that returns a crack zone to apply.
            add_xs: distances from the crack zone to add additional nodes in the
                X direction (both sides of the crack zone but not in the Z
                direction).

        """
        self.name = name
        self.crack_zone = crack_zone
        self.add_xs = add_xs

    def crack(self, config: Config):
        """Return a Config (deepcopied) with a cracked Bridge."""
        config = deepcopy(config)
        bridge = config.bridge
        bridge.data_id = self.name
        self._crack_deck(bridge)  # Add cracked materials.
        # Add additional nodes as requested.
        crack_zone = self.crack_zone(bridge)
        xs_lo = (self.add_xs * -1) + crack_zone.x_min
        xs_hi = self.add_xs + crack_zone.x_max
        bridge.additional_xs = np.concatenate([xs_lo, xs_hi])
        print_i(f"Additional X positions of nodes for cracking:")
        print_i(f"    {bridge.additional_xs}")
        return config

    def _crack_deck(self, bridge: Bridge):
        """Add cracked materials to a bridge's deck."""
        cz = self.crack_zone(bridge)
        c_x_start, c_z_start, c_x_end, c_z_end = [
            cz.x_min,
            cz.z_min,
            cz.x_max,
            cz.z_max,
        ]
        if callable(bridge.sections):
            raise NotImplementedError()
        # Find where the cracked area and current sections overlap.
        overlaps: List[Tuple[Material, float, float, float, float]] = []
        for section in bridge.sections:
            s_x_start = bridge.x(section.start_x_frac)
            s_z_start = bridge.z(section.start_z_frac)
            s_x_end = bridge.x(section.end_x_frac)
            s_z_end = bridge.z(section.end_z_frac)
            overlap_x_start = max(c_x_start, s_x_start)
            overlap_z_start = max(c_z_start, s_z_start)
            overlap_x_end = min(c_x_end, s_x_end)
            overlap_z_end = min(c_z_end, s_z_end)
            overlap_x = overlap_x_end - overlap_x_start
            overlap_z = overlap_z_end - overlap_z_start
            if overlap_x > 0 and overlap_z > 0:
                overlaps.append(
                    (
                        section,
                        overlap_x_start,
                        overlap_z_start,
                        overlap_x_end,
                        overlap_z_end,
                    )
                )
        # Create new cracked sections for each of these overlaps.
        cracked_sections, max_id = [], 1000000
        for i, (section, x_start, z_start, x_end, z_end) in enumerate(overlaps):
            cracked_section = deepcopy(section)
            cracked_section.id = max_id + i + 1
            y_x = cracked_section.youngs_x()
            cracked_section.youngs_x = lambda: 0.5 * y_x
            cracked_section.start_x_frac = bridge.x_frac(x_start)
            cracked_section.start_z_frac = bridge.z_frac(z_start)
            cracked_section.end_x_frac = bridge.x_frac(x_end)
            cracked_section.end_z_frac = bridge.z_frac(z_end)
            cracked_sections.append(cracked_section)
        bridge.sections = cracked_sections + bridge.sections

    def without(self, bridge: Bridge, thresh: float = 0):
        """Return a function to reject non crack area points."""
        cz = self.crack_zone(bridge)
        c_x_start, c_z_start, c_x_end, c_z_end = [
            cz.x_min,
            cz.z_min,
            cz.x_max,
            cz.z_max,
        ]
        if thresh != 0:
            c_x_start -= thresh
            c_z_start -= thresh
            c_x_end += thresh
            c_z_end += thresh

        def reject(point: Point) -> Point:
            return (
                point.x < c_x_start
                or point.x > c_x_end
                or point.z < c_z_start
                or point.z > c_z_end
            )

        return reject


def transverse_crack(
    length: float = 0.5,
    width: Optional[float] = None,
    at_x: Optional[float] = None,
    at_z: Optional[float] = None,
) -> CrackDeck:
    """A bridge with a transverse crack on the deck."""

    def crack_zone(bridge: Bridge) -> CrackZone:
        nonlocal width
        nonlocal at_x
        nonlocal at_z
        if width is None:
            width = bridge.width / 2
        if at_x is None:
            at_x = bridge.x_min + (bridge.length / 2)
        if at_z is None:
            at_z = bridge.z_min
        return CrackZone(
            x_min=at_x, z_min=at_z, x_max=at_x + length, z_max=at_z + width,
        )

    return CrackDeck(
        name=safe_str(f"tcrack-{length}-{width}-{at_x}-{at_z}"), crack_zone=crack_zone,
    )
