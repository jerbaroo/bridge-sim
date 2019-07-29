"""Test the sampling of vehicles."""
from model.bridge_705 import bridge_705_config
from vehicles.sample import noise_col_names, sample_vehicle


def test_sample_vehicle():
    c = bridge_705_config()
    c.vehicle_density = [(11.5, 0.7), (12.2, 0.2), (43, 0.1)]

    # Test noise is added.
    vehicle = sample_vehicle(c)
    true_vehicle = c.vehicle_data.loc[vehicle.index]
    for col_name in noise_col_names:
        # DataFrame is only of length 1, still need .all applied.
        assert (vehicle.loc[vehicle.index, col_name] !=
                c.vehicle_data.loc[vehicle.index, col_name]).all()

    # Test noise is not added.
    vehicle = sample_vehicle(c, noise_stddevs=0)
    true_vehicle = c.vehicle_data.loc[vehicle.index]
    for col_name in noise_col_names:
        # DataFrame is only of length 1, still need .all applied.
        assert (vehicle.loc[vehicle.index, col_name] ==
                c.vehicle_data.loc[vehicle.index, col_name]).all()
