"""Simulation configuration object."""

import os
from timeit import default_timer as timer
from typing import Callable, List, Tuple

from lib.model.bridge import Bridge
from lib.vehicles import load_vehicle_data
from util import print_i, print_w

# Print debug information for this file.
D: bool = True


def _get_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


class Config:
    def __init__(
        self,
        bridge: Callable[[], Bridge],
        fem_runner: Callable[[], "FEMRunner"],
        vehicle_data_path: str,
        vehicle_pdf: List[Tuple[float, float]],
        vehicle_pdf_col: str,
        generated_data: str = "generated-data",
        shorten_paths: bool = False,
    ):
        """Simulation configuration object.

        Combines a Bridge and FEMRunner among other things.

        :param bridge: function that returns a bridge.
        :param fem_runner:
        :param vehicle_data_path: path of the vehicle CSV file.
        :param vehicle_pdf:
            percentage of vehicles below a maximum value for that column.

            Example: [(2.4, 0.5), (5.6, 94.5), (16, 5)]

            Here 5% of vehicles are 2.4m or less in length, 94.5% greater than
            2.4m and less than 5.6m, and the remaining 5% are less than 16m.
            This applies if 'vehicle_pdf_col' is "length".
        :param vehicle_pdf_col: column of vehicle_data to group by.
        :param generated_data: directory where to save generated files.
        :param shorten_paths: shorten simulation paths.
        """
        # Bridge.
        # TODO: Move reset call into Bridge constructor.
        self._bridge = bridge
        self.bridge = self._bridge()
        self._fem_runner = fem_runner
        self.fem_runner = self._fem_runner(self)

        # OpenSees
        self.os_model_template_path: str = "model-template.tcl"
        self.os_3d_model_template_path: str = "model-template-3d.tcl"

        # Simulation performance.
        self.parallel = 1
        self.parallel_ulm = True
        self.shorten_paths = shorten_paths
        self.resp_matrices = dict()

        # Unit loads.
        self.il_num_loads: int = 600
        self.il_unit_load_kn: float = 1000
        self.pd_unit_disp: float = 1.0
        self.pd_unit_load_kn: int = 10
        self.unit_axial_delta_temp_c: int = 1
        self.unit_moment_delta_temp_c: int = 1
        self.cte = 12e-6

        # Responses & events.
        self.sensor_hz: float = 1 / 100
        self.event_time_s: float = 2  # Seconds.

        # Vehicles.
        self.perturb_stddev: float = 0.1
        self.axle_width: float = 2.5
        self.vehicle_pdf = vehicle_pdf
        self.vehicle_pdf_col = vehicle_pdf_col
        start = timer()
        self.vehicle_data_path = vehicle_data_path
        self.vehicle_data = load_vehicle_data(vehicle_data_path)
        print_i(
            f"Loaded vehicle data from {vehicle_data_path} in"
            + f" {timer() - start:.2f}s"
        )

        # Ensure vehicle probability density sums to 1.
        pdf_sum = sum(map(lambda f: f[1], self.vehicle_pdf))
        if int(pdf_sum) != 100:
            pre_pdf_sum = pdf_sum
            for i in range(len(self.vehicle_pdf)):
                self.vehicle_pdf[i] = (
                    self.vehicle_pdf[i][0],
                    self.vehicle_pdf[i][1] / pdf_sum,
                )
            pdf_sum = sum(map(lambda f: f[1], self.vehicle_pdf))
            print_w(f"Vehicle PDF sums to {pre_pdf_sum}, adjusted to sum to 1")

        # Root directories for generated data.
        self.root_generated_data_dir = _get_dir(generated_data)
        if self.root_generated_data_dir[-1] in "/\\":
            raise ValueError("generated_data must not end in path separator")
        self.root_generated_images_dir = lambda: _get_dir(
            os.path.join(self.root_generated_data_dir + "-images")
        )

    # Bridge-specific directories for generated data.

    def generated_data_dir(self):
        return _get_dir(
            os.path.join(
                self.root_generated_data_dir,
                self.bridge.id_str(),
                self.bridge.type if self.bridge.type is not None else "healthy",
            )
        )

    def generated_images_dir(self):
        return _get_dir(
            os.path.join(
                self.root_generated_images_dir(),
                self.bridge.id_str(),
                self.bridge.type if self.bridge.type is not None else "healthy",
            )
        )

    # Bridge-specific but accuracy-independent directories.

    def generated_data_dir_no_acc(self):
        return _get_dir(
            os.path.join(
                self.root_generated_data_dir,
                self.bridge.id_str(acc=False),
                self.bridge.type if self.bridge.type is not None else "healthy",
            )
        )

    def generated_images_dir_no_acc(self):
        return _get_dir(
            os.path.join(
                self.root_generated_images_dir(),
                self.bridge.id_str(acc=False),
                self.bridge.type if self.bridge.type is not None else "healthy",
            )
        )

    def get_path_in(self, in_: str, dirname: str, filename: str):
        """Filepath in a directory in a directory (created if necessary).

        TODO: Use safe_str here.

        """
        dirpath = os.path.join(in_, dirname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return os.path.join(dirpath, filename)

    def get_data_path(
        self, dirname: str, filename: str, bridge: bool = True, acc: bool = True
    ):
        """Get a bridge-specific image path in a named directory."""
        dir_path = self.generated_data_dir()
        if not bridge:
            dir_path = self.root_generated_images_dir()
        elif not acc:
            dir_path = self.generated_data_dir_no_acc()
        return self.get_path_in(dir_path, dirname, filename)

    def get_image_path(
        self, dirname: str, filename: str, bridge: bool = True, acc: bool = True
    ):
        """Get a bridge-specific image path in a named directory."""
        dir_path = self.generated_images_dir()
        if not bridge:
            dir_path = self.root_generated_images_dir()
        elif not acc:
            dir_path = self.generated_images_dir_no_acc()
        return self.get_path_in(dir_path, dirname, filename)