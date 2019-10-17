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


def set_deck_node_step(c: "Config", max_shell_area: float):
    """Set the deck node step size based on a maximum shell area.

    Updates the given 'Config' and returns the final deck shell area.

    """
    # Start with the minimum possible amount of nodes.
    num_nodes_x, num_nodes_z = 2, 2

    def set_node_step():
        """Set node step size based on number of nodes."""
        c.os_node_step = c.bridge.length / (num_nodes_x - 1)
        c.os_node_step_z = c.bridge.width / (num_nodes_z - 1)

    set_node_step()
    print_d(D, f"Initial deck node step x = {c.os_node_step}")
    print_d(D, f"Initial deck node step z = {c.os_node_step_z}")
    # Function to return the current bridge deck shell area.
    deck_shell_area = lambda: c.os_node_step * c.os_node_step_z
    print_d(D, f"Initial deck shell area = {deck_shell_area()}")
    # Decrease node step size until shell's are below maximum.
    while deck_shell_area() > max_shell_area:
        # Always decrease the maximum shell side
        # (by increasing number of nodes).
        if c.os_node_step > c.os_node_step_z:
            num_nodes_x += 1
        else:
            num_nodes_z += 1
        set_node_step()
    return deck_shell_area()


def set_support_num_nodes(c: "Config", max_shell_area: float):
    """Set the support number of nodes based on a maximum shell area.

    Returns the final wall shell area.

    TODO: This assumes square supports that hang vertically. The square
        assumption means that actual maximum shell on a support will be smaller
        than it could be without being greater than max_shell_area, while the
        assumption that they hang vertically could have the opposite effect.
        This function should have approximately the intended effect, but you
        should be aware.

    """
    # Start with the minimum possible number of nodes.
    num_nodes_y, num_nodes_z = 2, 2

    def set_num_nodes():
        c.os_support_num_nodes_y = num_nodes_y
        c.os_support_num_nodes_z = num_nodes_z

    set_num_nodes()
    wall_shell_length = lambda: c.bridge.supports[0].height / (num_nodes_y + 1)
    wall_shell_height = lambda: c.bridge.supports[0].width_top / (num_nodes_z + 1)
    print_d(D, f"Initial wall shell length = {wall_shell_length()}")
    print_d(D, f"Initial wall shell height = {wall_shell_height()}")
    # Function to return the current bridge support shell area.
    wall_shell_area = lambda: wall_shell_length() * wall_shell_height()
    print_d(D, f"Initial wall shell area = {wall_shell_area()}")
    # Decrease number of nodes until shell's are below maximum.
    while wall_shell_area() > max_shell_area:
        print(f"{wall_shell_area()}")
        # Always decrease the maximum shell side.
        # (by increasing number of nodes).
        if wall_shell_length() > wall_shell_height():
            num_nodes_y += 1
        else:
            num_nodes_z += 1
        set_num_nodes()
    return wall_shell_area()


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

        max_shell_area: Optional[float], maximum shell area for deck and
            support shells in meters. NOTE: If this is set, they values of
            node_step_x, node_step_z, support_num_nodes_z, support_num_nodes_y
            will be overridden.

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
            generated_dir: str = "generated-data/",
            max_shell_area: Optional[float] = None):
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
        self.generated_dir = generated_dir
        self.events_dir = os.path.join(self.generated_dir, "events/")
        # Set images dir to generated-dir with "-images" and bridge extension.
        self.images_dir = os.path.join(
            os.path.split(self.generated_dir)[0],
            os.path.basename(self.generated_dir) + "-images",
            self.bridge.long_name().lower())
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
        if max_shell_area is not None:
            dsa = set_deck_node_step(c=self, max_shell_area=max_shell_area)
            wsa = set_support_num_nodes(c=self, max_shell_area=max_shell_area)
            print_i(f"Maximum shell area = {max_shell_area}")
            print_i(f"Deck shell area = {dsa}")
            print_i(f"Wall shell area = {wsa}")
        print_i(f"Deck node step x = {self.os_node_step}")
        print_i(f"Deck node step z = {self.os_node_step_z}")
        print_i(f"Wall num nodes y = {self.os_support_num_nodes_y}")
        print_i(f"Wall num nodes z = {self.os_support_num_nodes_z}")
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
