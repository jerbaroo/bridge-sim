"""Test creep calculation."""

import numpy as np

from bridge_sim import bridges, configs, creep, model, shrinkage, sim
from bridge_sim.util import convert_times


def test_creep_non_negative():
    config, exe_found = configs.test_config(msl=10)
    seconds = convert_times(f="day", t="second", times=np.arange(365))
    strain = creep.creep_coeff(config, shrinkage.CementClass.Normal, times=seconds, x=51)
    assert strain[0] == 0


def test_install_day():
    _, exe_found = configs.test_config(msl=10)
    config = configs.opensees_default(bridges.bridge_705(msl=10))
    if not exe_found:
        return
    point = model.Point(x=48)
    traffic_array = np.zeros((1, config.il_num_loads * len(config.bridge.lanes)))
    responses_array = np.zeros((1, 1))
    response_type = model.RT.YTrans
    install_day = 37
    start_day = 10 * 365
    end_day = start_day + 1
    # Creep due to shrinkage.
    c1 = sim.responses.to_creep(
        config=config,
        points=[point],
        responses_array=responses_array,
        response_type=response_type,
        install_day=install_day,
        start_day=start_day,
        end_day=end_day,
        self_weight=True,
        shrinkage=True,
    )
    _0, _1, _2, _3, c2 = sim.responses.to(
        config=config,
        points=[point],
        traffic_array=traffic_array,
        response_type=response_type,
        with_creep=True,
        install_day=install_day,
        start_day=start_day,
        end_day=end_day,
        ret_all=True
    )
    assert (c2 == c1).all()
