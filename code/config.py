"""Simulation configuration."""
import os
from typing import Callable, List, Tuple

import numpy as np
import pandas as pd

from model import *


class Config:
    """Simulation configuration.

    Args:
        bridge: Callable[[], Bridge], returns a bridge specification.
        vehicle_data: pd.DataFrame, describes vehicles on the bridge.
        TODO: Make vehicle density group a parameters.
        vehicle_density: List[Tuple[float, float]], density of vehicles
            below a maximum length in meters.

            Example: [(2.4, 0.5), (5.6, 94.5), (16, 5)]

            Here 5% of vehicles are 2.4m or less in length, 94.5% greater than
            2.4m and less than 5.6m, and the remaining 5% are less than 16m.
        vehicle intensity: the total amount of vehicles per hour.
        vehicle_density_col: str, column of vehicle_data to group on.

    Attrs:
        il_matrices: Dict[str, ILMatrix], IL matrices kept in memory.
        generated_dir: str, directory where to save generated files.
        images_dir: str, directory where to save generated images.
        image_path: Callable[[str], str], a path relative to images_dir.
        fem_responses_path_prefix: str, prefix of where to save responses.
        il_unit_load_kn: float, unit load to place on the bridge in kN.
        os_node_step: float, distance between two OpenSees nodes in meters.
        os_exe_path: str, path of the OpenSees executable.
        os_model_template_path: str, path of the OpenSees model template file.

        # Diana.
        di_exe_path: str, path of the Diana executable.
        di_model_path: str, path of the template Diana model file.
        di_model_path: str, path of the Diana model file.
        di_cmd_path: str, path of the Diana command file.
        di_out_path: str, path of the Diana output file.
        di_filos_path: str, path of the Diana filos file.
        di_max_x_elem: int, index of maximum x-axis element.

    """
    def __init__(
            self, bridge: Callable[[], Bridge], vehicle_data: pd.DataFrame,
            vehicle_density: List[Tuple[float, float]],
            vehicle_intensity: float, vehicle_density_col: str="length"):
        reset_model_ids()
        self.bridge = bridge()
        self.vehicle_data = vehicle_data
        self.vehicle_density=vehicle_density
        self.vehicle_intensity=vehicle_intensity
        self.vehicle_density_col=vehicle_density_col

        density_sum = sum(map(lambda f: f[1], self.vehicle_density))
        if int(density_sum) != 100:
            print_w(
                f"Vehicle density did not sum to 1, was {density_sum},"
                + " adjusting...")
            for i in range(len(self.vehicle_density)):
                self.vehicle_density[i] = (
                    self.vehicle_density[i][0],
                    self.vehicle_density[i][1] / density_sum)
            density_sum = sum(map(lambda f: f[1], self.vehicle_density))
            print_w(f"Vehicle density sums to {density_sum:.2f}")

        self.il_matrices = dict()
        self.generated_dir = "generated/"
        self.images_dir = "images/"
        self.image_path = lambda filename: os.path.join(
            self.images_dir, filename)

        # Make directories.
        # TODO: create savefig which created directories as needed.
        for directory in [self.generated_dir, self.images_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Responses & influence line.
        self.fem_responses_path_prefix = os.path.join(
            self.generated_dir, "responses/responses")
        self.il_unit_load_kn = 1000

        # OpenSees.
        self.os_node_step = 0.2
        self.os_exe_path = "c:/Program Files/OpenSees3.0.3-x64/OpenSees.exe"
        self.os_model_template_path = "model-template.tcl"

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
        # TODO: Move all this to Diana FEMRunner.
        self.di_exe_path = "c:/Program Files/Diana 10.3/bin/diana.exe"
        self.di_model_template_path = "diana-705-template.dat"
        self.di_model_path = "diana-705.dat"
        self.di_cmd_path = "diana-cmd.dcf"
        self.di_out_path = "diana-out.out"
        self.di_filos_path = "diana.ff"
        self.di_translation_path = "displa_paths.tb"
        self.di_strain_path = "strains_paths.tb"
