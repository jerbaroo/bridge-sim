from classify.scenario.bridge import transverse_crack
from config import Config
from fem.responses.matrix.il import ILMatrix
from fem.responses.matrix.dc import DCMatrix
from fem.run.opensees import OSRunner
from model.response import ResponseType


def run_uls(c: Config, piers: bool, healthy: bool, cracked: bool):
    """Run all unit load simulations."""
    response_type = ResponseType.YTranslation
    if piers:
        # Pier settlement.
        list(DCMatrix.load(
            c=c, response_type=response_type, fem_runner=OSRunner(c)
        ))
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
