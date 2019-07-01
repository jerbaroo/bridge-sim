import numpy as np

from opensees.build import build_model
from opensees.run import run_model


def _os_runner(c: Config, f: FEMParams):
    """Generate a FEMResponses for each FEMParams for each ResponseType."""
    responses = [0 for _ in range(len(f.simulations))]
    for i, loads in enumerate(f.simulations):
        build_opensees_model(c, loads=loads)
        responses[i] = run_opensees_model(c)
    for response_type in Response:
        FEMResponses(
            response_type,
            list(map(lambda r: np.array(r[response_type]), responses))
        ).save(c)


os_runner = FEMRunner(_os_runner, "OpenSees")
