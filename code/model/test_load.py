from model.bridge.bridge_705 import bridge_705_3d, bridge_705_config
from model.load import MvVehicle, Vehicle

c = bridge_705_config(bridge_705_3d)

get_wagen1 = lambda: MvVehicle(
    kn=[(5050, 5300), (4600, 4000), (4350, 3700), (4050, 3900)],
    axle_distances=[3.6, 1.32, 1.45],
    axle_width=2.5,
    kmph=40,
    lane=0,
    init_x_frac=0
)


def test_mv_vehicle_to_point_loads():
    wagen1 = get_wagen1()
    loads = wagen1.to_point_loads(time=2, bridge=c.bridge)
    assert len(loads) == 4
    assert loads[0][0].kn == 5050
    assert loads[0][1].kn == 5300
    assert loads[0][0].z_frac > loads[0][1].z_frac


def test_mv_vehicle_time_at():
    wagen1 = get_wagen1()
    mps = wagen1.kmph / 3.6
    assert wagen1.time_at(x=20, bridge=c.bridge) == 20 / mps
    assert wagen1.time_at(x=102.75, bridge=c.bridge) == 102.75 / mps


def test_mv_vehicle_enters_bridge():
    pass
