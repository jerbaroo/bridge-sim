"""
Configuration object holding simulation parameters.
"""
import os

import numpy as np
import pandas as pd

from model import bridge_705, Load


class Config():
    """Simulation parameters.

    NOTE:
        - the A16 data must have index column "number"
        - the A16 data must have a weight column "total_weight"
        - the A16 data must have a vehicle type column "type"

    Attributes:
        bridge: description of a bridge.
        generated_dir: str, directory where to save all generated files.
        fig_dir: str, directory where to save generated figures.
    
        # A16 data.
        a16_csv_path: str, path of the A16 CSV data.
        a16_col_names: [str], column names of the A16 CSV data.

        # Responses & influence line.
        fem_responses_path_prefix: str, prefix of path to save/load responses.
        il_unit_load: float, unit load to place on the bridge.

        # OpenSees.
        os_node_step: float, distance between two nodes (element length).
        os_exe_path: str, path of the OpenSees executable.
        os_model_template_path: str, path of the model template file.
        os_built_model_path: str, path to save/load the built model.
        os_element_path: str, path to save element recorder data.
        os_x_path: str, path to save node x translation recorder data.
        os_y_path: str, path to save node y translation recorder data.
        os_stress_strain_path_prefix: str, prefix of the path to save
            stress/strain recorder data.

    """
    def __init__(self, bridge):
        self.bridge = bridge

        __dir__ = os.path.dirname(os.path.realpath(__file__))
        self.generated_dir = os.path.normpath(
            os.path.join(__dir__, "generated/"))
        self.images_dir = os.path.normpath(
            os.path.join(self.generated_dir, "images/"))
        for directory in [self.generated_dir, self.images_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # A16 data.
        self.a16_csv_path = "../data/a16-data/A16.csv"
        self.a16_col_names = [
            "month", "day", "year", "hour", "min", "sec", "number", "lane",
            "type", "speed", "length", "total_weight", "weight_per_axle",
            "axle_distance"]

        # Responses & influence line.
        self.fem_responses_path_prefix = os.path.join(
            self.generated_dir, "responses/responses")
        self.il_unit_load = 1e2

        # OpenSees.
        self.os_node_step = 0.2
        self.os_exe_path = "c:/Program Files/OpenSees3.0.3-x64/OpenSees.exe"
        self.os_model_template_path = "model-template.tcl"
        self.os_built_model_path = os.path.join(
            self.generated_dir, "built-model.tcl")
        self.os_element_path = os.path.join(self.generated_dir, "elem.out")
        self.os_x_path = os.path.join(self.generated_dir, "node-x.out")
        self.os_y_path = os.path.join(self.generated_dir, "node-y.out")
        self.os_stress_strain_path_prefix = os.path.join(
            self.generated_dir, "stress-strain")

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


bridge_705_config = Config(bridge_705)
