"""Provided instances of the Bridge class."""

from bridge_sim.bridges.bridge_705 import bridge_705
from bridge_sim.model import Support, Lane, MaterialDeck, MaterialSupport, Bridge


def bridge_narrow() -> Bridge:
    """Narrow example bridge with one supporting pier."""
    return Bridge(
        name="example",
        msl=0.2,
        length=20,
        width=5,
        supports=[
            Support(
                x=10,
                z=0,
                length=2,
                height=2,
                width_top=2,
                width_bottom=2,
                materials=[
                    MaterialSupport(
                        density=0.7,
                        thickness=0.7,
                        youngs=40000,
                        poissons=0.2,
                        start_frac_len=0,
                    )
                ],
                fix_z_translation=True,
                fix_x_translation=True,
            )
        ],
        materials=[MaterialDeck(thickness=0.7, youngs=40000, poissons=0.2,)],
        lanes=[Lane(-1, 1, True)],
    )


def bridge_wide() -> Bridge:
    """Wide example bridge with two supporting piers."""
    return Bridge(
        name="wide",
        msl=0.2,
        length=20,
        width=10,
        supports=[
            Support(
                x=5,
                z=0,
                length=2,
                height=2,
                width_top=2,
                width_bottom=2,
                materials=[
                    MaterialSupport(
                        density=0.7,
                        thickness=0.7,
                        youngs=40000,
                        poissons=0.2,
                        start_frac_len=0,
                    )
                ],
                fix_z_translation=True,
                fix_x_translation=True,
            ),
            Support(
                x=15,
                z=0,
                length=2,
                height=2,
                width_top=2,
                width_bottom=2,
                materials=[
                    MaterialSupport(
                        density=0.7,
                        thickness=0.7,
                        youngs=40000,
                        poissons=0.2,
                        start_frac_len=0,
                    )
                ],
                fix_z_translation=True,
                fix_x_translation=True,
            ),
        ],
        materials=[MaterialDeck(thickness=0.7, youngs=40000, poissons=0.2,)],
        lanes=[Lane(-4, -1, True), Lane(1, 4, True),],
    )


__all__ = ["bridge_705", "bridge_narrow", "bridge_wide"]
