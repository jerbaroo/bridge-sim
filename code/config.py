"""
Configuration object holding simulation parameters.
"""
import os

import numpy as np
import pandas as pd

from model import Load


class Config():
    """Simulation parameters.

    NOTE:
        - the A16 data must have index column "number"
        - the A16 data must have a weight column "total_weight"
        - the A16 data must have a vehicle type column "type"

    Attributes:
        bridge: description of a bridge.
        generated_dir: directory to save all generated files.
        fig_dir: directory to save generated figures.

        # A16 data.
        a16_csv_path: str, path of the A16 CSV data.
        a16_col_names: [str], column names of the A16 CSV data.

        # Influence line.
        il_mat_path_prefix: str, prefix of path to save/load the IL matrix.
        il_num_loads: int, amount of positions at which to apply load.
        il_unit_load: float, the value of load to place on the bridge.
        il_save_time: int, time index to read the response after loading.
        il_mat_path: str, path to save/load the IL matrix.

        # OpenSees.
        os_node_step: distance between two nodes, or length of an element.
        os_exe_path: str, path of the OpenSees executable.
        os_model_template_path: str, path of the model template file.
        os_built_model_path: str, path to save/load the built model.
        os_element_path: str, path to save element recorder data.
        os_x_path: str, path to save node x translation recorder data.
        os_y_path: str, path to save node y translation recorder data.
        os_stress_strain_path: str, path to save stress/strain recorder data.
    """
    def __init__(self, bridge):
        self.bridge = bridge
        self.generated_dir = "generated/"
        self.fig_dir = os.path.join(self.generated_dir, "images/")

        # Influence line.
        self.il_mat_path_prefix = os.path.join(
            self.generated_dir, "il/il-matrix")
        self.il_unit_load = -5e4

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

        # A16 data.
        self.a16_csv_path = "../data/a16-data/A16.csv"
        self.a16_col_names = [
            "month", "day", "year", "hour", "min", "sec", "number", "lane",
            "type", "speed", "length", "total_weight", "weight_per_axle",
            "axle_distance"]
