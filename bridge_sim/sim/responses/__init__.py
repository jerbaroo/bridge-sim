"""High-level API for saving/loading responses from FE simulation."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Tuple

import bridge_sim
import numpy as np
import pandas as pd
from bridge_sim import temperature, util, creep
from bridge_sim.crack import CrackDeck

from bridge_sim.model import (
    Config,
    ResponseType,
    Point,
    PointLoad,
    Vehicle,
    PierSettlement,
)
from bridge_sim.shrinkage import CementClass
from bridge_sim.sim.model import SimParams, Responses
from bridge_sim.sim.run import load_expt_responses, load_fem_responses, load_ulm
from bridge_sim.traffic import TrafficArray
from bridge_sim.util import flatten, print_i, print_w, convert_times

D: str = "sim.responses"
# D: bool = False


def load(
    config: Config,
    response_type: ResponseType,
    point_loads: List[PointLoad] = [],
    pier_settlement: List[PierSettlement] = [],
    temp_deltas: Tuple[Optional[float], Optional[float]] = (None, None),
    self_weight: bool = False,
    run: bool = False,
) -> Responses:
    """Responses from a single linear simulation.

    The simulation is only run if results are not found on disk. Note that for
    temperature loading no post-processing is done.

    Args:
        config: simulation configuration object.
        response_type: sensor response type to return.
        point_loads: a list of point-loads to apply.
        pier_settlement: a pier settlement to apply.
        temp_deltas: uniform and linear temperature components.
        self_weight: add loads corresponding to structure self weight.
        run: force the simulation to run even if data already generated.

    """
    return load_fem_responses(
        c=config,
        sim_params=SimParams(
            ploads=point_loads,
            pier_settlement=pier_settlement,
            axial_delta_temp=temp_deltas[0],
            moment_delta_temp=temp_deltas[1],
            self_weight=self_weight,
        ),
        response_type=response_type,
        run=run,
    )


def to_traffic_array(
    config: Config,
    traffic_array: TrafficArray,
    response_type: ResponseType,
    points: List[Point],
):
    """Responses to a traffic array at some points.

    Args:
        config: Config, simulations configuration object.
        traffic_array: traffic array to calculate responses to.
        response_type: the type of sensor response.
        points: points at which to calculate responses.

    Returns: NumPY array indexed first by point then time.

    """
    ulm = load_ulm(config, response_type, points)
    assert ulm.shape[1] == len(points)
    assert traffic_array.shape[1] == ulm.shape[0]
    print(traffic_array.shape, ulm.shape)
    return np.matmul(traffic_array, ulm).T


def to_loads_direct(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    loads: List[List[PointLoad]],
):
    """Responses to point-loads over time (via direct simulation)."""
    expt_responses = load_expt_responses(
        c=c,
        expt_params=[SimParams(ploads=loads_) for loads_ in loads],
        response_type=response_type,
    )
    return np.array(
        [sim_responses.at_decks(points) for sim_responses in expt_responses]
    )


def to_vehicles_direct(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    vehicles: List[Vehicle],
    times: List[float],
):
    """Responses to vehicles over time (via direct simulation)."""
    loads = [
        flatten([v.point_load_pw(config=c, time=time) for v in vehicles], PointLoad)
        for time in times
    ]
    # loads = [v.point_load_pw(c) for v in vehicles]
    # loads_per_time = [[] for _ in times]
    # for v_loads in loads:
    #     for t, t_loads in enumerate(v_loads):
    #         loads_per_time[t] += t_loads
    # loads_per_time = [flatten(v_loads, PointLoad) for v_loads in loads_per_time]
    # print([len(load_) for load_ in loads_per_time])
    # print(loads_per_time[0])
    # print(loads_per_time[-1])
    assert isinstance(loads, list)
    assert isinstance(loads[0], list)
    assert isinstance(loads[0][0], PointLoad)
    return to_loads_direct(
        c=c, response_type=response_type, points=points, loads=loads,
    )


def to_pier_settlement(
    config: Config,
    points: List[Point],
    responses_array: List[List[float]],
    response_type: ResponseType,
    pier_settlement: List[Tuple[PierSettlement, PierSettlement]],
) -> List[List[float]]:
    """Time series of responses to pier settlement.

    Args:
        config: simulation configuration object.
        points: points in the TrafficArray.
        responses_array: NumPY array indexed first by point then time.
        response_type: the sensor response type to add.
        pier_settlement: start and end settlements of piers.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing the responses from pier settlement.

    """
    if len(pier_settlement) == 0:
        return np.zeros(responses_array.shape)
    assert len(responses_array) == len(points)
    for ps in pier_settlement:
        assert ps[0].pier == ps[1].pier
    # Sorted by pier settlement index then by point index.
    unit_responses = [
        load(
            config=config,
            response_type=response_type,
            pier_settlement=[
                PierSettlement(pier=ps[0].pier, settlement=config.unit_pier_settlement)
            ],
        ).at_decks(points)
        for ps in pier_settlement
    ]
    assert len(unit_responses) == len(pier_settlement)
    assert len(unit_responses[0]) == len(points)
    start_responses, end_responses = [0 for _ in points], [0 for _ in points]
    for p_i, _ in enumerate(points):
        for ps_i, ps in enumerate(pier_settlement):
            start_responses[p_i] += unit_responses[ps_i][p_i] * (
                ps[0].settlement / config.unit_pier_settlement
            )
            end_responses[p_i] += unit_responses[ps_i][p_i] * (
                ps[1].settlement / config.unit_pier_settlement
            )
    ps_responses = np.zeros(responses_array.shape)
    for p, _ in enumerate(points):
        ps_responses[p] = np.interp(
            np.arange(ps_responses.shape[1]),
            [0, ps_responses.shape[1] - 1],
            [start_responses[p], end_responses[p]],
        )
    return ps_responses


def to_temperature(
    config: Config,
    points: List[Point],
    responses_array: List[List[float]],
    response_type: ResponseType,
    weather: Optional[pd.DataFrame] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    skip_weather_interp: bool = False,
) -> List[List[float]]:
    """Time series of responses to temperature.

    Date formats must be given as "%d/%m/%y %H:%M" e.g. "01/05/19 00:00".

    Args:
        config: simulation configuration object.
        points: points in the TrafficArray.
        responses_array: NumPY array indexed first by point then time.
        response_type: the sensor response type to add.
        weather: the FULL weather data to calculate responses.
        start_date: start-date of weather data.
        end_date: end-date of weather data.
        skip_weather_interp: if True then use the given weather data directly
            instead of interpolating to minutely data. The consequence of
            setting this to True is the data might be a bit more jagged, due
            to data e.g. only every 5 minutes.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing the responses from temperature.

    """
    temp_responses = np.zeros(responses_array.shape)
    if weather is None:
        return temp_responses
    print_i("Calculating weather...")
    if not skip_weather_interp:
        weather = temperature.from_to_mins(
            weather,
            from_=datetime.strptime(start_date, temperature.f_string),
            to=datetime.strptime(end_date, temperature.f_string),
        )
    print_i("Calculated weather")
    effect = temperature.effect(
        config=config, response_type=response_type, points=points, weather=weather,
    )
    assert len(responses_array) == len(points)
    assert len(effect) == len(points)
    total_points = len(points)
    for p, _ in enumerate(points):
        print_i(f"Calculating temperature for point {p} / {total_points}", end="\r")
        temp_responses[p] = util.apply(effect[p], temp_responses[p])
    print_i(f"Calculated temperature for {total_points} points")
    return temp_responses


def to_shrinkage(
    config: Config,
    points: List[Point],
    responses_array: List[List[float]],
    response_type: ResponseType,
    start_day: Optional[int] = None,
    end_day: Optional[int] = None,
    cement_class: CementClass = CementClass.Normal,
    x: Optional[float] = None,
) -> List[List[float]]:
    """Time series of responses to concrete shrinkage.

    Args:
        config: simulation configuration object.
        points: points in the TrafficArray.
        responses_array: NumPY array indexed first by point then time.
        response_type: the sensor response type to add.
        start_day: start day of responses e.g. 365 is 1 year.
        end_day: end day of responses.
        cement_class: cement class used in construction.
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing the responses from shrinkage.

    """
    shrinkage_responses = np.zeros(responses_array.shape)
    if start_day is None:
        return shrinkage_responses
    days = np.arange(start_day, end_day + 1)
    seconds = convert_times(f="day", t="second", times=days)
    effect = bridge_sim.shrinkage.total_responses(
        config=config,
        response_type=response_type,
        times=seconds,
        points=points,
        cement_class=cement_class,
        x=x,
    )
    assert len(responses_array) == len(points)
    assert len(effect) == len(points)
    for p, _ in enumerate(points):
        shrinkage_responses[p] = util.apply(effect[p], shrinkage_responses[p])
    return shrinkage_responses


def to_creep(
    config: Config,
    points: List[Point],
    responses_array: List[List[float]],
    response_type: ResponseType,
    install_day: int,
    start_day: int,
    end_day: int,
    cement_class: CementClass = CementClass.Normal,
    self_weight: bool = False,
    pier_settlement: List[Tuple[PierSettlement, PierSettlement]] = [],
    shrinkage: bool = False,
    psi: Tuple[float, float, float] = [1, 1, 1],
    x: Optional[float] = None,
) -> List[List[float]]:
    """Time series of responses to concrete creep.

    Three different types of creep can be calculated, due to self-weight, due
    to pier settlement and due to shrinkage. Use "self_weight=True" to include
    the creep due to self-weight, pass both pier settlement arguments to include
    the creep due to pier settlement and use "shrinkage=True" to include the
    creep due to shrinkage.

    Args:
        config: simulation configuration object.
        points: points in 'responses_array'.
        responses_array: NumPY array indexed first by point then time.
        response_type: the sensor response type to compute.
        install_day: day the sensors were installed.
        start_day: start day of responses e.g. 365 is 1 year.
        end_day: end day of responses.
        cement_class: cement class used in construction.
        self_weight: return creep due to self weight?
        pier_settlement: return creep due to linear pier settlement?
        shrinkage: return creep due to shrinkage?
        psi: psi values for self-weight, pier settlement and shrinkage. If not
            given defaults are 1.0 for each component.
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing the responses from creep.

    """
    sw_psi, ps_psi, sh_psi = psi
    assert start_day >= install_day
    if sum(map(int, [self_weight, len(pier_settlement) > 0, shrinkage])) == 0:
        return np.zeros(responses_array.shape)
    # Calculate creep coefficient. We want to calculate the creep coefficient
    # from start_day to end_day, the period of sensor responses which are
    # requested. However we also need to calculate the value at install day,
    # since this is the value being subtracted from the time series.
    days = np.arange(start_day, end_day + 1)
    seconds = convert_times(f="day", t="second", times=days)
    coeff = util.apply(
        creep.creep_coeff(config=config, cement_class=cement_class, times=seconds, x=x),
        np.arange(responses_array.shape[1]),
    )
    install_times = convert_times(
        f="day", t="second", times=np.arange(install_day, install_day + 1)
    )
    coeff_install = creep.creep_coeff(config, cement_class, times=install_times, x=x)[0]
    # In-case creep due to some effect is not requested then we just consider an
    # array of zeros for that effect.
    sw_result, ps_result, sh_result = [
        np.zeros(responses_array.shape) for _ in range(3)
    ]
    # Convert responses from self-weight, pier settlement or shrinkage to
    # responses_array. First the most calculated case: self-weight.
    if self_weight:
        # For each point, a time series of the same repeating response.
        sw_responses = np.array(
            [
                np.repeat(r, responses_array.shape[1])
                for r in load(
                    config=config, response_type=response_type, self_weight=True
                ).at_decks(points)
            ]
        )
        assert sw_responses.shape == responses_array.shape
        sw_result = np.empty(responses_array.shape)
        for p in range(len(points)):
            assert len(sw_responses[p]) == len(coeff)
            install_val = sw_responses[p][0] * (1 + (coeff_install * sw_psi))
            sw_result[p] = (
                np.multiply(sw_responses[p], (1 + (coeff * sw_psi))) - install_val
            )
            assert (
                sw_result[p][-1]
                == sw_responses[p][-1] * (1 + coeff[-1] * sw_psi) - install_val
            )
    if len(pier_settlement) > 0:
        # We need the value of pier settlement at install day, and then also for
        # the range of the time series being considered.
        # install_ps_responses = load(
        #     config=config,
        #     response_type=response_type,
        #     pier_settlement=install_pier_settlement,
        # ).at_decks(points)
        ps_responses = to_pier_settlement(
            config=config,
            points=points,
            responses_array=responses_array,
            response_type=response_type,
            pier_settlement=pier_settlement,
        )
        assert ps_responses.shape == responses_array.shape
        ps_result = np.empty(responses_array.shape)
        for p in range(len(points)):
            assert len(ps_responses[p]) == len(coeff)
            install_val = ps_responses[p] * (1 + (coeff_install * ps_psi))
            ps_result[p] = (
                np.multiply(ps_responses[p], (1 + (coeff * ps_psi))) - install_val
            )
            assert ps_result[p][-1] == (
                ps_responses[p][-1] * (1 + coeff[-1] * ps_psi)
            ) - (ps_responses[p][-1] * (1 + (coeff_install * ps_psi)))
    if shrinkage:
        # We need the value of shrinkage at install day, and then also for
        # the range of the time series being considered.
        # install_sh_responses = (
        #     to_shrinkage(
        #         config=config,
        #         points=points,
        #         responses_array=responses_array,
        #         response_type=response_type,
        #         start_day=install_day,
        #         end_day=install_day + 1,
        #         cement_class=cement_class,
        #     )
        #     .T[0]
        #     .T
        # )  # Consider only first value for each point.
        sh_responses = to_shrinkage(
            config=config,
            points=points,
            responses_array=responses_array,
            response_type=response_type,
            start_day=start_day,
            end_day=end_day,
            cement_class=cement_class,
            x=x,
        )
        assert sh_responses.shape == responses_array.shape
        sh_result = np.empty(responses_array.shape)
        for p in range(len(points)):
            assert len(sh_responses[p]) == len(coeff)
            install_val = sh_responses[p] * (1 + (coeff_install * sh_psi))
            sh_result[p] = (
                np.multiply(sh_responses[p], (1 + (coeff * sh_psi))) - install_val
            )
            assert sh_result[p][-1] == sh_responses[p][-1] * (
                1 + coeff[-1] * sh_psi
            ) - (sh_responses[p][-1] * (1 + (coeff_install * sh_psi)))
    return sw_result + ps_result + sh_result


def to(
    config: Config,
    points: List[Point],
    traffic_array: List[List[float]],
    response_type: ResponseType,
    with_creep: bool,
    pier_settlement: List[Tuple[PierSettlement, PierSettlement]] = [],
    weather: Optional[pd.DataFrame] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    install_day: Optional[int] = None,
    start_day: Optional[int] = None,
    end_day: Optional[int] = None,
    cement_class: CementClass = CementClass.Normal,
    crack: Optional[Tuple[CrackDeck, int]] = None,
    ret_all: bool = False,
    psi: Tuple[float, float, float] = [1, 1, 1],
    x: Optional[float] = None,
    skip_weather_interp: bool = False,
) -> List[List[float]]:
    """Time series of responses to multiple effects.

    Args:
        config: simulation configuration object.
        points: points in the TrafficArray.
        traffic_array: NumPY array indexed first by point then time.
        response_type: the sensor response type to add.
        pier_settlement: a pier settlement to apply.
        with_creep: include the effects of creep?
        weather: the FULL weather data to calculate responses.
        start_date: start-date of weather data.
        end_date: end-date of weather data.
        install_day: required if calculating effect due to creep.
        start_day: start day of responses e.g. 365 is 1 year.
        end_day: end day of responses.
        cement_class: cement class used in construction.
        crack: a crack to apply at some time index.
        ret_all: return individual components.
        psi: psi values for self-weight, pier settlement and shrinkage. If not
            given defaults are 1, 1.5 and 0.55 respectively.
        x: X position used to calculate cross-sectional area and perimeter, if
            not given use the center of the bridge.
        skip_weather_interp: see 'to_temperature'.

    Returns: NumPY array of same shape as "responses_array" and considering the
        same points, but only containing any of the given response sources.

    """

    def _get(_config: Config):
        _tr_responses = to_traffic_array(
            config=_config,
            traffic_array=traffic_array,
            response_type=ResponseType.YTrans,
            points=points,
        )
        print_i(f"Calculated responses to traffic")
        _ps_responses = to_pier_settlement(
            config=_config,
            points=points,
            responses_array=_tr_responses,
            response_type=response_type,
            pier_settlement=pier_settlement,
        )
        print_i(f"Calculated responses to pier settlement")
        _temp_responses = to_temperature(
            config=_config,
            points=points,
            responses_array=_tr_responses,
            response_type=response_type,
            weather=weather,
            start_date=start_date,
            end_date=end_date,
            skip_weather_interp=skip_weather_interp,
        )
        print_i(f"Calculated responses to temperature")
        _shrinkage_responses = to_shrinkage(
            config=_config,
            points=points,
            responses_array=_tr_responses,
            response_type=response_type,
            start_day=start_day,
            end_day=end_day,
            cement_class=cement_class,
            x=x,
        )
        print_i(f"Calculated responses to shrinkage")
        _creep_responses = np.zeros(_shrinkage_responses.shape)
        if with_creep:
            _creep_responses = to_creep(
                config=_config,
                points=points,
                responses_array=_tr_responses,
                response_type=response_type,
                install_day=install_day,
                start_day=start_day,
                end_day=end_day,
                cement_class=cement_class,
                self_weight=True,
                pier_settlement=pier_settlement,
                shrinkage=True,
                psi=psi,
                x=x,
            )
        print_i(f"Calculated responses to creep")
        return (
            _tr_responses,
            _ps_responses,
            _temp_responses,
            _shrinkage_responses,
            _creep_responses,
        )

    # Healthy.
    (
        tr_responses,
        ps_responses,
        temp_responses,
        shrinkage_responses,
        creep_responses,
    ) = _get(config)
    responses = (
        tr_responses
        + ps_responses
        + temp_responses
        + shrinkage_responses
        + creep_responses
    )
    if crack is None:
        if ret_all:
            return (
                tr_responses,
                ps_responses,
                temp_responses,
                shrinkage_responses,
                creep_responses,
            )
        return responses
    if ret_all:
        raise NotImplementedError("ret_all and cracking not supported")
    # Cracked.
    (
        ctr_responses,
        cps_responses,
        ctemp_responses,
        cshrinkage_responses,
        ccreep_responses,
    ) = _get(crack[0].crack(config))
    crack_responses = (
        ctr_responses
        + cps_responses
        + ctemp_responses
        + cshrinkage_responses
        + ccreep_responses
    )
    # Split responses and cracked responses at given time, and concat result.
    time = crack[1]
    return np.concatenate([responses.T[:time], crack_responses.T[time:]]).T
