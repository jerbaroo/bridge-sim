from typing import Optional

from bridge_sim.model import Config, ResponseType, Point
from bridge_sim.util import print_i
from lib.classify.scenario.bridge import (
    transverse_crack,
    healthy_damage_w_transverse_crack_nodes,
)
from lib.fem.responses.matrix.dc import DCExpt
from lib.fem.responses.matrix.il import ILExpt
from lib.fem.run.opensees import OSRunner


def run_uls(
    c: Config,
    piers: bool,
    healthy: bool,
    cracked: bool,
    crack_x: Optional[int] = None,
    crack_length: Optional[int] = None,
):
    """Run all unit load simulations."""

    def crack_f():
        return transverse_crack(at_x=crack_x, length=crack_length)

    print_i(
        f"Running simulations with crack zone at x = {crack_x}, length = {crack_length}"
    )

    response_type = ResponseType.YTranslation
    if piers:
        # Pier settlement.
        list(DCExpt.load(c=c, response_type=response_type, fem_runner=OSRunner(c)))
    if healthy:
        c = healthy_damage_w_transverse_crack_nodes(crack_f=crack_f).use(c)[0]
        # Unit load simulations (healthy bridge).
        ILExpt.load_wheel_tracks(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            wheel_zs=c.bridge.wheel_track_zs(c),
            run_only=True,
        )
    elif cracked:
        # Unit load simulations (cracked bridge).
        c = crack_f().use(c)[0]
        ILExpt.load_wheel_tracks(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            wheel_zs=c.bridge.wheel_track_zs(c),
            run_only=True,
        )


def run_ulm(c: Config, healthy: bool, cracked: bool, x_i: float, z_i: float):
    """Run all unit load simulations."""
    response_type = ResponseType.YTranslation
    wheel_xs = c.bridge.wheel_track_xs(c)
    wheel_x = wheel_xs[x_i]
    wheel_zs = c.bridge.wheel_track_zs(c)
    wheel_z = wheel_zs[z_i]
    print_i(f"Wheel (x, z) = ({wheel_x}, {wheel_z})")
    point = Point(x=wheel_x, y=0, z=wheel_z)
    if healthy:
        ILExpt.load_ulm(
            c=c, response_type=response_type, points=[point], sim_runner=OSRunner(c),
        )
    if cracked:
        c = transverse_crack().use(c)[0]
        ILExpt.load_ulm(
            c=c, response_type=response_type, points=[point], sim_runner=OSRunner(c),
        )
