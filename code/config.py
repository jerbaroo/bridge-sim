"""
Configuration object holding simulation parameters and data.
"""
import numpy as np
import pandas as pd


class Config():
    """Simulation parameters and data.

    Args:
        bridge: description of a bridge.

        TODO: Move to Bridge.
        node_start: position on the x-axis of the first node.
        TODO: Move to OpenSees.
        node_step: distance between two nodes, or length of an element.

        # Influence line.
        il_mat_path_prefix: str, prefix of path to save/load the IL matrix.
        il_num_loads: int, amount of positions at which to apply load.
        il_unit_load: float, the value of load to place on the bridge.
        il_save_time: int, time index to read the response after loading.
        il_mat_path: str, path to save/load the IL matrix.
        il_matrix: load the IL matrix into a numpy matrix.

        # OpenSees.
        os_exe_path: str, path of the OpenSees executable.
        os_model_template_path: str, path of the model template file.
        os_built_model_path: str, path to save/load the built model.
        os_element_path: str, path to save element recorder data.
        os_x_path: str, path to save node x translation recorder data.
        os_y_path: str, path to save node y translation recorder data.
        os_stress_strain_path: str, path to save stress/strain recorder data.

        # A16 data.
        a16_raw_path: str, path of the raw A16 traffic load data.
        a16_csv_path: str, path of the CSV A16 traffic load data.
        a16_col_names: [str], column names of the A16 traffic load data.

    NOTE, some assumptions are made:
      - the A16 data must have index column "number"
      - the A16 data must have a weight column "total_weight"
    """
    def __init__(self, bridge, node_start=0, node_step=0.2,
                 il_mat_path_prefix="generated/il/il-matrix", il_num_loads=10,
                 il_unit_load=-5e4, il_save_time=1,
                 os_exe_path="c:/Program Files/OpenSees3.0.3-x64/OpenSees.exe",
                 os_model_template_path="model-template.tcl",
                 os_built_model_path="generated/built-model.tcl",
                 os_element_path="generated/elem.out",
                 os_x_path="generated/node-x.out",
                 os_y_path="generated/node-y.out",
                 os_stress_strain_path_prefix="generated/stress-strain",
    ):
        self.bridge = bridge

        # Nodes and elements.
        self.node_start = node_start
        self.node_step = node_step
        def get_num_elems():
            result = int(self.bridge.length / self.node_step)
            assert result * self.node_step == self.bridge.length
            return result
        get_num_elems()
        self.num_elems = get_num_elems
        self.num_nodes = lambda: self.num_elems() + 1
        self.node_ids = lambda: np.arange(1, self.num_nodes() + 1)
        assert len(list(self.node_ids())) == self.num_nodes()
        self.elem_ids = lambda: np.arange(1, self.num_elems() + 1)
        assert len(list(self.elem_ids())) == self.num_elems()

        # Influence line.
        self.il_mat_path_prefix = il_mat_path_prefix
        self.il_num_loads = il_num_loads
        self.il_unit_load = il_unit_load
        self.il_save_time = il_save_time
        def get_il_mat_path():
            return (f"{self.il_mat_path_prefix}-nl-{self.il_num_loads}"
                    + f"-ns-{self.num_elems()}-l-{self.il_unit_load}"
                    + f"-t-{il_save_time}.npy")
        self.il_mat_path = get_il_mat_path
        self.il_matrix = lambda: np.load(self.il_mat_path())

        # OpenSees.
        self.os_exe_path = os_exe_path
        self.os_model_template_path = os_model_template_path
        self.os_built_model_path = os_built_model_path
        self.os_element_path = os_element_path
        self.os_x_path = os_x_path
        self.os_y_path = os_y_path
        self.os_stress_strain_path_prefix = os_stress_strain_path_prefix
        self.os_stress_strain_path = (lambda patch:
            f"{self.os_stress_strain_path_prefix}-{patch.id}.out")

        # A16 data.
        self.a16_raw_path = "../data/a16-data/A16.dat"
        self.a16_csv_path = "../data/a16-data/A16.csv"
        self.a16_col_names = [
            "month", "day", "year", "hour", "min", "sec", "number", "lane",
            "type", "speed", "length", "total_weight", "weight_per_axle",
            "axle_distance"
        ]
        self._a16_data = None
        self._a16_data_path = None
        self._a16_col_names = None
        def get_a16_data():
            if (self._a16_data_path == self.a16_csv_path
                and self._a16_col_names == self.a16_col_names):
                return self._a16_data
            self._a16_data = pd.read_csv(
                self.a16_csv_path, usecols=self.a16_col_names,
                index_col="number"
            )
            self._a16_data_path = self.a16_csv_path
            self._a16_col_names = self.a16_col_names
            return self._a16_data
        self.a16_data = get_a16_data
