import os
from typing import Optional

import findup

from lib.config import Config
from lib.fem.run.opensees import os_runner
from lib.model.bridge import Bridge


proj_dir = os.path.dirname(findup.glob(".git"))


def opensees_default(bridge: Bridge, os_exe: Optional[str] = None, **kwargs) -> Config:
    return Config(
        bridge=bridge,
        fem_runner=os_runner(os_exe),
        vehicle_data_path=os.path.join(proj_dir, "data/traffic/traffic.csv"),
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
