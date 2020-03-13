from classify.scenario.bridge import transverse_crack
from config import Config
from fem.responses.matrix.il import ILMatrix
from fem.responses.matrix.dc import DCMatrix
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.response import ResponseType
from util import print_i


def run_uls(c: Config, piers: bool, healthy: bool, cracked: bool):
    """Run all unit load simulations."""
    response_type = ResponseType.YTranslation
    if piers:
        # Pier settlement.
        list(DCMatrix.load(c=c, response_type=response_type, fem_runner=OSRunner(c)))
    if healthy:
        # Unit load simulations (healthy bridge).
        ILMatrix.load_wheel_tracks(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            wheel_zs=c.bridge.wheel_track_zs(c),
            run_only=True,
        )
    if cracked:
        # Unit load simulations (cracked bridge).
        c = transverse_crack().use(c)[0]
        ILMatrix.load_wheel_tracks(
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
        ILMatrix.load_ulm(
            c=c,
            response_type=response_type,
            points=[point],
            sim_runner=OSRunner(c),
        )
    if cracked:
        c = transverse_crack().use(c)[0]
        ILMatrix.load_ulm(
            c=c,
            response_type=response_type,
            points=[point],
            sim_runner=OSRunner(c),
        )
