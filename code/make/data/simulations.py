from config import Config
from fem.responses.matrix.il import ILMatrix
from fem.responses.matrix.dc import DCMatrix
from fem.run.opensees import OSRunner
from model.response import ResponseType


def run_uls(c: Config):
    """Run all unit load simulations."""
    response_type = ResponseType.YTranslation
    ILMatrix.load_wheel_tracks(
        c=c,
        response_type=response_type,
        sim_runner=OSRunner(c),
        wheel_zs=c.bridge.wheel_track_zs(c),
        run_only=True,
    )
    list(DCMatrix.load(
        c=c, response_type=response_type, fem_runner=OSRunner(c)
    ))
