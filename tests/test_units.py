"""Test that responses have correct units/magnitude.

The tests in "test_unit_load" are regression tests for simulations run directly
with OpenSees, to ensure that the response is the same as it was before. This
file instead tests that different methods of calculating responses all return
responses in the same units e.g. strain and not microstrain, m and not mm. There
is some duplication between these files I guess, but "shur look".

"""

from copy import deepcopy

import numpy as np

from bridge_sim import configs, model, sim, temperature, traffic, vehicles

config, exe_found = configs.test_config(msl=5)
config.shorten_paths = True


def test_to_traffic_array():
    return
    if not exe_found:
        return
    _0, _1, ta = traffic.load_traffic(config, traffic.normal_traffic(config), 10)
    responses = sim.responses.to_traffic_array(
        config=config,
        traffic_array=ta,
        response_type=model.RT.YTrans,
        points=[model.Point(x=10, z=-8.4)],
    )
    assert np.amin(responses) == -0.001


def test_point_loads():
    if not exe_found:
        return
    x = config.bridge.x_center
    time = vehicles.truck1.time_at(x=x, bridge=config.bridge)
    point_loads = vehicles.truck1.wheel_track_loads(config=config, times=[time])[0]
    y_responses = sim.responses.load(
        config=config, response_type=model.RT.YTrans, point_loads=point_loads, run=True
    )
    y_response = y_responses.at_decks([model.Point(x=x, z=-8.4)])[0]
    assert y_response == -0.0003048905  # Metre.
    s_responses = sim.responses.load(
        config=config, response_type=model.RT.StrainXXB, point_loads=point_loads,
    )
    s_response = s_responses.at_decks([model.Point(x=x, z=-8.4)])[0]
    assert s_response == 8.321818e-06  # Strain.


def test_uniform_temp_load():
    if not exe_found:
        return
    temp_deltas = (1, None)
    y_responses = sim.responses.load(
        config=config, response_type=model.RT.YTrans, temp_deltas=temp_deltas, run=True,
    )
    y_response = y_responses.at_decks([model.Point(x=config.bridge.x_center)])[0]
    assert y_response == 7.37182e-05  # Metre.
    s_responses = sim.responses.load(
        config=config, response_type=model.RT.StrainXXB, temp_deltas=temp_deltas,
    )
    s_response = s_responses.at_decks([model.Point(x=config.bridge.x_center)])[0]
    assert s_response == 9.06927625e-06  # Strain.
    s_post_responses = deepcopy(s_responses).add_temp_strain(config, temp_deltas)
    s_post_response = s_post_responses.at_decks([model.Point(x=config.bridge.x_center)])[0]
    assert s_post_response == -2.9307237500000006e-06
    strain_responses = deepcopy(s_post_responses).to_stress(config.bridge)
    assert max(strain_responses.values()) == 0.17815742399999993
    assert min(strain_responses.values()) == -0.18672204800249995


def test_linear_temp_load():
    if not exe_found:
        return
    temp_deltas = (None, 1)
    y_responses = sim.responses.load(
        config=config, response_type=model.RT.YTrans, temp_deltas=temp_deltas, run=True,
    )
    y_response = y_responses.at_decks([model.Point(x=config.bridge.x_center)])[0]
    assert y_response == 1.30414e-05  # Metre.
    s_responses = sim.responses.load(
        config=config, response_type=model.RT.StrainXXB, temp_deltas=temp_deltas,
    )
    s_response = s_responses.at_decks([model.Point(x=config.bridge.x_center)])[0]
    assert np.isclose(s_response, -4.8807424e-07)  # Strain.
    s_post_responses = deepcopy(s_responses).add_temp_strain(config, temp_deltas)
    s_post_response = s_post_responses.at_decks([model.Point(x=config.bridge.x_center)])[0]
    assert s_post_response == 5.51192576e-06
    strain_responses = deepcopy(s_post_responses).to_stress(config.bridge)
    assert max(strain_responses.values()) == 0.35262588936582
    assert min(strain_responses.values()) == 0.01336460966400001  # Should be close to 0.


def test_pier_settlement():
    if not exe_found:
        return
    y_responses = sim.responses.load(
        config=config, response_type=model.RT.YTrans,
        pier_settlement=[model.PierSettlement(pier=5, settlement=1)], run=True,
    )
    assert min(y_responses.values()) == -1.01501  # Metre. Should be close to -1.
    assert max(y_responses.values()) == 0.093416  # Metre.
    s_responses = sim.responses.load(
        config=config, response_type=model.RT.StrainXXB,
        # 10 millimeters.
        pier_settlement=[model.PierSettlement(pier=5, settlement=10 / 1000)],
    )
    assert min(s_responses.values()) == -5.68946825e-05  # Strain.
    assert max(s_responses.values()) == 8.4176429e-05  # Strain.


def test_temp_effect():
    if not exe_found:
        return
    weather = temperature.load("holly-springs-19")
    effect = temperature.effect(
        config=config,
        response_type=model.RT.YTrans,
        points=[model.Point(x=config.bridge.x_center)],
        weather=weather,
    )[0]
    assert effect[-1] == 0.0006522767883093816  # Metre.
    effect = temperature.effect(
        config=config,
        response_type=model.RT.StrainXXB,
        points=[model.Point(x=config.bridge.x_center)],
        weather=weather,
    )[0]
    assert effect[-1] == -3.03602389200358e-05  # Strain.


def test_to_pier_settlement():
    if not exe_found:
        return
    responses_array = np.zeros((1, 1))  # One point and one timestep.
    responses = sim.responses.to_pier_settlement(
        config=config,
        points=[model.Point(x=config.bridge.supports[4].x, z=config.bridge.supports[4].z)],
        responses_array=responses_array,
        response_type=model.ResponseType.YTrans,
        pier_settlement=[(model.PierSettlement(pier=4, settlement=1), model.PierSettlement(pier=4, settlement=1))],
    )
    assert np.isclose(responses[0][0], -0.9819369)  # Metre.
    responses = sim.responses.to_pier_settlement(
        config=config,
        points=[model.Point(x=config.bridge.supports[4].x, z=config.bridge.supports[4].z)],
        responses_array=responses_array,
        response_type=model.ResponseType.StrainXXB,
        # 10 mm.
        pier_settlement=[(
            model.PierSettlement(pier=4, settlement=10 / 1E3),
            model.PierSettlement(pier=4, settlement=10 / 1E3),
        )],
    )
    assert np.isclose(responses[0][0], 2.2771967865779597e-05)  # Strain


def test_to_temperature():
    if not exe_found:
        return
    responses_array = np.zeros((1, 1))  # One point and one timestep.
    weather = temperature.load("holly-springs-19")
    responses = sim.responses.to_temperature(
        config=config,
        points=[model.Point(config.bridge.x_center)],
        responses_array=responses_array,
        response_type=model.ResponseType.YTrans,
        weather=weather,
        start_date="14/05/2019 00:00",
        end_date="15/05/2019 00:00",
    )
    assert np.isclose(responses[0][0], 0.001714997507674702)  # Metre.
    responses = sim.responses.to_temperature(
        config=config,
        points=[model.Point(config.bridge.x_center)],
        responses_array=responses_array,
        response_type=model.ResponseType.StrainXXB,
        weather=weather,
        start_date="14/05/2019 00:00",
        end_date="15/05/2019 00:00",
    )
    assert np.isclose(responses[0][0], -1.4587014932072391e-05)  # Strain.


def test_to_shrinkage():
    if not exe_found:
        return
    responses_array = np.zeros((1, 1))  # One point and one timestep.
    responses = sim.responses.to_shrinkage(
        config=config,
        points=[model.Point(config.bridge.x_center)],
        responses_array=responses_array,
        response_type=model.ResponseType.YTrans,
        start_day=100,
        end_day=101,
    )
    assert np.isclose(responses[0][0], 0.00036038554721046413)  # Metre.
    responses = sim.responses.to_shrinkage(
        config=config,
        points=[model.Point(config.bridge.x_center)],
        responses_array=responses_array,
        response_type=model.ResponseType.StrainXXB,
        start_day=100,
        end_day=101,
    )
    assert np.isclose(responses[0][0], 4.433689488022111e-05)  # Strain.

