from lib.config import Config
from lib.fem.params import ExptParams, SimParams
from lib.fem.responses.matrix import ResponsesMatrix, load_expt_responses
from lib.fem.responses.matrix.il import ILMatrix
from lib.fem.run import FEMRunner
from lib.model.load import PierSettlement
from lib.model.response import ResponseType
from util import print_w


class DCMatrix(ResponsesMatrix):
    """Responses of one sensor type for displacement control simulations."""

    @staticmethod
    def load(
        c: Config,
        response_type: ResponseType,
        fem_runner: FEMRunner,
        save_all: bool = True,
    ):
        """Load a DCMatrix from disk, running simulations first if necessary.

        Args:
            c: Config, global configuration object.
            response_type: ResponseType, the type of sensor response to load.
            fem_runner: FEMRunner, the FE program to run simulations with.
            save_all: bool, save all response types when running a simulation.

        """
        # id_str = f"dc-{response_type.name()}-{fem_runner.name}"

        # Determine experiment simulation parameters.
        expt_params = ExptParams(
            [
                SimParams(displacement_ctrl=PierSettlement(c.pd_unit_disp, i))
                for i in range(len(c.bridge.supports))
            ]
        )

        return load_expt_responses(
            c=c,
            expt_params=expt_params,
            response_type=response_type,
            sim_runner=fem_runner,
        )

        # def load_func(expt_params):
        #     return DCMatrix(
        #         c=c,
        #         response_type=response_type,
        #         expt_params=expt_params,
        #         fem_runner=fem_runner,
        #         save_all=save_all,
        #     )
        # return ResponsesMatrix.load(
        #     c=c,
        #     id_str=id_str,
        #     expt_params=_expt_params,
        #     load_func=load_func,
        #     fem_runner=fem_runner,
        #     save_all=save_all,
        # )
