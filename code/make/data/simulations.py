from config import Config
from fem.responses.matrix.il import ILMatrix
from fem.run.opensees import OSRunner
from model.response import ResponseType


def run_uls(c: Config):
    """Run all unit load simulations."""
    wheel_zs = c.bridge.wheel_tracks(c)
    il_matrices = {
        wheel_z: ILMatrix.load(
            c=c,
            response_type=ResponseType.YTranslation,
            fem_runner=OSRunner(c),
            load_z_frac=c.bridge.z_frac(wheel_z),
            save_all=True,  # Default but let's be explicit.
        )
        for wheel_z in wheel_zs
    }
