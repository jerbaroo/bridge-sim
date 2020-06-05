"""Command line interface to bridge-sim.

Run './scripts/cli.sh' from the root directory of the cloned 'bridge_sim' repository.

"""

import os
import pdb

import lib.make.temperature
import lib.make.validation
import pathos.multiprocessing as multiprocessing
import sys
import traceback

import click

from bridge_sim.configs import opensees_default
from bridge_sim.model import ResponseType
from bridge_sim.vehicles import truck1
from lib.validate import _truck1_x_pos
from lib.make import paramselect
from lib.make.plot import contour as contour_
from lib.make.plot import geometry as geometry_
from lib.make.plot import vehicle, verification
from bridge_sim.bridges.bridge_705 import bridge_705
from bridge_sim.util import clean_generated, print_i, remove_except_npy

# Storing CLI parameters here as global variables.
pdb_ = "--pdb" in sys.argv
b_func = None
c_func = opensees_default
two_materials_ = None
parallel_ = None
parallel_ulm_ = None
save_to_ = None
shorten_paths_ = None
il_num_loads_ = None


def c():
    """Construct a 'Config' based on CLI parameters."""
    new_c = c_func(b_func)
    new_c.parallel = parallel_
    new_c.parallel_ulm = parallel_ulm_
    new_c.shorten_paths = shorten_paths_
    new_c.il_num_loads = il_num_loads_
    old_c_root_generated_data_dir = new_c._root_generated_data_dir
    new_c.root_generated_data_dir = lambda: os.path.join(
        save_to_, old_c_root_generated_data_dir
    )
    return new_c


@click.group()
@click.option(
    "--uls", type=int, default=600, help="Unit load simulations per wheel track",
)
@click.option(
    "--msl", type=float, default=0.5, help="Maximum shell length of the bridge.",
)
@click.option(
    "--two-materials",
    is_flag=True,
    help="One material for the deck and one for piers.",
)
@click.option(
    "--parallel", type=int, default=1, help="Run experiment simulations in parallel",
)
@click.option(
    "--parallel-ulm",
    type=bool,
    default=True,
    help=f"One process per wheel track (max {multiprocessing.cpu_count()} processes).",
)
@click.option(
    "--save-to", type=str, default="", help="Save/load data from a given folder.",
)
@click.option(
    "--shorten-paths", is_flag=True, help="Save responses at shorter filepaths.",
)
@click.option(
    "--pdb", is_flag=True, help="Jump into the debugger on exception.",
)
def cli(
    uls: int,
    msl: str,
    two_materials: bool,
    parallel: int,
    parallel_ulm: bool,
    save_to: bool,
    shorten_paths: bool,
    pdb: bool,
):
    global b_func
    global two_materials_
    global save_to_
    global parallel_
    global parallel_ulm_
    global shorten_paths_
    global il_num_loads_
    b_func = bridge_705(msl)
    two_materials_ = two_materials
    save_to_ = save_to
    parallel_ = parallel
    parallel_ulm_ = parallel_ulm
    shorten_paths_ = shorten_paths
    il_num_loads_ = uls

    click.echo(f"Bridge: {b_func().name}")
    click.echo(f"ULS: {il_num_loads_}")
    click.echo(f"MSL: {msl}")
    click.echo(f"Two materials: {two_materials_}")
    click.echo(f"Parallel: {parallel_}")
    click.echo(f"Parallel wheel tracks: {parallel_ulm_}")
    click.echo(f"Save to: {save_to_}")
    click.echo(f"Shorten paths: {shorten_paths_}")


########
# Util #
########


@cli.command(help="Remove all simulation data for a bridge.")
def remove():
    clean_generated(c())


@cli.command(help="Remove simulation data except for result files.")
@click.option(
    "--keep",
    type=str,
    default="y-translation strain",
    help="Words required in the filename.",
)
def clean(keep):
    from bridge_sim.scenarios import transverse_crack

    remove_except_npy(c=c(), keep=keep)
    c_ = transverse_crack().use(c())[0]
    remove_except_npy(c=c_, keep=keep)


########
# Info #
########


@cli.group(help="Print and plot useful information.")
def info():
    pass


@info.command(help="Print information about this bridge.")
@click.option("--piers", is_flag=True)
def bridge(piers):
    c().bridge.print_info(c=c(), pier_fix_info=piers)


@info.command(help="Z positions of the wheel tracks, in meters.")
def wheel_tracks():
    config = c()
    print_i(f"Wheel tracks: {config.bridge.wheel_tracks(config)}")


@info.command(help="Print and plot information on Truck 1.")
def truck_1():
    vehicle.wagen1_plot(c())
    print_i(f"Truck 1 x positions: {_truck1_x_pos()}")


@info.command(help="Load position and intensity per wheel of Truck 1.")
@click.option(
    "--x",
    type=float,
    required=True,
    help="X position of front axle of Truck 1, in meters.",
)
def truck_1_loads(x: float):
    config = c()
    time = truck1.time_at(x=x, bridge=config.bridge)
    print_i(f"Time = {time:.4f}s")
    axle_loads = truck1.to_point_loads(time=time, bridge=config.bridge)
    for i in range(len(axle_loads)):
        print_i(
            f"Axle {i}: ({axle_loads[i][0].repr(config.bridge)}), "
            f" ({axle_loads[i][1].repr(config.bridge)})"
        )


@info.command(help="Make and plot the vehicles database.")
def vehicle_dist():
    from plot.vehicles import plot_dist

    plot_dist(c())


@info.command(help="Shells in 3D coloured by material properties.")
def shells_3d():
    geometry_.make_shell_properties_3d(c())


@info.command(help="Top view of shells coloured by material properties.")
@click.option("--shells", type=click.Choice(["deck", "pier"]), default="deck")
@click.option(
    "--prop",
    type=click.Choice(["mesh", "thickness", "density", "poisson", "young"]),
    required=True,
)
@click.option("--refined", is_flag=True)
@click.option("--outline", is_flag=True)
@click.option("--lanes", is_flag=True)
def shells_top(shells, prop, refined, outline, lanes):
    geometry_.make_shell_properties_top_view(
        c=c(),
        shells_name_=shells,
        prop_name_=prop,
        refined_=refined,
        outline=outline,
        lanes=lanes,
    )


@info.command(help="3D scatter plot of FEM nodes.")
def nodes():
    geometry_.make_node_plots(c())


@info.command(help="Plot of model geometry and boundary conditions.")
def boundary():
    geometry_.make_boundary_plot(c())


@info.command(help="Plot available sensors on the deck.")
@click.option(
    "--pier-radius",
    type=float,
    required=True,
    help="Radius around pier lines to ignore.",
)
@click.option(
    "--track-radius",
    type=float,
    required=True,
    help="Radius around wheel tracks to ignore.",
)
@click.option(
    "--edge-radius",
    type=float,
    required=True,
    help="Radius around bridge edges to ignore.",
)
def avail_sensors(pier_radius, track_radius, edge_radius):
    geometry_.make_available_sensors_plot(
        c=c(),
        pier_radius=pier_radius,
        track_radius=track_radius,
        edge_radius=edge_radius,
    )


##############
# Simulation #
##############


@cli.group(help="Run simulations, generate data.")
def run():
    pass


@run.command(help="Run unit load simulations.")
@click.option("--point", is_flag=True, help="Run point-load simulations.")
@click.option("--indices", type=str, help="Indices of point-load simulations.")
@click.option("--piers", is_flag=True, help="Run pier settlement simulations.")
@click.option("--temp", is_flag=True, help="Run temperature load simulations.")
def uls(point, indices, piers, temp):
    from bridge_sim import sim
    if indices is not None:
        indices = list(map(int, indices.split()))
    if point:
        list(sim.run.point_load(c(), indices, run_only=True))
    if piers:
        list(sim.run.pier_settlement(c(), run_only=True))
    if temp:
        list(sim.run.temperature(c(), run_only=True))


@run.command(help="Generate data for convergence plots.")
def convergence():
    verification.make_convergence_data(c())


##########
# Verify #
##########


@cli.group(help="Verify a number of loads.")
def verify():
    pass


@verify.command(help="Contour plots of point loads.")
@click.option("--scatter", is_flag=True, help="Scatter plot instead of contour plot.")
def point_loads(scatter: bool):
    if not two_materials_:
        raise ValueError("You need the --two-materials option!")
    lib.make.validation.unit_loads(c=c(), scatter=scatter)


@verify.command(help="Contour plots of pier settlement.")
def pier_settlement():
    if not two_materials_:
        raise ValueError("You need the --two-materials option!")
    lib.make.validation.pier_settlement(c())


@verify.command(help="Contour plots of temperature deck loading.")
def temp_loads():
    if not two_materials_:
        raise ValueError("You need the --two-materials option!")
    lib.make.validation.temperature_load(c())


@verify.command(help="Plots of time series of shrinkage.")
def shrinkage():
    from lib.make import shrinkage

    shrinkage.plot_autogenous_shrinkage(c())
    shrinkage.plot_drying_shrinkage(c())
    shrinkage.plot_total_shrinkage(c())


@verify.command(help="Plots of time series of creep.")
def creep():
    from lib.make import creep

    creep.plot_creep(c())


@verify.command(help="Plots of time series of temperature effect.")
def temp_effect():
    lib.make.temperature.temperature_effect(c(), "holly-springs")


@verify.command(help="Plot unit load simulations.")
def uls():
    from lib.make import uls
    uls.plot_uls(c())


############
# Validate #
############


@cli.group(help="Validate the generated FEM of bridge 705.")
def validate():
    pass


@validate.command(help="Regression plots against bridge 705 measurements.")
def r2():
    verification.r2_plots(c())


@validate.command(help="Plot convergence as model size increases.")
def convergence():
    verification.plot_convergence(c())


@validate.command(help="Plot NESW convergence around a point load.")
@click.option("--fp", type=str, help="Filepath of results file.")
@click.option("--at", type=str, help="Named point for plot title")
@click.option("--to", type=str, help="Filepath extension for saving plot.")
def convergence_nesw(fp, at, to):
    verification.plot_nesw_strain_convergence(
        c=c(), filepath=fp, from_=at, label=to,
    )


@validate.command(help="Plot strain convergence for pier settlement.")
@click.option("--pier", type=int, required=True, help="Index of the pier to settle.")
@click.option(
    "--max-nodes",
    type=int,
    required=True,
    help="Maximum number of nodes in a simulation.",
)
@click.option(
    "--without-radius",
    type=float,
    required=True,
    help="Radius around pier lines to ignore.",
)
@click.option(
    "--nesw-loc", type=int, required=True, help="Location of pier to plot NESW around."
)
@click.option(
    "--nesw-max-dist",
    type=float,
    required=True,
    help="Maximum distance to plot NESW around.",
)
@click.option("--process", type=int, default=0, help="Results identifier.")
@click.option(
    "--min-shell-len", type=float, default=0, help="Minimum shell len considered."
)
@click.option(
    "--max-shell-len", type=float, required=True, help="Maximum shell len considered."
)
def pier_conv(
    pier: int,
    max_nodes: int,
    without_radius: float,
    nesw_loc: int,
    nesw_max_dist: float,
    process: int,
    min_shell_len: float,
    max_shell_len: float,
):
    verification.plot_pier_convergence(
        c=c(),
        process=process,
        pier_i=pier,
        max_nodes=max_nodes,
        strain_ignore_radius=without_radius,
        nesw_location=nesw_loc,
        nesw_max_dist=nesw_max_dist,
        min_shell_len=min_shell_len,
        max_shell_len=max_shell_len,
    )


@validate.command(help="Influence lines from OpenSees and measurements.")
@click.option(
    "--strain-sensors",
    required=True,
    type=click.Choice(["O", "T"]),
    help="Prefix of strain sensors to plot.",
)
def inflines(strain_sensors):
    if not shorten_paths_:
        raise ValueError("--shorten-paths option is required")
    verification.per_sensor_plots(c=c(), strain_sensors_startwith=strain_sensors)


@validate.command(help="Confirm that density has no effect on simulation.")
def density():
    from make import validate

    validate.density_no_effect(c())


@validate.command(help="Time series of 3 sensors to Truck 1's movement.")
def truck_1_ts():
    from make import validate

    validate.truck_1_time_series(c())


@validate.command(help="Plot stress for some high stress scenarios.")
@click.option("--top", is_flag=True, help="Top or bottom stress.")
def stress_strength(top):
    from make import validate

    validate.stress_strength_plot(c=c(), top=top)


##########
# Thesis #
##########


@cli.group(help="Additional plots for my thesis.")
def thesis():
    pass


@thesis.command(help="3D contour plot of bridge 705.")
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


@thesis.command(help="ULS parameter selection plot.")
def uls():
    paramselect.number_of_uls_plot(c())


@thesis.command(help="Plot noise from dynamic test 1.")
def noise():
    paramselect.experiment_noise(c())


@thesis.command(help="Contour plot of temperature effect.")
@click.option(
    "--bottom", type=float, default=17, help="Bottom temperature in celcius."
)
@click.option("--top", type=float, default=23, help="Top temperature in celcius.")
def temp_contour(bottom, top):
    from lib.make.temperature import temp_contour_plot

    temp_contour_plot(c=c(), temp_bottom=bottom, temp_top=top)


@thesis.command(help="Plot bridge deck temperature profile.")
def temp_profile():
    from lib.make.temperature import temp_profile_plot

    temp_profile_plot(c=c(), fname="holly-springs")


#########
# Debug #
#########


@cli.group(help="Verify/debug this system.")
def debug():
    pass


@debug.command(help="TCL files & contour plots for mesh refinement.")
@click.option("--build", type=bool, default=True)
@click.option("--plot", type=bool, default=True)
def refinement_tcls(build: bool, plot: bool):
    from make import verify

    verify.mesh_refinement(c=c(), build=build, plot=plot)


@debug.command(help="Compare fem by direct simulation and matmul.")
def comp_responses():
    from make import verify

    verify.compare_responses(c())


@debug.command(help="Compare vehicles with different amount of axles.")
def comp_axles():
    from make import verify

    verify.compare_axles(c())


@debug.command(help="Compare load positions (normal vs. buckets).")
def comp_load_positions():
    from make.verify import compare_load_positions

    compare_load_positions(c())


@debug.command(help="Contour plot of a unit load simulation.")
@click.option(
    "--x-i", type=int, default=302, help="Index into wheel track (lowest x is 0)."
)
@click.option(
    "--z-i", type=int, default=0, help="Index of wheel track (lowest z is 0)."
)
@click.option("--rt", required=True, type=click.Choice(["strain", "ytrans"]))
def uls_contour(x_i: int, z_i: int, rt: str):
    from make.verify import uls_contour_plot

    if rt == "strain":
        response_type = ResponseType.Strain
    elif rt == "ytrans":
        response_type = ResponseType.YTranslation

    uls_contour_plot(c=c(), x_i=x_i, z_i=z_i, response_type=response_type)


@debug.command(help="Contour plot of truck 1, healthy & cracked.")
@click.option("--x", type=int, default=51.8, help="X position of Truck 1's front axle.")
@click.option(
    "--crack-x", type=float, default=52, help="X position of start of crack area."
)
@click.option(
    "--rt", required=True, type=click.Choice(["strain", "strain-z", "ytrans"])
)
@click.option("--scatter", is_flag=True, help="Scatter plot instead of contour plot.")
@click.option("--run", is_flag=True, help="Force the simulation to run again.")
@click.option("--length", type=float, default=0.5, help="Length of transverse crack.")
@click.option("--outline", is_flag=True, help="Plot an outline of the crack area.")
@click.option("--wheels", is_flag=True, help="Plot position of vehicles's wheel.")
@click.option("--temp", is_flag=True, help="Add temperature effect.")
def truck1_contour(
    x: int,
    crack_x: float,
    rt: str,
    scatter: bool,
    run: bool,
    length: float,
    outline: bool,
    wheels: bool,
    temp: bool,
):
    from make.verify import wagen_1_contour_plot

    if rt == "strain":
        response_type = ResponseType.Strain
    if rt == "strain-z":
        response_type = ResponseType.StrainZZB
    elif rt == "ytrans":
        response_type = ResponseType.YTranslation

    wagen_1_contour_plot(
        c=c(),
        x=x,
        crack_x=crack_x,
        response_type=response_type,
        scatter=scatter,
        run=run,
        length=length,
        outline=outline,
        wheels=wheels,
        temp=temp,
    )


@debug.command(help="Plot a time series where a crack occurs.")
def cracked_concrete():
    from make.verify import cracked_concrete_plot

    cracked_concrete_plot(c())


####################
##### Classify #####
####################


@cli.group(help="Run classification experiments.")
def classify():
    pass


@classify.command(help="Time series of fem with crack occuring.")
@click.option(
    "--n", type=float, default=1, help="Meters sensor is in front of crack zone."
)
def crack_ts(n: float):
    from classify.crack import time_series_plot

    time_series_plot(c(), n=1)


@classify.command(help="Responses to traffic with a top view.")
@click.option("--mins", type=float, default=1, help="Minutes of traffic.")
@click.option("--skip", type=int, default=50, help="Skip every n recorded fem.")
@click.option(
    "--scenarios",
    type=click.Choice(["healthy", "pier"]),
    default="healthy",
    help="Damage scenario.",
)
def top_view(mins, skip, damage):
    from classify.scenario.bridge import healthy_damage, pier_disp_damage
    from make.classify.top_view import top_view_plot

    if damage == "healthy":
        damage_scenario = healthy_damage
    elif damage == "pier":
        damage_scenario = pier_disp_damage([(5, 1 / 1000)])

    top_view_plot(
        c=c(), max_time=int(60 * mins), skip=skip, damage_scenario=damage_scenario
    )


@classify.command(help="Plot removal of temperature effect.")
@click.option("--name", type=str, default="may", help="Filename to plot effect for.")
def temp_rm(name):
    classification_.temperature_removal_month(c=c(), month=name)


if __name__ == "__main__":
    if pdb_:
        try:
            cli()
        except:
            extype, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
    else:
        cli()


__all__ = []
