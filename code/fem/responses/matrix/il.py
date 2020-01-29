import os
import pathos.multiprocessing as multiprocessing
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
        wheel_zs = c.bridge.wheel_track_zs(c)
        # A unique path for this unit load matrix.
        result_path = ILMatrix.id_str(
            c=c,
            response_type=response_type,
            sim_runner=sim_runner,
            wheel_zs=wheel_zs,
        ) + str([str(point) for point in points]) + "-ulm"
        # If the unit load matrix is available, return it.
        if result_path in c.resp_matrices:
            print_i(f"Unit load matrix {wheel_zs} already calculated!")
            return c.resp_matrices[result_path]
        # Otherwise load each wheel track..
        wheel_tracks = ILMatrix.load_wheel_tracks(
            c=c,
            response_type=response_type,
            sim_runner=sim_runner,
            wheel_zs=wheel_zs,
        )
        # ..and calculate the unit load matrix.
        # Dimensions: (lanes * 2 * ULS) (rows) * point (columns).
        print_i(f"Calculating unit load matrix...")
        unit_load_matrix = np.empty((len(wheel_zs) * c.il_num_loads, len(points)))
        for w, wheel_z in enumerate(wheel_tracks.keys()):
            i = w * c.il_num_loads  # Row index.
            wheel_track = wheel_tracks[wheel_z]
            # For each unit load simulation.
            for sim_responses in wheel_track.expt_responses:
                for j, point in enumerate(points):
                    unit_load_matrix[i][j] = sim_responses.at_deck(point, interp=True)
                i += 1
            print_i(f"Calculated unit load matrix for wheel track {w}")
        # Divide by the load of the unit load simulations, so the value at a
        # cell is the response to 1 kN. Then multiple the traffic and unit load
        # matrices to get the responses.
        unit_load_matrix /= c.il_unit_load_kn
        c.resp_matrices[result_path] = unit_load_matrix
        return unit_load_matrix

    @staticmethod
    def load_wheel_tracks(
        c: Config,
        response_type: ResponseType.YTranslation,
        sim_runner: FEMRunner,
        wheel_zs: List[float],
        save_all: bool = True,
    ):
        # A unique path these wheel tracks.
        result_path = ILMatrix.id_str(
            c=c,
            response_type=response_type,
            sim_runner=sim_runner,
            wheel_zs=wheel_zs,
        ) + "-uls"
        # Return if these wheel tracks are already in memory.
        if result_path in c.resp_matrices:
            print_i(f"Wheel tracks {wheel_zs} already calculated!")
            return c.resp_matrices[result_path]

        def wheel_track_path(wheel_z):
            id_str = ILMatrix.id_str(
                c=c,
                response_type=response_type,
                sim_runner=sim_runner,
                wheel_zs=[wheel_z],
            )
            return c.get_data_path("uls", safe_str(id_str) + ".uls")

        def create_wheel_track(wheel_z):
            if not os.path.exists(wheel_track_path(wheel_z)):
                wheel_track = ILMatrix.load(
                    c=c,
                    response_type=response_type,
                    fem_runner=sim_runner,
                    load_z_frac=c.bridge.z_frac(wheel_z),
                )
                with open(wheel_track_path(wheel_z), "wb") as f:
                    print_i(f"Saving wheel track {wheel_z} to disk!")
                    dill.dump(wheel_track, f)
                    print_i(f"Saved wheel track {wheel_z} to disk!")
            else:
                print_i(f"Wheel track {wheel_z} already calculated!")

        # For each wheel track, generate it if doesn't exists.
        processes = multiprocessing.cpu_count() if c.parallel_ulm else 1
        with multiprocessing.Pool(processes=processes) as pool:
            pool.map(create_wheel_track, wheel_zs)
        # Load all wheel tracks from disk into the resulting dictionary.
        result = dict()
        for wheel_z in wheel_zs:
            with open(wheel_track_path(wheel_z), "rb") as f:
                result[wheel_z] = dill.load(f)
        c.resp_matrices[result_path] = result
        return result

    @staticmethod
    def load(
        c: Config,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        load_z_frac: float,
        save_all: bool = True,
    ) -> "ILMatrix":
        """Load an ILMatrix from disk, running simulations first if necessary.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, type of sensor response to load.
            fem_runner: FEMRunner, program to run finite element simulations.
            load_z_frac: float, load position as a fraction of the transverse
                direction in [0 1].
            save_all: bool, whether to save responses from all sensor types when
                running simulations, this is useful if simulations take a long
                time to run and you anticipate needing other sensor types.

        """
        assert 0 <= load_z_frac <= 1
        id_str = (
            ILMatrix.id_str(
                c=c,
                response_type=response_type,
                sim_runner=fem_runner,
                wheel_zs=[c.bridge.z(load_z_frac)],
            )
            + "-matrix"
        )

        # Determine experiment simulation parameters.
        _expt_params = ExptParams(
            [
                SimParams(
                    ploads=[
                        PointLoad(
                            x_frac=x_frac, z_frac=load_z_frac, kn=c.il_unit_load_kn,
                        )
                    ],
                    response_types=[response_type],
                )
                for x_frac in np.linspace(0, 1, c.il_num_loads)
            ]
        )

        def load_func(expt_params):
            """Load a ResponsesMatrix from given simulation parameters."""
            il_matrix = ILMatrix(
                c=c,
                response_type=response_type,
                expt_params=expt_params,
                fem_runner=fem_runner,
                save_all=save_all,
                expt_responses=load_expt_responses(
                    c=c,
                    expt_params=expt_params,
                    response_type=response_type,
                    sim_runner=fem_runner,
                ),
            )
            il_matrix.load_z_frac = load_z_frac
            return il_matrix

        return ResponsesMatrix.load(
            c=c,
            id_str=id_str,
            expt_params=_expt_params,
            load_func=load_func,
            fem_runner=fem_runner,
            save_all=save_all,
        )
