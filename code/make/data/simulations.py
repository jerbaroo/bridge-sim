from config import Config
from fem.responses.matrix.il import ILMatrix
from fem.run.opensees import OSRunner
from model.response import ResponseType


def run_uls(c: Config):
    """Run all unit load simulations."""
    ILMatrix.load_uls(
        c=c,
        response_type=ResponseType.YTranslation,
        sim_runner=OSRunner(c),
        wheel_zs=c.bridge.wheel_tracks(c),
        save_all=True,  # Default but let's be explicit.
    )
