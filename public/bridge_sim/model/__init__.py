from lib.config import Config as LibConfig
from lib.model.load import PointLoad as LibPointLoad
from lib.model.load import PierSettlement as LibPierSettlement
from lib.model.response import ResponseType

RT = ResponseType


def PierSettlement(pier: int, settlement: float) -> LibPierSettlement:
    """Apply a load to a pier until a vertical translation is reached.

    Args:
        pier: int, index of a pier on a bridge.
        settlement: float, pier settlement in meters.

    """
    return LibPierSettlement(settlement, pier)


def PointLoad(config: LibConfig, x: float, z: float, kn: float):
    """A point load at a position on a bridge deck.

    Args:
        bridge: Bridge, temporarily needed.
        x: float, x position on bridge.
        z: float, z position on bridge.
        kn: float, load intensity.

    """
    return LibPointLoad(
        x_frac=config.bridge.x_frac(x), z_frac=config.bridge.z_frac(z), kn=kn,
    )
