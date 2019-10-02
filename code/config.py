"""Simulation configuration."""
import os
from timeit import default_timer as timer
from typing import Callable, List, Optional, Tuple

import numpy as np

import config_sys
from model.bridge import Bridge, Dimensions, _reset_model_ids
from model.response import ResponseType
from vehicles import load_vehicle_data
from util import print_d, print_i, print_w

# Print debug information for this file.
D: bool = True


class Config:
    """Simulation configuration.

    NOTE: All paths are relative to the project root directory.

    Args:
        bridge: Callable[[], Bridge], returns a bridge specification.
        vehicle_data_path: str, path of the vehicle data CSV file.
        vehicle_density: List[Tuple[float, float]], density of vehicles
            below a maximum length in meters.

            Example: [(2.4, 0.5), (5.6, 94.5), (16, 5)]

            Here 5% of vehicles are 2.4m or less in length, 94.5% greater than
            2.4m and less than 5.6m, and the remaining 5% are less than 16m.
        vehicle_intensity: the total amount of vehicles per hour.
        vehicle_density_col: str, column of vehicle_data to group by.
        generated_dir: str, directory where to save generated files.

    Attrs:
        resp_matrices: Dict[str, ResponsesMatrix], response matrices in memory.
        perturb_stddev: float, standard deviation to perturb a vehicle column.
        images_dir: str, directory where to save generated images.
        image_path: Callable[[str], str], a path relative to images_dir.
        time_step: float, time interval between recording sensor responses.
        time_end: float, maximum time to record an event, may end earlier.
        fem_responses_path_prefix: str, prefix of where to save responses.
        il_num_loads: int, the number of equidistant positions to apply load.
        il_unit_load_kn: float, unit load to place on the bridge in kN.
        os_node_step: float, distance between two OpenSees nodes in meters.
        os_exe_path: str, path of the OpenSees executable.
        os_model_template_path: str, path of the OpenSees model template file.
        noise_mean: Callable[[ResponseType], float], return the mean of the
            distribution of the noise for a sensor type.
        noise_stddev: Callable[[ResponseType], float], return the standard
            deviation of the distribution of the noise for a sensor type.

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
            self, bridge: Callable[[], Bridge], vehicle_data_path: str,
            vehicle_density: List[Tuple[float, float]],
            vehicle_intensity: float, vehicle_density_col: str,
            generated_dir: Optional[str] = None):
        # Bridge.
        _reset_model_ids()
        self.bridge = bridge()

        # Vehicles.
        start = timer()
        self.vehicle_data = load_vehicle_data(vehicle_data_path)
        print_i(f"Loaded vehicle data from {vehicle_data_path} in"
                + f" {timer() - start:.2f}s")
        self.vehicle_density = vehicle_density
        self.vehicle_intensity = vehicle_intensity
        self.vehicle_density_col = vehicle_density_col
        self.perturb_stddev: float = 0.1

        # Ensure vehicle probability density sums to 1.
        density_sum = sum(map(lambda f: f[1], self.vehicle_density))
        if int(density_sum) != 100:
            print_w(f"Vehicle density sums to {density_sum}, not to 1")
            for i in range(len(self.vehicle_density)):
                self.vehicle_density[i] = (
                    self.vehicle_density[i][0],
                    self.vehicle_density[i][1] / density_sum)
            density_sum = sum(map(lambda f: f[1], self.vehicle_density))
            print_w(f"Vehicle density adjusted to sum to {density_sum:.2f}")

        # Generated data.
        self.generated_dir = "generated-data/"
        if generated_dir is not None:
            self.generated_dir = generated_dir
        self.events_dir = os.path.join(self.generated_dir, "events/")
        self.images_dir = self.generated_dir
        if self.images_dir.endswith("/"):
            self.images_dir = self.images_dir[:-1]
        self.images_dir += "-images/"
        self.image_path = lambda filename: os.path.join(
            self.images_dir, filename)

        # Influence lines.
        self.fem_responses_path_prefix: str = os.path.join(
            self.generated_dir, "responses/")
        self.resp_matrices = dict()
        self.il_num_loads: int = 100
        self.il_unit_load_kn: float = 1000

        # Event recording.
        self.time_step: float = 1 / 250  # Record at 250 Hz.
        self.time_end: float = 2  # Seconds.
        self.time_overlap: float = self.time_end * 0.1  # Seconds.
        self.event_metadata_path = os.path.join(
            self.generated_dir, "events-metadata.txt")

        #################
        ##### Noise #####
        #################
        self.noise_mean = lambda rt: {
            ResponseType.Strain: 0,
            ResponseType.Stress: 0,
            ResponseType.XTranslation: 0,
            ResponseType.YTranslation: 0
        }[rt]
        self.noise_stddev = lambda rt: {
            ResponseType.Strain: 1e-5,
            ResponseType.Stress: 1e6,
            ResponseType.XTranslation: 5e-8,
            ResponseType.YTranslation: 2e-4
        }[rt]

        #####################
        ##### OpenSees. #####
        #####################
        self.os_node_step: float = self.bridge.length / 100
        self.os_node_step_z: float = self.bridge.width / 100
        self.os_support_num_nodes_z: int = 10
        self.os_support_num_nodes_y: int = 10
        self.os_exe_path: str = config_sys.os_exe_path
        self.os_model_template_path: str = "code/model-template.tcl"
        self.os_3d_model_template_path: str = "code/model-template-3d.tcl"

        # Make directories.
        for directory in [
                self.generated_dir, self.images_dir, self.events_dir,
                self.fem_responses_path_prefix,
                os.path.join(self.images_dir, "bridges/"),
                os.path.join(self.images_dir, "ils/")]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        #######################################################################
        # TODO: Remove everything below this line #############################
        #######################################################################

        # Put all this non-configuration in OpenSees FEMRunner.
        def os_get_num_elems():
            result = int(np.round(self.bridge.length / self.os_node_step))
            print_d(D, f"os_num_elems = {result}")
            assert np.isclose(result * self.os_node_step, self.bridge.length)
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
        self.di_model_template_path = "code/diana-705-template.dat"
        self.di_model_path = "code/diana-705.dat"
        self.di_cmd_path = "code/diana-cmd.dcf"
        self.di_out_path = "code/diana-out.out"
        self.di_filos_path = "code/diana.ff"
        self.di_translation_path = "code/displa_paths.tb"
        self.di_strain_path = "code/strains_paths.tb"
