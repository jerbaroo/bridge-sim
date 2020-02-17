import os
import pathos.multiprocessing as multiprocessing
from collections import deque
from copy import deepcopy
from typing import List, Optional

import dill
import numpy as np

from config import Config
from fem.params import ExptParams, SimParams
from fem.responses.matrix import ResponsesMatrix, load_expt_responses
from fem.run import FEMRunner
from model.bridge import Point
from model.load import PointLoad
from model.response import ResponseType
from util import print_d, print_i, print_w, round_m, safe_str

# Print debug information for this file.
D: bool = False


class ILMatrix(ResponsesMatrix):
    """Responses of one sensor type for influence line calculations.

    Each simulation is for a different loading position in the longitudinal
    direction of the bridge. The z position is fixed for one ILMatrix, thus a
    different ILMatrix should be used for each tire wheel on a bridge.

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
        single ILMatrix.

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
        def ulm_partial(wheel_z):
            """Slice of unit load matrix for one wheel track."""
            wheel_track = ILMatrix.load_wheel_track(
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
                i += 1
            assert i == c.il_num_loads
            print_i(f"Calculated unit load matrix for wheel track {wheel_z}")
            return partial
        # Calculate results in parallel.
        print_i(f"Calculating unit load matrix...")
        wheel_zs = c.bridge.wheel_track_zs(c)
        with multiprocessing.Pool(processes=len(wheel_zs)) as pool:
            partial_results = pool.map(ulm_partial, wheel_zs)
        # And insert into the unit load matrix.
        unit_load_matrix = np.empty((len(wheel_zs) * c.il_num_loads, len(points)))
        for w_ind in range(len(wheel_zs)):
            row_ind = w_ind * c.il_num_loads
            unit_load_matrix[row_ind:row_ind + c.il_num_loads] = partial_results[w_ind]
        # Divide by unit load, so the value at a cell is the response to 1 kN.
        unit_load_matrix /= c.il_unit_load_kn
        return unit_load_matrix

    @staticmethod
    def load_wheel_tracks(
        c: Config,
        response_type: ResponseType.YTranslation,
        sim_runner: FEMRunner,
        wheel_zs: List[float],
        run_only: bool = False,
    ):
        """Return a dictionary of wheel tracks indexed by z position.

        Each wheel track will be calculated in parallel if the
        'Config.parallel_ulm' is set. If the 'run_only' option is given, then
        the simulations will run but the results will not be loaded into memory.

        """

        def create_or_load_wheel_track(wheel_z, _run_only: bool = True):
            results = ILMatrix.load_wheel_track(
                c=deepcopy(c),
                response_type=response_type,
                fem_runner=deepcopy(sim_runner),
                load_z_frac=c.bridge.z_frac(wheel_z),
                run_only=_run_only,
            )
            # If results are only being generated, then evaluate the generator,
            # such that the results are generated. Otherwise leave the generator
            # to be used by the caller.
            if _run_only:
                # This forces the generator to be consumed without keeping the
                # contents in memory. https://stackoverflow.com/a/47456679
                deque(results, maxlen=0)
            # Otherwise return the generator, to be evaluated.
            else:
                return results

        # For each wheel track, generate it if doesn't exists.
        if c.parallel_ulm:
            processes = min(multiprocessing.cpu_count(), len(wheel_zs))
            print_i(f"Running with {processes} processes")
            with multiprocessing.Pool(processes=processes) as pool:
                pool.map(create_or_load_wheel_track, wheel_zs)
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
    ) -> "ILMatrix":
        """Load a wheel track from disk, running simulations if necessary.

        NOTE: The result is a generator, not a list.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, type of sensor response to return.
            fem_runner: FEMRunner, program to run finite element simulations.
            load_z_frac: float, load position as a fraction of the transverse
                direction in [0 1].
            run_only: bool, only run the simulation, do not load results.

        """
        assert 0 <= load_z_frac <= 1
        # Determine experiment simulation parameters.
        expt_params = ExptParams(
            [
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
                for x in c.bridge.wheel_track_xs(c)
            ]
        )
        return load_expt_responses(
            c=c,
            expt_params=expt_params,
            response_type=response_type,
            sim_runner=fem_runner,
            run_only=run_only,
        )
