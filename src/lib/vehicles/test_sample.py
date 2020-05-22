"""Test the sampling of vehicles."""
from model.load import Vehicle
from model.bridge.bridge_705 import bridge_705_2d, bridge_705_test_config
from vehicles.sample import noise_col_names, sample_vehicle
from util import print_d

# Print debug information for this file.
D: bool = False


def test_sample_vehicle():
    c = bridge_705_test_config(bridge_705_2d)
    c.vehicle_density = [(11.5, 0.7), (12.2, 0.2), (43, 0.1)]

    # Test a vehicles is returned.
    vehicle = sample_vehicle(c)
    print_d(D, vehicle)
    assert isinstance(vehicle, Vehicle)

    # Test noise is added.
    _, vehicle = sample_vehicle(c=c, pd_row=True)
    true_vehicle = c.vehicle_data.loc[vehicle.index]
    for col_name in noise_col_names:
        # DataFrame is only of length 1, still need .all applied.
        assert (
            vehicle.loc[vehicle.index, col_name]
            != c.vehicle_data.loc[vehicle.index, col_name]
        ).all()

    # Test noise is not added.
    c.perturb_stddev = 0
    _, vehicle = sample_vehicle(c=c, pd_row=True)
    true_vehicle = c.vehicle_data.loc[vehicle.index]
    for col_name in noise_col_names:
        # DataFrame is only of length 1, still need .all applied.
        assert (
            vehicle.loc[vehicle.index, col_name]
            == c.vehicle_data.loc[vehicle.index, col_name]
        ).all()
