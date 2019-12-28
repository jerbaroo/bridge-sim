"""Simulation configuration object."""
import os
from copy import deepcopy
from timeit import default_timer as timer
from typing import Callable, List, Tuple

import config_sys
from model.bridge import Bridge, _reset_model_ids
from model.response import ResponseType
from vehicles import load_vehicle_data
from util import print_i, print_w

# Print debug information for this file.
D: bool = True


def _get_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


class Config:
    """Simulation configuration object.

    In addition to the arguments of this constructor you may want to change the
    attributes of this 'Config' object. Please see the source of this 'Config'
    object directly for definition and comments, do not depend on documentation.

    Args:
        bridge: Callable[[], Bridge], returns a bridge specification.
        vehicle_data_path: str, path of the vehicle data CSV file.
        vehicle_pdf_col: str, column of vehicle_data to group by.
        vehicle_pdf: List[Tuple[float, float]], density of vehicles below a
            maximum value for that column.

            Example: [(2.4, 0.5), (5.6, 94.5), (16, 5)]

            Here 5% of vehicles are 2.4m or less in length, 94.5% greater than
            2.4m and less than 5.6m, and the remaining 5% are less than 16m.
            This applies if 'vehicle_pdf_col' is "length".
        generated_data: str, directory where to save generated files.

    """

    def __init__(
        self,
        bridge: Callable[[], Bridge],
        vehicle_data_path: str,
        vehicle_pdf: List[Tuple[float, float]],
        vehicle_pdf_col: str,
        generated_data: str = "generated-data",
    ):
        # Bridge.
        # TODO: Move reset call into Bridge constructor.
        self.bridge = bridge()

        # OpenSees
        self.os_exe_path: str = config_sys.os_exe_path
        self.os_model_template_path: str = "code/model-template.tcl"
        self.os_3d_model_template_path: str = "code/model-template-3d.tcl"

        # Simulation settings.
        self.parallel = False
        self.resp_matrices = dict()
        self.il_num_loads: int = 100
        self.il_unit_load_kn: float = 1000
        self.pd_unit_disp: float = 1.0
        self.pd_unit_load_kn: int = 10
        self.unit_axial_delta_temp_c: int = 1
        self.unit_moment_delta_temp_c: int = 1

        # Responses & events.
        self.sensor_hz: float = 1 / 250  # Record at 250 Hz.
        self.time_end: float = 2  # Seconds.
        self.time_overlap: float = self.time_end * 0.1  # Seconds.

        # Noise
        self.noise_mean = lambda rt: {
            ResponseType.Strain: 0,
            ResponseType.Stress: 0,
            ResponseType.XTranslation: 0,
            ResponseType.YTranslation: 0,
        }[rt]
        self.noise_stddev = lambda rt: {
            ResponseType.Strain: 1e-5,
            ResponseType.Stress: 1e6,
            ResponseType.XTranslation: 5e-8,
            ResponseType.YTranslation: 1e-5,
        }[rt]

        # Vehicles.
        self.perturb_stddev: float = 0.1
        self.axle_width: float = 2.5
        self.vehicle_pdf = vehicle_pdf
        self.vehicle_pdf_col = vehicle_pdf_col
        start = timer()
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
