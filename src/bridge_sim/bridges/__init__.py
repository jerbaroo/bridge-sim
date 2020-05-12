from lib.model.bridge import Bridge, Lane, Support, MaterialDeck, MaterialSupport


def bridge_example() -> Bridge:
    return Bridge(
        name="example",
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
                sections=[
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
    return Bridge(
        name="wide",
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
                sections=[
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
                sections=[
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
        lanes=[
            Lane(-4, -3, True),
            Lane(-2, -1, True),
            Lane(1, 2, True),
            Lane(3, 4, True),
        ],
    )
