"""Command line interface to bridge-sim."""
import click

from config import Config
from make.data import simulations
from make.plot import contour
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
        single_sections=(
            bridge_705_single_sections if two_materials_ else None
        ),
    )



@click.group()
@click.option("--dimensions", type=click.Choice(["2", "3"]), default="3", help="2D or 3D bridge.")
@click.option("--mesh", type=click.Choice(["debug", "low", "full"]), default="debug", help="Mesh density of the bridge.")
@click.option("--two-materials", is_flag=True, help="One material for the deck and one for the piers.")
@click.option("--parallel", is_flag=True, default=True, help="Run simulations in parallel.")
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
        c = c_func(bridge_705_3d_overload)
    elif dimensions == "2":
        c = c_func(bridge_705_2d)


#######################
##### Util & Info #####
#######################


@cli.command()
def clean():
    clean_generated(c)


@cli.command()
@click.option("--piers", is_flag=True)
def bridge_info(piers):
    c.bridge.print_info(pier_fix_info=piers)


######################
##### Simulation #####
######################


@cli.group()
def simulation():
    pass


@simulation.command()
def unit_load_simulations():
    simulations.run_uls(c)


@simulation.command()
def convergence_data():
    verification.make_convergence_data(c, run=True, plot=False)


########################
##### Verification #####
########################


@cli.group()
def verification():
    pass


@verification.command()
def comparison_plots_705():
    contour.comparison_plots_705(c)


####################
##### Scenario #####
####################


@cli.group()
def scenario():
    pass


@scenario.command()
def contour_pier_displacement():
    contour.plots_of_pier_displacement(c)


if __name__ == "__main__":
    cli()
