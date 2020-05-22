"""Plots based on the ExptResponses classes."""
from typing import Optional

from config import Config
from fem.responses.matrix.dc import DCMatrix
from fem.responses.matrix.il import ILMatrix
from fem.run import FEMRunner
from fem.run.opensees import OSRunner
from model.bridge import Dimensions
from model.bridge.util import wheel_tracks
from model.response import ResponseType
from plot.matrices import imshow_il, matrix_subplots, plot_dc, plot_il


def il_plots(
    c: Config,
    num_loads: int = 100,
    num_subplot_ils: int = 12,
    fem_runner: Optional[FEMRunner] = None,
):
    """Make plots of the influence lines.

    Args:
        c: Config, global configuration object.
        num_loads: int, the number of loading positions or influence lines.
        num_subplot_ils: int, the number of influence lines on the subplots.
        fem_runner: Optional[FEMRunner], FEM program to run simulations with,
            default is OpenSees.

    """
    original_il_num_loads = c.il_num_loads
    c.il_num_loads = num_loads
    if fem_runner is None:
        fem_runner = OSRunner(c)

    pload_z_fracs = [None]  # A single wheel track value ignored for 2D.

    # If a 3D FEM then generate IL plots for each wheel track.
    if c.bridge.dimensions == Dimensions.D3:
        pload_z_fracs = wheel_tracks(c)

    for pload_z_frac in pload_z_fracs:
        for response_type in fem_runner.supported_response_types(c.bridge):

            # TODO: Remove once Stress and Strain are fixed.
            if c.bridge.dimensions == Dimensions.D3 and response_type in [
                ResponseType.Stress,
                ResponseType.Strain,
            ]:
                continue

            il_matrix = ILMatrix.load(
                c=c,
                response_type=response_type,
                fem_runner=fem_runner,
                load_z_frac=pload_z_frac,
            )

            filename = pstr(
                f"{il_matrix.fem_runner.name}-{response_type.name()}"
                + f"-loadz={c.bridge.z(pload_z_frac):.2f}-numloads-{num_loads}"
            )

            imshow_il(
                c=c,
                il_matrix=il_matrix,
                num_loads=num_loads,
                num_sensors=num_loads,
                save=c.get_image_path("ils", f"imshow-{filename}"),
            )

            matrix_subplots(
                c=c,
                resp_matrix=il_matrix,
                num_subplots=num_subplot_ils,
                num_x=num_loads,
                plot_func=plot_il,
                z_frac=il_matrix.load_z_frac,
                save=c.get_image_path("ils", f"subplots-{filename}"),
            )
    c.il_num_loads = original_il_num_loads


def dc_plots(
    c: Config,
    num_loads: int = 100,
    num_subplot_ils: int = 12,
    fem_runner: Optional[FEMRunner] = None,
):
    """Make plots of the displacement control fem.

    Args:
        c: Config, global configuration object.
        num_loads: int, the number of loading positions or influence lines.
        num_subplot_ils: int, the number of influence lines on the subplots.
        fem_runner: Optional[FEMRunner], FEM program to run simulations with,
            default is OpenSees.

    """
    num_piers = len(c.bridge.supports)

    if fem_runner is None:
        fem_runner = OSRunner(c)

    pload_z_fracs = [None]  # A single wheel track value ignored for 2D.

    # If a 3D FEM then generate DC plots for each wheel track.
    if c.bridge.dimensions == Dimensions.D3:
        pload_z_fracs = wheel_tracks(c)

    for pload_z_frac in pload_z_fracs:
        for response_type in fem_runner.supported_response_types(c.bridge):

            # Make the influence line imshow matrix.
            dc_matrix = DCMatrix.load(
                c=c, response_type=response_type, fem_runner=OSRunner(c)
            )

            filename = (
                f"subplots-{dc_matrix.fem_runner.name}"
                + f"-{response_type.name()}"
                + f"-numexpts-{dc_matrix.num_expts}"
            )

            matrix_subplots(
                c=c,
                resp_matrix=dc_matrix,
                num_x=num_x,
                plot_func=plot_dc,
                save=c.get_image_path("dcs", f"subplots-{filename}"),
            )
    c.il_num_loads = original_num_ils
