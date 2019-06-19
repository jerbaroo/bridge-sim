"""
Configuration object holding simulation parameters.
"""
import numpy as np
import pandas as pd

from model import Load
from util import param_path


class Config():
    """Simulation parameters.

    NOTE:
        - the A16 data must have index column "number"
        - the A16 data must have a weight column "total_weight"
        - the A16 data must have a vehicle type column "type"

    Attributes:
        bridge: description of a bridge.

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

        # A16 data.
        a16_csv_path: str, path of the A16 CSV data.
        a16_col_names: [str], column names of the A16 CSV data.
        a16_data: the A16 data as a DataFrame, TODO: remove.
    """
    def __init__(self, bridge):
        self.bridge = bridge

        self.images_dir = "generated/images"

        # Influence line.
        self.il_mat_path_prefix = "generated/il/il-matrix"
        self.il_num_loads = 10
        self.il_unit_load = -5e4
        self.il_save_time = 1
        def get_il_mat_path():
            # param_path(self, "il", "il_mat_path_prefix", ["il_mat_path", "il_matrix"])
            return (f"{self.il_mat_path_prefix}-nl-{self.il_num_loads}"
                    + f"-ns-{self.os_num_elems()}-l-{self.il_unit_load}"
                    + f"-t-{self.il_save_time}.npy")
        self.il_mat_path = get_il_mat_path
        self._il_matrix = None
        def get_il_matrix():
            if self._il_matrix is None:
                self._il_matrix = np.load(self.il_mat_path())
            return self._il_matrix
        self.il_matrix = get_il_matrix

        # OpenSees.
        self.os_node_step = 0.2
        self.os_exe_path = "c:/Program Files/OpenSees3.0.3-x64/OpenSees.exe"
        self.os_model_template_path = "model-template.tcl"
        self.os_built_model_path = "generated/built-model.tcl"
        self.os_element_path = "generated/elem.out"
        self.os_x_path = "generated/node-x.out"
        self.os_y_path = "generated/node-y.out"
        self.os_stress_strain_path_prefix = "generated/stress-strain"
        self.os_stress_strain_path = (lambda patch:
            f"{self.os_stress_strain_path_prefix}-{patch.id}.out")

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
        self._a16_data = None
        def get_a16_data():
            if self._a16_data is None:
                self._a16_data = pd.read_csv(self.a16_csv_path,
                    usecols=self.a16_col_names, index_col="number")
            return self._a16_data
        self.a16_data = get_a16_data

        # Testing.
        self.test_settlement_loads = [Load(0.5, -5e4)]
