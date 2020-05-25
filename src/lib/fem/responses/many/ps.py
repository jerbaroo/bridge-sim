from bridge_sim.model import Config, PierSettlement, ResponseType
from lib.fem.params import SimParams
from lib.fem.responses.many import ManyResponses, load_expt_responses
from lib.fem.run import FEMRunner


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
