"""High-level API for saving/loading responses from FE simulation."""

from __future__ import annotations

# Print debug information for this file.
import os
from collections import deque
from copy import deepcopy
from typing import Callable, List, Optional, Tuple

import numpy as np
from bridge_sim.model import (
    Config,
    ResponseType,
    Point,
    PointLoad,
    Vehicle,
    Config as LibConfig,
    PierSettlement,
)
from bridge_sim.scenarios import (
    PierSettlementScenario,
    Scenario,
    HealthyScenario,
    transverse_crack,
    healthy_damage_w_crack_nodes,
)
from bridge_sim.sim.model import SimParams, ManyResponses, Responses
from bridge_sim.sim.run import FEMRunner, load_expt_responses, load_fem_responses
from bridge_sim.sim.run.opensees import OSRunner
from bridge_sim.util import (
    print_i,
    print_w,
    flatten,
    print_d,
    round_m,
    shorten_path,
    log,
)
from pathos import multiprocessing as multiprocessing

D: str = "fem.fem"
# D: bool = False


def responses_to_traffic_array(
    c: Config,
    traffic_array: "TrafficArray",
    response_type: ResponseType,
    damage_scenario: "Scenario",
    points: List[Point],
    sim_runner: Callable[[Config], FEMRunner] = OSRunner,
):
    """The magic function.

    Args:
        c: Config, global configuration object.
        traffic_array: TrafficArray, ....
        damage_scenario: DamageScenario, the scenarios scenario of the bridge.
        response_type: ResponseType, the type of sensor response to calculate.
        points: List[Point], points on the bridge to calculate fem at.
        sim_runner: Callable[[Config], FEMRunner], the FEM program to run
            simulations with.

    """
    use_c = damage_scenario.use(c)[0]
    unit_load_matrix = ULResponses.load_ulm(
        c=use_c,
        response_type=response_type,
        points=points,
        sim_runner=sim_runner(use_c),
    )
    print(traffic_array.shape)
    print(unit_load_matrix.shape)
    responses = np.matmul(traffic_array, unit_load_matrix)

    # Calculate the response at each point due to pier settlement.
    pd_responses = np.zeros(responses.shape).T
    assert len(pd_responses) == len(points)
    if isinstance(damage_scenario, PierSettlementScenario):
        pd_expt = list(
            PSResponses.load(c=c, response_type=response_type, fem_runner=sim_runner(c))
        )
        for point_i, point in enumerate(points):
            for pier_displacement in damage_scenario.pier_disps:
                pd_sim_responses = pd_expt[pier_displacement.pier]
                pd_responses[point_i] += pd_sim_responses.at_deck(
                    point, interp=False
                ) * (pier_displacement.displacement / c.pd_unit_disp)

    return responses + pd_responses.T


def responses_to_loads_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    loads: List[List[PointLoad]],
    damage_scenario: Scenario = HealthyScenario(),
):
    """Responses to point-loads via direct simulation (not using superposition).
    """
    if not isinstance(damage_scenario, HealthyScenario):
        raise ValueError("Only HealthyDamage supported in direct simulation")
    expt_responses = load_expt_responses(
        c=c,
        expt_params=[SimParams(ploads=loads_) for loads_ in loads],
        response_type=response_type,
    )
    result = []
    for sim_responses in expt_responses:
        result.append([sim_responses.at_deck(point, interp=True) for point in points])
        print_i("Interpolating fem in responses_from_load_d")
    return np.array(result)


def responses_to_vehicles_d(
    c: Config,
    response_type: ResponseType,
    points: List[Point],
    mv_vehicles: List[Vehicle],
    times: List[float],
    binned: bool = True,
    damage_scenario: Scenario = HealthyScenario(),
):
    """Response vehicles via direct simulation (not using superposition).

    """
    if not isinstance(damage_scenario, HealthyScenario):
        raise ValueError("Only HealthyDamage supported in direct simulation")
    if binned:
        loads = [
            [v.to_wheel_track_loads(c=c, time=time) for v in mv_vehicles]
            for time in times
        ]
    else:
        print_w(f"Not using fractions of wheel track bins in simulation")
        loads = [
            [v.to_point_load_pw(time=time, bridge=c.bridge) for v in mv_vehicles]
            for time in times
        ]
    loads = [flatten(vehicle_loads, PointLoad) for vehicle_loads in loads]
    print([len(load_) for load_ in loads])
    print(loads[0])
    print(loads[-1])
    assert isinstance(loads, list)
    assert isinstance(loads[0], list)
    assert isinstance(loads[0][0], PointLoad)
    return responses_to_loads_d(
        c=c,
        response_type=response_type,
        points=points,
        loads=loads,
        damage_scenario=damage_scenario,
    )


def load(
    config: LibConfig,
    response_type: ResponseType,
    point_loads: List[PointLoad] = [],
    pier_settlement: List[PierSettlement] = [],
    temp_deltas: Tuple[Optional[float], Optional[float]] = (None, None),
):
    """Responses from a single linear simulation.

    The simulation is only run if results are not found on disk.

    Args:
        config: simulation configuration object.
        response_type: sensor response type to return.
        point_loads: a list of point-loads to apply.
        pier_settlement: a pier settlement to apply.
        temp_deltas: uniform and linear temperature components.

    """
    return load_fem_responses(
        c=config,
        sim_params=SimParams(
            ploads=point_loads,
            pier_settlement=pier_settlement,
            axial_delta_temp=temp_deltas[0],
            moment_delta_temp=temp_deltas[1],
        ),
        response_type=response_type,
    )


class PSResponses(ManyResponses):
    """Responses of one sensor type for pier settlement simulations."""

    @staticmethod
    def load(
        c: Config,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        save_all: bool = True,
    ):
        """Load a DCExpt from disk, running simulations first if necessary.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, the type of sensor response to load.
            fem_runner: FEMRunner, the FE program to run simulations with.
            save_all: bool, save all response types when running a simulation.

        """
        # id_str = f"dc-{response_type.name()}-{fem_runner.name}"

        # Determine experiment simulation parameters.
        expt_params = [
            SimParams(displacement_ctrl=PierSettlement(c.pd_unit_disp, i))
            for i in range(len(c.bridge.supports))
        ]

        return load_expt_responses(
            c=c, expt_params=expt_params, response_type=response_type,
        )


class ULResponses(ManyResponses):
    """Responses of one sensor type for influence line calculations.

    Each simulation is for a different loading position in the longitudinal
    direction of the bridge. The z position is fixed for one ILExpt, thus a
    different ILExpt should be used for each tire wheel on a bridge.

    """

    def response_to(
        self,
        x_frac: float,
        z_frac: float,
        load_x_frac: float,
        load: float,
        y_frac: float = 1,
        time_index: int = 0,
    ):
        """The response value in kN at a position to a load at a position.

        NOTE: only the loading position in longitudinal direction can be chosen,
        with 'load_x_frac', the position in transverse direction is fixed for a
        single ILExpt.

        Args:
            x_frac: float, response position on x-axis in [0 1].
            y_frac: float, response position on y-axis in [0 1].
            z_frac: float, response position on x-axis in [0 1].
            load_x_frac: float, load position on x-axis in [0 1].
            load: float, value of the load in kN.
            time_index: int, time index of the simulation.

        """
        assert 0 <= x_frac <= 1
        assert 0 <= load_x_frac <= 1
        print_d(D, f"x_frac = {x_frac} = load_x_frac = {load_x_frac}")
        response = super().sim_response(
            expt_frac=load_x_frac,
            x_frac=x_frac,
            y_frac=y_frac,
            z_frac=z_frac,
            time_index=time_index,
        )
        return response * (load / self.c.il_unit_load_kn)

    def id_str(
        c: Config,
        response_type: ResponseType,
        sim_runner: FEMRunner,
        wheel_zs: List[float],
    ):
        wheel_zs_str = [round_m(wheel_z) for wheel_z in wheel_zs]
        return (
            f"il-{response_type.name()}-{sim_runner.name}-{c.il_unit_load_kn}"
            + f"-{c.il_num_loads}-z={wheel_zs_str}"
        )

    @staticmethod
    def load_ulm(
        c: Config,
        response_type: ResponseType,
        points: List[Point],
        sim_runner: FEMRunner,
    ):
        wheel_zs = c.bridge.wheel_track_zs(c)
        filepath = c.get_data_path(
            "ulms",
            (
                ULResponses.id_str(
                    c=c,
                    response_type=response_type,
                    sim_runner=sim_runner,
                    wheel_zs=wheel_zs,
                )
                + str([str(point) for point in points])
            )
            + ".ulm",
        )
        filepath = shorten_path(c=c, bypass_config=True, filepath=filepath)

        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                return np.load(f)

        def ulm_partial(wheel_z):
            """Slice of unit load matrix for one wheel track."""
            wheel_track = ULResponses.load_wheel_track(
                c=c,
                response_type=response_type,
                fem_runner=sim_runner,
                load_z_frac=c.bridge.z_frac(wheel_z),
                run_only=False,
            )
            partial = np.empty((c.il_num_loads, len(points)))
            i = 0
            for sim_responses in wheel_track:
                for j, point in enumerate(points):
                    partial[i][j] = sim_responses.at_deck(point, interp=False)
                    if wheel_z < 0 and i == 302:
                        log(
                            c,
                            f"z = {wheel_z}, i = 302, partial[i][j] = {partial[i][j]}",
                        )
                i += 1
            assert i == c.il_num_loads
            print_i(f"Calculated unit load matrix for wheel track {wheel_z}")
            return partial

        # Calculate results in parallel.
        print_i(f"Calculating unit load matrix...")
        with multiprocessing.Pool(processes=len(wheel_zs)) as pool:
            partial_results = pool.map(ulm_partial, wheel_zs)
        # And insert into the unit load matrix.
        unit_load_matrix = np.empty((len(wheel_zs) * c.il_num_loads, len(points)))
        for w_ind in range(len(wheel_zs)):
            row_ind = w_ind * c.il_num_loads
            unit_load_matrix[row_ind : row_ind + c.il_num_loads] = partial_results[
                w_ind
            ]
        # Divide by unit load, so the value at a cell is the response to 1 kN.
        unit_load_matrix /= c.il_unit_load_kn
        with open(filepath, "wb") as f:
            np.save(f, unit_load_matrix)
        return unit_load_matrix

    @staticmethod
    def load_wheel_tracks(
        c: Config,
        response_type: ResponseType,
        sim_runner: FEMRunner,
        wheel_zs: List[float],
        run_only: bool = False,
    ):
        """Return a dictionary of wheel tracks indexed by z position.

        Each wheel track will be calculated in parallel if the
        'Config.parallel_ulm' is set. If the 'run_only' option is given, then
        the simulations will run but the results will not be loaded into memory.

        """

        def create_or_load_wheel_track(
            wheel_z,
            _run_only: bool = True,
            left_only: bool = False,
            right_only: bool = False,
        ):
            results = ULResponses.load_wheel_track(
                c=deepcopy(c),
                response_type=response_type,
                fem_runner=deepcopy(sim_runner),
                load_z_frac=c.bridge.z_frac(wheel_z),
                run_only=_run_only,
                left_only=left_only,
                right_only=right_only,
            )
            # If results are only being generated, then evaluate the generator,
            # such that the results are generated. Otherwise leave the generator
            # to be used by the caller.
            if _run_only:
                # This forces the generator to be consumed without keeping the
                # contents in memory. https://stackoverflow.com/a/47456679
                deque(results, maxlen=0)
                return
            # Otherwise return the generator, to be evaluated.
            else:
                return results

        # For each wheel track, generate it if doesn't exists.
        # Use upto (2 x wheel_track) parallelism.
        if c.parallel_ulm:
            processes = min(multiprocessing.cpu_count(), len(wheel_zs * 2))
            print_i(f"Running with {processes} processes")
            with multiprocessing.Pool(processes=processes) as pool:

                def _run(params):
                    """Tuple of wheel z & left/right and runs wheel track."""
                    z, l, r = params
                    create_or_load_wheel_track(wheel_z=z, left_only=l, right_only=r)

                # Construct two variants of parameters for each wheel track.
                all_params = []
                for wheel_z in wheel_zs:
                    all_params.append((wheel_z, True, False))
                    all_params.append((wheel_z, False, True))
                assert len(all_params) == 2 * len(wheel_zs)
                pool.map(_run, all_params)
        else:
            list(map(create_or_load_wheel_track, wheel_zs))
        if run_only:
            return
        # Load all wheel tracks from disk into the resulting dictionary.
        result = dict()
        for wheel_z in wheel_zs:
            result[wheel_z] = create_or_load_wheel_track(
                wheel_z=wheel_z, _run_only=False
            )
        return result

    @staticmethod
    def load_wheel_track(
        c: Config,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        load_z_frac: float,
        run_only: bool,
        indices: Optional[List[int]] = None,
        left_only: bool = False,
        right_only: bool = False,
    ) -> List[Responses]:
        """Load a wheel track from disk, running simulations if necessary.

        NOTE: The result is a generator, not a list.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, type of sensor response to return.
            fem_runner: FEMRunner, program to run finite element simulations.
            load_z_frac: float, load position as a fraction of the transverse
                direction in [0 1].
            run_only: bool, only run the simulation, do not load results.
            left_only: bool, if true only run the left-hand-side of the wheel
                track. If true, right_only must be false and indices None.
            right_only: bool, if True only run the right-hand-side of the wheel
                track. If true, left_only must be false and indices None.

        """
        wheel_xs = c.bridge.wheel_track_xs(c)
        first_right_index = len(wheel_xs) // 2
        print(f"First right index = {first_right_index}")

        if left_only:
            assert not right_only
            assert indices is None
            wheel_xs = wheel_xs[:first_right_index]
        if right_only:
            assert not left_only
            assert indices is None
            wheel_xs = wheel_xs[first_right_index:]

        assert 0 <= load_z_frac <= 1
        # Determine experiment simulation parameters.
        expt_params = [
            SimParams(
                ploads=[
                    PointLoad(
                        x_frac=c.bridge.x_frac(x),
                        z_frac=load_z_frac,
                        kn=c.il_unit_load_kn,
                    )
                ],
                clean_build=True,
            )
            for x in wheel_xs
        ]
        # Filter simulations, only running those in 'indices'.
        if indices is not None:
            expt_params.sim_params = [
                sp for i, sp in enumerate(expt_params.sim_params) if i in indices
            ]
        return load_expt_responses(
            c=c,
            expt_params=expt_params,
            response_type=response_type,
            sim_runner=fem_runner,
            run_only=run_only,
        )


def run_uls(
    c: Config,
    piers: bool,
    healthy: bool,
    cracked: bool,
    crack_x: Optional[int] = None,
    crack_length: Optional[int] = None,
):
    """Run all unit load simulations."""

    def crack_f():
        return transverse_crack(at_x=crack_x, length=crack_length)

    print_i(
        f"Running simulations with crack zone at x = {crack_x}, length = {crack_length}"
    )

    response_type = ResponseType.YTranslation
    if piers:
        # Pier settlement.
        list(PSResponses.load(c=c, response_type=response_type, fem_runner=OSRunner(c)))
    if healthy:
        c = healthy_damage_w_crack_nodes(crack_f=crack_f).use(c)[0]
        # Unit load simulations (healthy bridge).
        ULResponses.load_wheel_tracks(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            wheel_zs=c.bridge.wheel_track_zs(c),
            run_only=True,
        )
    elif cracked:
        # Unit load simulations (cracked bridge).
        c = crack_f().use(c)[0]
        ULResponses.load_wheel_tracks(
            c=c,
            response_type=response_type,
            sim_runner=OSRunner(c),
            wheel_zs=c.bridge.wheel_track_zs(c),
            run_only=True,
        )


def run_ulm(c: Config, healthy: bool, cracked: bool, x_i: float, z_i: float):
    """Run all unit load simulations."""
    response_type = ResponseType.YTranslation
    wheel_xs = c.bridge.wheel_track_xs(c)
    wheel_x = wheel_xs[x_i]
    wheel_zs = c.bridge.wheel_track_zs(c)
    wheel_z = wheel_zs[z_i]
    print_i(f"Wheel (x, z) = ({wheel_x}, {wheel_z})")
    point = Point(x=wheel_x, y=0, z=wheel_z)
    if healthy:
        ULResponses.load_ulm(
            c=c, response_type=response_type, points=[point], sim_runner=OSRunner(c),
        )
    if cracked:
        c = transverse_crack().use(c)[0]
        ULResponses.load_ulm(
            c=c, response_type=response_type, points=[point], sim_runner=OSRunner(c),
        )
