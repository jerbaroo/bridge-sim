"""Simulation configuration."""
import os
from typing import Callable

import numpy as np

from model import *


class Config:
    """Simulation configuration.

    NOTE:
        - Paths are relative to this file.

    Args:
        bridge: Callable[[], Bridge], returns a bridge specification.

    Attrs:
        il_matrices: Dict[str, ILMatrix], IL matrices kept in memory.
        generated_dir: str, directory where to save generated files.
        images_dir: str, directory where to save generated images.
        image_path: Callable[[str], str], a path relative to images_dir.

        # A16 data.
        a16_csv_path: str, path of the A16 CSV data.

        # Responses & influence line.
        fem_responses_path_prefix: str, prefix of where to save responses.
        il_unit_load_kn: float, unit load to place on the bridge in kN.

        # OpenSees.
        os_node_step: float, distance between two nodes in meters.
        os_exe_path: str, path of the OpenSees executable.
        os_model_template_path: str, path of the model template file.

        # Diana.
        di_exe_path: str, path of the Diana executable.
        di_model_path: str, path of the template Diana model file.
        di_model_path: str, path of the Diana model file.
        di_cmd_path: str, path of the Diana command file.
        di_out_path: str, path of the Diana output file.
        di_filos_path: str, path of the Diana filos file.
        di_max_x_elem: int, index of maximum x-axis element.

    """
    def __init__(self, bridge: Callable[[], Bridge]):
        reset_model_ids()
        self.bridge = bridge()

        self.il_matrices = dict()
        self.generated_dir = "generated/"
        self.images_dir = "images/"
        self.image_path = lambda filename: os.path.join(
            self.images_dir, filename)

        # Make directories.
        for directory in [self.generated_dir, self.images_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # A16 data.
        self.a16_csv_path = "../data/a16-data/A16.csv"

        # Responses & influence line.
        self.fem_responses_path_prefix = os.path.join(
            self.generated_dir, "responses/responses")
        self.il_unit_load_kn = 1000

        # OpenSees.
        self.os_exe_path = "c:/Program Files/OpenSees3.0.3-x64/OpenSees.exe"
        self.os_model_template_path = "model-template.tcl"
        self.os_node_step = 0.2

        # Put all this non-configuration in OpenSees FEMRunner.
        def os_get_num_elems():
            result = int(self.bridge.length / self.os_node_step)
            assert result * self.os_node_step == self.bridge.length
            return result
        os_get_num_elems()
        self.os_num_elems = os_get_num_elems
        self.os_num_nodes = lambda: self.os_num_elems() + 1
        self.os_node_ids = lambda: np.arange(1, self.os_num_nodes() + 1)
        assert len(list(self.os_node_ids())) == self.os_num_nodes()
        self.os_elem_ids = lambda: np.arange(1, self.os_num_elems() + 1)
        assert len(list(self.os_elem_ids())) == self.os_num_elems()

        # Diana.
        self.di_exe_path = "c:/Program Files/Diana 10.3/bin/diana.exe"
        self.di_model_template_path = "diana-705-template.dat"
        self.di_model_path = "diana-705.dat"
        self.di_cmd_path = "diana-cmd.dcf"
        self.di_out_path = "diana-out.out"
        self.di_filos_path = "diana.ff"
        self.di_translation_path = "displa_paths.tb"
        self.di_strain_path = "strains_paths.tb"


def bridge_705_config() -> Config:
    return Config(bridge_705)
