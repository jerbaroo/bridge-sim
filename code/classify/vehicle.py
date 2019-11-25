from model.load import MvVehicle

# Wagen 1 from the experimental campaign.
to_kn = 0.00980665
wagen1 = MvVehicle(
    kn=[
        (5050 * to_kn, 5300 * to_kn),
        (4600 * to_kn, 4000 * to_kn),
        (4350 * to_kn, 3700 * to_kn),
        (4050 * to_kn, 3900 * to_kn),
    ],
    axle_distances=[3.6, 1.32, 1.45],
    axle_width=2.5,
    kmph=40,
    lane=0,
    init_x_frac=0,
)
