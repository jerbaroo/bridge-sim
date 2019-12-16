"""Command line interface to bridge-sim."""
import click

from config import Config
from make.data import simulations
from make.plot import contour, vehicle, verification
from make.plot import classification as classification_
from make.plot import geometry as geometry_
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
    help="One material for the deck and one for the piers.",
)
@click.option(
    "--parallel", is_flag=True, default=True, help="Run simulations in parallel.",
)
def cli(dimensions, mesh, two_materials, parallel):
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
    if dimensions == "3":
        c = lambda: c_func(bridge_705_3d_overload)
    elif dimensions == "2":
        c = lambda: c_func(bridge_705_2d)


################
##### Util #####
################


@cli.command()
def clean():
    clean_generated(c())


################
##### Util #####
################
################


@cli.group()
def info():
    pass


@info.command(help="Print a summary of this bridge.")
@click.option("--piers", is_flag=True)
def bridge_info(piers):
    c.bridge.print_info(pier_fix_info=piers)


@info.command(help="Z positions of the wheel tracks.")
def wheel_tracks():
    config = c()
    print_i(f"Wheel tracks: {config.bridge.wheel_tracks(config)}")


@info.command(help="Plot of specification of Truck 1.")
def wagen_1():
    vehicle.wagen1_plot(c())


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


@cli.group()
def simulation():
    pass


@simulation.command()
def unit_load_simulations():
    simulations.run_uls(c())


@simulation.command()
def convergence_data(help="Record simulation as model size is increased."):
    verification.make_convergence_data(c())


########################
##### Verification #####
########################


@cli.group()
def validate():
    pass


@validate.command(help="Contour plots comparing OpenSees and Diana.")
def diana_comp():
    contour.comparison_plots_705(c())


@validate.command(help="Regression plots against bridge 705 measurements.")
def r2():
    verification.r2_plots(c())


@validate.command(help="Plot of model convergence as model size increases.")
def convergence():
    verification.plot_convergence(c())


####################
##### Scenario #####
####################


@cli.group(help="Plots for damage scenarios.")
def scenario():
    pass


@scenario.command(help="Mean response to traffic per scenario.")
def contour_traffic():
    contour.mean_traffic_response_plots(c())


@scenario.command(help="Response to point loads per scenario.")
def contour_point_load():
    contour.point_load_response_plots(c())


@scenario.command()
def contour_cracked_concrete():
    contour.cracked_concrete_plots(c())


@scenario.command()
def contour_each_pier_displaced():
    contour.each_pier_displacement_plots(c())


########################
##### Distribution #####
########################


##########################
##### Classification #####
##########################


@cli.group()
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
