from copy import deepcopy

import numpy as np

from classify.data.responses import responses_to_loads_m, responses_to_vehicles_d
from classify.vehicle import wagen1
from config import Config
from fem.build import BuildContext
from fem.params import ExptParams, SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from fem.run.opensees.build.d3 import build_model_3d
from model.bridge import Point
from model.load import PointLoad
from model.response import ResponseType
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck
from util import flatten, safe_str


def mesh_refinement(c: Config, build: bool, plot: bool):
    """Generate TCL files for debugging mesh refinement."""
    response_type = ResponseType.YTranslation
    min_config = deepcopy(c)
    min_config.bridge.type = "debugging"
    # min_config.bridge.base_mesh_deck_max_x = 100
    # min_config.bridge.base_mesh_deck_max_z = 100
    # min_config.bridge.base_mesh_pier_max_long = 10
    pload = PointLoad(x_frac=0.5, z_frac=0.5, kn=100)

    def build_with_refinement(refinement_radii):
        sim_params = SimParams(
            response_types=[response_type],
            ploads=[pload],
            refinement_radii=refinement_radii,
        )
        # Build and save the model file.
        if build:
            build_model_3d(
                c=min_config,
                expt_params=ExptParams([sim_params]),
                os_runner=OSRunner(min_config),
            )
        # Load and plot responses.
        if plot:
            sim_responses = load_fem_responses(
                c=min_config,
                sim_runner=OSRunner(min_config),
                response_type=response_type,
                sim_params=sim_params,
                run=True,
            )
            for scatter in [True, False]:
                top_view_bridge(
                    min_config.bridge, abutments=True, piers=True, lanes=True
                )
                plot_contour_deck(
                    c=min_config, responses=sim_responses, scatter=scatter, levels=100,
                )
                plt.title(f"{refinement_radii}")
                plt.savefig(
                    min_config.get_image_path(
                        "debugging",
                        safe_str(
                            f"{response_type.name()}-{refinement_radii}-scatter-{scatter}"
                        )
                        + ".pdf",
                    )
                )
                plt.close()

    build_with_refinement([])
    build_with_refinement([10])


def compare_responses(c: Config):
    """Compare responses to Truck 1, direct simulation and matmul."""
    assert c.il_num_loads == 400
    num_times = 100
    # Running time:
    # responses_to_vehicles_d: num_times * 8
    # responses_to_vehicles_d: 4 * il_num_loads
    # responses_to_loads_m: 0 (4 * il_num_loads)
    # responses_to_loads_m: 0 (4 * il_num_loads)

    point = Point(x=c.bridge.x_max / 2, y=0, z=0)
    end_time = wagen1.left_bridge(bridge=c.bridge)
    wagen1_times = np.linspace(0, end_time, num_times)
    plt.portrait()

    # Start with responses from direct simulation.
    responses_not_binned = responses_to_vehicles_d(
        c=c,
        response_type=ResponseType.YTranslation,
        points=[point],
        mv_vehicles=[wagen1],
        times=wagen1_times,
        sim_runner=OSRunner(c),
        binned=False,
    )
    plt.subplot(4, 1, 1)
    plt.title(f"{num_times} responses")
    plt.plot(responses_not_binned)

    # # Then responses from direct simulation with binning.
    c.shorten_paths = True
    responses_binned = responses_to_vehicles_d(
        c=c,
        response_type=ResponseType.YTranslation,
        points=[point],
        mv_vehicles=[wagen1],
        times=wagen1_times,
        sim_runner=OSRunner(c),
        binned=True,
    )
    c.shorten_paths = False
    plt.subplot(4, 1, 2)
    plt.title(f"{num_times} responses (binned)")
    plt.plot(responses_binned)

    # plt.subplot(4, 1, 3)
    # plt.plot(np.array(responses_not_binned) - np.array(responses_binned))
    # plt.title("Difference between first and second plots")

    num_times = int(end_time / c.sensor_hz)
    wagen1_times = np.linspace(0, end_time, num_times)

    # Then from 'TrafficArray' we get responses, without binning.
    responses_ulm = [
        responses_to_loads_m(
            c=c,
            response_type=ResponseType.YTranslation,
            points=[point],
            sim_runner=OSRunner(c),
            loads=flatten(
                wagen1.to_point_load_pw(time=time, bridge=c.bridge), PointLoad
            ),
        )
        for time in wagen1_times
    ]
    plt.subplot(4, 1, 3)
    plt.title(f"{num_times} responses with ULS = {c.il_num_loads} traffic_array")
    plt.plot(np.array(responses_ulm).reshape(-1, 1))

    # # Then from 'TrafficArray' we get responses, with binning.
    responses = [
        responses_to_loads_m(
            c=c,
            response_type=ResponseType.YTranslation,
            points=[point],
            sim_runner=OSRunner(c),
            loads=flatten(wagen1.to_point_loads_binned(c=c, time=time), PointLoad),
        )
        for time in wagen1_times
    ]
    plt.subplot(4, 1, 4)
    plt.title(
        f"{num_times} responses from {c.il_num_loads} il_num_loads\ntraffic_array binned"
    )
    plt.plot(np.array(responses).reshape(-1, 1))

    plt.tight_layout()
    plt.savefig(c.get_image_path("system-verification", "compare-time-series.pdf"))
