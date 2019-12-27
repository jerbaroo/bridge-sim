"""Command line interface to bridge-sim."""
import click

from classify.vehicle import wagen1, wagen1_x_pos
from config import Config
from make.data import simulations
from make.plot import classification as classification_
from make.plot import contour as contour_
from make.plot import geometry as geometry_
from make.plot import material, vehicle, verification
from model.bridge.bridge_705 import (
    bridge_705_2d,
    bridge_705_3d,
    bridge_705_config,
    bridge_705_debug_config,
    bridge_705_test_config,
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
    type=click.Choice(["debug", "low", "full"]),
    default="debug",
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
    if mesh == "debug":
        c_func = bridge_705_debug_config
    elif mesh == "low":
        c_func = bridge_705_test_config
    elif mesh == "full":
        c_func = bridge_705_config
    if save:
        og_c_func = c_func

        def c_func_save(*args, **kwargs):
            result_c = og_c_func(*args, **kwargs)
            result_c.root_generated_data_dir = "saved-" + result_c.root_generated_data_dir
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


@info.command(help="Print a summary of this bridge.")
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


@info.command(help="Plot the material properties of this bridge.")
def materials():
    material.material_property_plots(c())


####################
##### Geometry #####
####################


@cli.group(help="Plots of the geometry of the bridge.")
def geometry():
    pass


@geometry.command(help="Shells coloured by material properties.")
def shells():
    geometry_.make_shell_plots(c())


@geometry.command(help="Nodes coloured by material properties.")
def nodes():
    geometry_.make_cloud_of_node_plots(c())


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
def convergence():
    verification.make_convergence_data(c())


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


@validate.command(help="Plot of model convergence as model size increases.")
def convergence():
    verification.plot_convergence(c())


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
    "--deform",
    type=float,
    required=True,
    help="Deformation amplitude, in meters."
)
def cover_photo(x: float, deform: float):
    contour_.cover_photo(c=c(), x=x, deformation_amp=deform)


@contour.command(help="Response to traffic at multiple timesteps, per scenario.")
def scenarios_traffic():
    contour_.traffic_response_plots(c())


@contour.command(help="Response to point loads per scenario.")
def scenarios_point_load():
    contour_.point_load_response_plots(c())


@contour.command(help="Response to each pier being displaced in turn.")
def each_pier_displaced():
    contour_.each_pier_displacement_plots(c())


@contour.command(help="Response to unit axial thermal deck load.")
def thermal_deck_axial():
    from make.plot.contour.thermal import unit_axial_thermal_deck_load
    unit_axial_thermal_deck_load(c())


@contour.command(help="Response to unit moment thermal deck load.")
def thermal_deck_moment():
    from make.plot.contour.thermal import unit_moment_thermal_deck_load
    unit_moment_thermal_deck_load(c())


@contour.command(help="Response to unit axial and moment thermal deck load.")
def thermal_deck():
    from make.plot.contour.thermal import unit_thermal_deck_load
    unit_thermal_deck_load(c())


########################
##### Distribution #####
########################


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
def pairwise_sensors():
    classification_.pairwise_sensors(c())


if __name__ == "__main__":
    cli()
