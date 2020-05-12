from lib.config import Config as LibConfig
from lib.model.load import PointLoad as LibPointLoad
from lib.model.load import PierSettlement as LibPierSettlement
from lib.model.response import ResponseType

RT = ResponseType


def PierSettlement(pier: int, settlement: float) -> LibPierSettlement:
    """Apply a load to a pier until a vertical translation is reached.

    Args:
        pier: int, index of a pier on a bridge.
        settlement: float, quantity of pier settlement.

    """
    return LibPierSettlement(settlement, pier)


def PointLoad(config: LibConfig, x: float, z: float, load: float):
    """A point load at a position on a bridge deck.

    Args:
        config: LibConfig, will not be necessary in future version.
        x: float, x position on a bridge.
        z: float, z position on a bridge.
        load: float, load intensity.

    """
    return LibPointLoad(
        x_frac=config.bridge.x_frac(x), z_frac=config.bridge.z_frac(z), kn=load,
    )
