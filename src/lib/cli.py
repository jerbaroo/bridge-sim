"""Command line interface to bridge-sim."""
import os
import pdb
import pathos.multiprocessing as multiprocessing
import sys
import traceback
from typing import List

import click

from classify.vehicle import wagen1, wagen1_x_pos
from make import paramselect
from make.data import simulations
from make.plot import classification as classification_
from make.plot import contour as contour_
from make.plot import geometry as geometry_
from make.plot import vehicle, verification
from model.response import ResponseType
from model.bridge.bridge_705 import (
    bridge_705_2d,
    bridge_705_3d,
    bridge_705_config,
    bridge_705_low_config,
    bridge_705_med_config,
    bridge_705_single_sections,
)
from util import clean_generated, print_i, remove_except_npy

pdb_ = "--pdb" in sys.argv
b_func = None
c_func = None
two_materials_ = None
parallel_ = None
parallel_ulm_ = None
save_to_ = None
shorten_paths_ = None
il_num_loads_ = None


def bridge_705_3d_overload(*args, **kwargs):
    new_c = bridge_705_3d(
        *args,
        **kwargs,
        single_sections=(bridge_705_single_sections() if two_materials_ else None),
    )
    return new_c


def c():
    new_c = c_func(b_func)
    new_c.parallel = parallel_
    new_c.parallel_ulm = parallel_ulm_
    new_c.shorten_paths = shorten_paths_
    new_c.il_num_loads = il_num_loads_
    new_c.root_generated_data_dir = os.path.join(
        save_to_, new_c.root_generated_data_dir
    )
    return new_c


@click.group()
@click.option(
    "--dimensions",
    type=click.Choice(["2", "3"]),
    default="3",
    help="2D or 3D bridge. (DEPRECATED)",
)
@click.option(
    "--uls", type=int, default=600, help="Unit load simulations per wheel track",
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
    "--shorten-paths",
    type=bool,
    default=False,
    help="Save responses at shorter filepaths.",
)
@click.option(
    "--pdb", is_flag=True, help="Jump into the debugger on exception.",
)
def cli(
    dimensions: str,
    uls: int,
    mesh: str,
    two_materials: bool,
    parallel: int,
    parallel_ulm: bool,
    save_to: bool,
    shorten_paths: bool,
    pdb: bool,
):
    if dimensions == 2 and two_materials:
        raise ValueError("--two-materials option only valid for a 3D bridge")
    global c_func
    global b_func
    global two_materials_
    global save_to_
    global parallel_
    global parallel_ulm_
    global shorten_paths_
    global il_num_loads_
    two_materials_ = two_materials
    save_to_ = save_to
    parallel_ = parallel
    parallel_ulm_ = parallel_ulm
    shorten_paths_ = shorten_paths
    il_num_loads_ = uls

    click.echo(f"Dimensions: {dimensions}")
    click.echo(f"Mesh density: {mesh}")
    click.echo(f"Two materials: {two_materials_}")
    click.echo(f"Save to: {save_to_}")
    click.echo(f"Parallel: {parallel_}")
    click.echo(f"Parallel wheel tracks: {parallel_ulm_}")
    click.echo(f"Shorten paths: {shorten_paths_}")
    click.echo(f"ULS: {il_num_loads_}")

    if mesh == "low":
        c_func = bridge_705_low_config
    elif mesh == "med":
        c_func = bridge_705_med_config
    elif mesh == "full":
        c_func = bridge_705_config
    else:
        raise ValueError(f"Unknown mesh {mesh}")

    if dimensions == "3":
        b_func = bridge_705_3d_overload
    elif dimensions == "2":
        b_func = bridge_705_2d
    else:
        raise ValueError(f"Unknown dimensions {dimensions}")


################
##### Util #####
################


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
    from classify.scenario.bridge import transverse_crack

    remove_except_npy(c=c(), keep=keep)
    c_ = transverse_crack().use(c())[0]
    remove_except_npy(c=c_, keep=keep)


################
##### Info #####
################


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


@info.command(help="Make and plot the vehicle database.")
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


######################
##### Simulation #####
######################


@cli.group(help="Run simulations and generate data.")
def simulate():
    pass


@simulate.command(help="Run unit load simulations.")
@click.option("--piers", is_flag=True, help="Run pier settlement simulations.")
@click.option("--healthy", is_flag=True, help="Run unit load simulations (healthy).")
@click.option("--cracked", is_flag=True, help="Run unit load simulations (cracked).")
@click.option("--crack-x", type=float, help="Set crack zone at this X position.")
@click.option(
    "--crack-length", type=float, help="Set length of crack zone in X direction."
)
def uls(piers, healthy, cracked, crack_x, crack_length):
    simulations.run_uls(
        c=c(),
        piers=piers,
        healthy=healthy,
        cracked=cracked,
        crack_x=crack_x,
        crack_length=crack_length,
    )


@simulate.command(help="Generate unit load matrices")
@click.option("--healthy", is_flag=True, help="Run unit load simulations (healthy).")
@click.option("--cracked", is_flag=True, help="Run unit load simulations (cracked).")
@click.option(
    "--x-i", type=int, default=302, help="Index into wheel track (lowest x is 0)."
)
@click.option(
    "--z-i", type=int, default=0, help="Index of wheel track (lowest z is 0)."
)
def ulm(healthy, cracked, x_i, z_i):
    simulations.run_ulm(c=c(), healthy=healthy, cracked=cracked, x_i=x_i, z_i=z_i)


@simulate.command(help="Record information for convergence plots.")
def converge():
    verification.make_convergence_data(c())


####################
##### Validate #####
####################


@cli.group(help="Validate the generated FEM of bridge 705.")
def validate():
    pass


@validate.command(help="Plots of temperature against sensor responses.")
def temp_sensors():
    verification.temp_plots()


@validate.command(help="Contour plots comparing OpenSees and Diana.")
@click.option("--run-only", is_flag=True, help="Only run simulations, don't plot.")
@click.option("--scatter", is_flag=True, help="Scatter instead of contour plot.")
def diana_comp(run_only: float, scatter: bool):
    contour_.comparison_plots_705(c=c(), run_only=run_only, scatter=scatter)


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


@validate.command(help="Contour plots of unit thermal deck loading.")
@click.option("--run", is_flag=True, help="Run the simulations before plotting.")
def thermal(run):
    from make.plot.contour import thermal

    if not two_materials_:
        raise ValueError("You need the --two-materials option!")
    thermal.unit_moment_thermal_deck_load(c=c(), run=run)
    thermal.unit_axial_thermal_deck_load(c=c(), run=run)


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


@validate.command(help="Time series of 3 sensors to Truck 1's movement.")
def truck_1_ts():
    from make import validate

    validate.truck_1_time_series(c())


@validate.command(help="Plot stress for some high stress scenarios.")
@click.option("--top", is_flag=True, help="Top or bottom stress.")
def stress_strength(top):
    from make import validate

    validate.stress_strength_plot(c=c(), top=top)


#################
##### Param #####
#################


@cli.group(help="Information for parameter selection.")
def params():
    pass


@params.command(help="Plot to select the amount of ULS.")
def param_uls():
    paramselect.number_of_uls_plot(c())


@params.command(help="Plot noise from dynamic test 1.")
def noise():
    paramselect.experiment_noise(c())


###################
##### Contour #####
###################


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


@contour.command(help="Response to a 100 kN point load per scenario.")
@click.option("--x", type=float, default=51.375, help="X position of the point load.")
@click.option("--z", type=float, default=0, help="Z position of the point load.")
@click.option("--run", is_flag=True, help="Force simulations to run.")
def point_load(x, z, run):
    contour_.point_load_response_plots(c=c(), x=x, z=z, run=run)


@contour.command(help="Unit thermal deck load under normal traffic.")
@click.option("--axial", type=float, required=True)
@click.option("--moment", type=float, required=True)
def traffic_thermal(axial, moment):
    from make.plot.contour.traffic_thermal import thermal_deck_load

    thermal_deck_load(c(), axial_delta_temp=axial, moment_delta_temp=moment)


##################
##### Verify #####
##################


@cli.group(help="Verify/debug this system.")
def verify():
    pass


@verify.command(help="TCL files & contour plots for mesh refinement.")
@click.option("--build", type=bool, default=True)
@click.option("--plot", type=bool, default=True)
def refinement_tcls(build: bool, plot: bool):
    from make import verify

    verify.mesh_refinement(c=c(), build=build, plot=plot)


@verify.command(help="Compare responses by direct simulation and matmul.")
def comp_responses():
    from make import verify

    verify.compare_responses(c())


@verify.command(help="Compare vehicles with different amount of axles.")
def comp_axles():
    from make import verify

    verify.compare_axles(c())


@verify.command(help="Compare load positions (normal vs. buckets).")
def comp_load_positions():
    from make.verify import compare_load_positions

    compare_load_positions(c())


@verify.command(help="Contour plot of a unit load simulation.")
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


@verify.command(help="Contour plot of truck 1, healthy & cracked.")
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
@click.option("--wheels", is_flag=True, help="Plot position of vehicle's wheel.")
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


@verify.command(help="Plot a time series where a crack occurs.")
def cracked_concrete():
    from make.verify import cracked_concrete_plot

    cracked_concrete_plot(c())


####################
##### Classify #####
####################


@cli.group(help="Run classification experiments.")
def classify():
    pass


@classify.command(help="Time series of responses with crack occuring.")
@click.option(
    "--n", type=float, default=1, help="Meters sensor is in front of crack zone."
)
def crack_ts(n: float):
    from classify.crack import time_series_plot

    time_series_plot(c(), n=1)


@classify.command(help="Responses to traffic with a top view.")
@click.option("--mins", type=float, default=1, help="Minutes of traffic.")
@click.option("--skip", type=int, default=50, help="Skip every n recorded responses.")
@click.option(
    "--damage",
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


@classify.command(help="")
@click.option("--mins", type=float, default=1, help="Minutes of traffic.")
def cluster(mins):
    from make.classify.cluster import cluster_damage

    cluster_damage(c=c(), mins=mins)


@classify.command(help="Plot events due to normal traffic.")
@click.option("--x", type=float, default=51.375)
@click.option("--z", type=float, default=-8.4)
def events(x, z):
    classification_.events(c=c(), x=x, z=z)


@classify.command(help="Plot temperature effect.")
@click.option(
    "--date", type=str, default="holly-springs", help="Filename to plot effect for."
)
@click.option("--vert", type=bool, default=True, help="Vertical lines every 24 hours.")
def temp_effect_date(date, vert):
    classification_.temperature_effect_date(c=c(), month=date, vert=vert)


@classify.command(help="Contour plot of temperature effect.")
@click.option(
    "--bottom", type=float, required=True, help="Bottom temperature in celcius."
)
@click.option("--top", type=float, required=True, help="Top temperature in celcius.")
def temp_contour(bottom, top):
    from make.classify.temp import temp_contour_plot

    temp_contour_plot(c=c(), temp_bottom=bottom, temp_top=top)


@classify.command(help="Plot bridge deck temperature gradient.")
@click.option(
    "--date",
    type=str,
    default="holly-springs",
    help="Filename of year temperature data.",
)
def temp_gradient(date):
    from make.classify.temp import temp_gradient_plot

    temp_gradient_plot(c=c(), date=date)


@classify.command(help="Plot removal of temperature effect.")
@click.option("--name", type=str, default="may", help="Filename to plot effect for.")
def temp_rm(name):
    classification_.temperature_removal_month(c=c(), month=name)


@classify.command()
def oneclass():
    classification_.oneclass(c())


@classify.command()
@click.option(
    "--load", type=bool, default=False, help="Load calculated features from disk."
)
def pairwise_cluster_2(load):
    classification_.pairwise_cluster(c=c(), load=load)


@classify.command()
def pairwise_sensors():
    classification_.pairwise_sensors(c())


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
