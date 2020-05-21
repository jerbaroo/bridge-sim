import os
from typing import Callable, Optional

import findup

from bridge_sim.model import Config, Bridge
from lib.fem.run.opensees import os_runner

project_dir = os.path.dirname(findup.glob(".git"))


def opensees_default(bridge: Callable[[], Bridge], os_exe: Optional[str] = None, **kwargs) -> Config:
    """A config using OpenSees for the given Bridge.

    :param bridge: function to return a new bridge.
    :param os_exe: absolute path to OpenSees binary.
    :param kwargs: passed on to Config constructor.
    :return: a new Config.
    """
    return Config(
        bridge=bridge,
        fem_runner=os_runner(os_exe),
        vehicle_data_path=os.path.join(project_dir, "data/traffic/traffic.csv"),
        vehicle_pdf=[
            (2.4, 5),
            (5.6, 45),
            (7.5, 30),
            (9, 15),
            (11.5, 4),
            (12.2, 0.5),
            (43, 0),
        ],
        vehicle_pdf_col="length",
        **kwargs,
    )
