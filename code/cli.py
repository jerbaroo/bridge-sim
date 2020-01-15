"""Command line interface to bridge-sim."""
import os

import click

from classify.vehicle import wagen1, wagen1_x_pos
from make import paramselect
from make.data import simulations
from make.plot import classification as classification_
from make.plot import contour as contour_
from make.plot import geometry as geometry_
from make.plot import vehicle, verification
from model.bridge.bridge_705 import (
    bridge_705_2d,
    bridge_705_3d,
    bridge_705_config,
    bridge_705_low_config,
    bridge_705_med_config,
    bridge_705_single_sections,
)
from util import clean_generated, print_i


c = None
c_func = None
two_materials_ = None
parallel_ = None


def bridge_705_3d_overload(*args, **kwargs):
    return bridge_705_3d(
        *args,
        **kwargs,
        single_sections=(bridge_705_single_sections if two_materials_ else None),
    )


@click.group()
@click.option(
    "--dimensions", type=click.Choice(["2", "3"]), default="3", help="2D or 3D bridge.",
)
@click.option(
    "--mesh",
    type=click.Choice(["low", "med", "full"]),
    default="low",
    help="Mesh density of the bridge.",
)
@click.option(
    "--two-materials",
    is_flag=True,
    help="One material for the deck and one for piers.",
)
@click.option(
    "--parallel", is_flag=True, default=True, help="Run simulations in parallel.",
)
@click.option(
    "--save", is_flag=True, default=False, help="Save/load data from a special folder.",
)
def cli(dimensions: str, mesh: str, two_materials: bool, parallel: bool, save: bool):
    if dimensions == 2 and two_materials:
        raise ValueError("--two-materials option only valid for a 3D bridge")
    global c
    global c_func
    global two_materials_
    click.echo(f"Dimensions: {dimensions}")
    click.echo(f"Mesh density: {mesh}")
    click.echo(f"Two materials: {two_materials}")
    click.echo(f"Parallel: {parallel}")
    two_materials_ = two_materials
    parallel_ = parallel
    if mesh == "low":
        c_func = bridge_705_low_config
    elif mesh == "med":
        c_func = bridge_705_med_config
    elif mesh == "full":
        c_func = bridge_705_config
    if save:
        og_c_func = c_func

        def c_func_save(*args, **kwargs):
            result_c = og_c_func(*args, **kwargs)
            result_c.root_generated_data_dir = (
                "saved-" + result_c.root_generated_data_dir
            )
            return result_c

        c_func = c_func_save
    if dimensions == "3":
        c = lambda: c_func(bridge_705_3d_overload)
    elif dimensions == "2":
        c = lambda: c_func(bridge_705_2d)


################
##### Util #####
################


@cli.command(help="Remove simulation data for the selected bridge.")
def clean():
    """TODO: Require confirmation."""
    clean_generated(c())


################
##### Util #####
################


@cli.group(help="Print and plot useful information.")
def info():
    pass


@info.command(help="Print information about this bridge.")
@click.option("--piers", is_flag=True)
def bridge(piers):
    config = c()
    config.bridge.print_info(c=config, pier_fix_info=piers)


@info.command(help="Z positions of the wheel tracks, in meters.")
def wheel_tracks():
    config = c()
    print_i(f"Wheel tracks: {config.bridge.wheel_tracks(config)}")


@info.command(help="Print and plot information on Truck 1.")
def truck_1():
    vehicle.wagen1_plot(c())
    print_i(f"Truck 1 x positions: {wagen1_x_pos()}")


@info.command(help="Load position and intensity per wheel of Truck 1.")
@click.option(
    "--x",
    type=float,
    required=True,
    help="X position of front axle of Truck 1, in meters.",
)
def truck_1_loads(x: float):
    config = c()
    time = wagen1.time_at(x=x, bridge=config.bridge)
    print_i(f"Time = {time:.4f}s")
    axle_loads = wagen1.to_point_loads(time=time, bridge=config.bridge)
    for i in range(len(axle_loads)):
        print_i(
            f"Axle {i}: ({axle_loads[i][0].repr(config.bridge)}), "
            f" ({axle_loads[i][1].repr(config.bridge)})"
        )


@info.command(help="Correlation of temperature and response.")
def thermal_correlation():
    pass


####################
##### Geometry #####
####################


@cli.group(help="Informative plots of a bridge's geometry.")
def geometry():
    pass


@geometry.command(help="Shells in 3D coloured by material properties.")
def shells_3d():
    geometry_.make_shell_properties_3d(c())


@geometry.command(help="Top view of shells coloured by material properties.")
def shells_top():
    geometry_.make_shell_properties_top_view(c())


@geometry.command(help="3D scatter plot of FEM nodes.")
def nodes():
    geometry_.make_node_plots(c())


######################
##### Simulation #####
######################


@cli.group(help="Run simulations and generate data.")
def simulate():
    pass


@simulate.command(help="Run all unit load simulations.")
def uls():
    simulations.run_uls(c())


@simulate.command(help="Record information for convergence plots.")
def converge():
    verification.make_convergence_data(c())


@simulate.command(help="Record strain convergence for pier settlement.")
@click.option("--pier", type=int, required=True, help="Index of the pier to settle.")
@click.option("--ignore", type=float, required=True, help="Radius around pier lines to ignore.")
@click.option("--dist", type=float, required=True, help="Distance around point to collect.")
def converge_pier(pier, ignore, dist):
    verification.make_pier_convergence_data(
        c=c(),
        pier_i=pier,
        strain_ignore_radius=ignore,
        max_distance=dist,
    )


######################
##### Validation #####
######################


@cli.group(help="Validate the generated FEM of bridge 705.")
def validate():
    pass


@validate.command(help="Contour plots comparing OpenSees and Diana.")
@click.option("--run-only", is_flag=True, help="Only run simulations, don't plot.")
def diana_comp(run_only: float):
    contour_.comparison_plots_705(c=c(), run_only=run_only)


@validate.command(help="Regression plots against bridge 705 measurements.")
def r2():
    verification.r2_plots(c())


@validate.command(help="Plot convergence as model size increases.")
def convergence():
    verification.plot_convergence(c())


@validate.command(help="Plot convergence in compass directions from point.")
@click.option("--filename", type=str, required=True, help="Filename of data to plot.")
@click.option("--title", type=str, required=True, help="Title inset, describing the point.")
@click.option("--label", type=str, required=True, help="String appended to plot filename.")
def nesw_conv(filename: str, title: str, label: str):
    config = c()
    convergence_dir = os.path.dirname(
        config.get_image_path("convergence", "_", bridge=False))
    verification.plot_nesw_strain_convergence(
        c=config,
        filepath=os.path.join(convergence_dir, filename),
        from_=title,
        label=label,
    )


@validate.command(help="Contour plots of unit thermal deck loading.")
def thermal():
    from make.plot.contour import thermal
    thermal.make_axis_plots(c())
    thermal.unit_axial_thermal_deck_load(c())
    # thermal.unit_moment_thermal_deck_load(c())
    # thermal.unit_thermal_deck_load(c())


@validate.command(help="Comparison of sensor measurements, OpenSees & Diana.")
def sensors():
    verification.per_sensor_plots(c=c(), strain_sensors_startwith="O")
    verification.per_sensor_plots(c=c(), strain_sensors_startwith="T")


@validate.command(help="Contour plots of unit pier displacement.")
def pier_disp():
    contour_.piers_displaced(c())


@validate.command(help="Confirm that density has no effect on simulation.")
def density():
    from make import validate
    validate.density_no_effect(c())


#################
##### Param #####
#################


@cli.command(help="Plot for parameter selection of #ULS.")
def param_uls():
    paramselect.number_of_uls_plot(c())


####################
##### Contour #####
####################


@cli.group(help="Contour plots for loading & damage scenarios.")
def contour():
    pass


@contour.command(help="3D angled contour plot of bridge 705.")
@click.option(
    "--x",
    type=float,
    required=True,
    help="X position of front axle of Truck 1, in meters.",
)
@click.option(
    "--deform", type=float, required=True, help="Deformation amplitude, in meters."
)
def cover_photo(x: float, deform: float):
    contour_.cover_photo(c=c(), x=x, deformation_amp=deform)


@contour.command(help="Response to traffic at multiple timesteps, per scenario.")
def scenarios_traffic():
    contour_.traffic_response_plots(c())


@contour.command(help="Response to point loads per scenario.")
def scenarios_point_load():
    contour_.point_load_response_plots(c())


@contour.command(help="Cracked concrete under normal traffic.")
def traffic_concrete():
    pass


@contour.command(help="Unit thermal deck load under normal traffic.")
@click.option("--axial", type=float, required=True)
@click.option("--moment", type=float, required=True)
def traffic_thermal(axial, moment):
    from make.plot.contour.traffic_thermal import thermal_deck_load
    thermal_deck_load(c(), axial_delta_temp=axial, moment_delta_temp=moment)


#################
##### Debug #####
#################


@cli.group(help="Debug this system.")
def debug():
    pass


@debug.command(help="TCL files & contour plots for mesh refinement.")
@click.option("--build", type=bool, default=True)
@click.option("--plot", type=bool, default=True)
def refinement_tcls(build: bool, plot: bool):
    from make import debug
    debug.mesh_refinement(c=c(), build=build, plot=plot)


##########################
##### Classification #####
##########################


@cli.group(help="Run classification experiments.")
def classify():
    pass


@classify.command()
def oneclass():
    classification_.oneclass(c())


@classify.command()
@click.option("--load", type=bool, default=False, help="Load calculated features from disk.")
def pairwise_cluster_2(load):
    classification_.pairwise_cluster(c=c(), load=load)


@classify.command()
def pairwise_sensors():
    classification_.pairwise_sensors(c())


if __name__ == "__main__":
    cli()
