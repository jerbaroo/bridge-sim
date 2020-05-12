from config import Config


def plot_pier_displacement(c: Config):
    """Comparison of two calculations of pier displacement.

    One calculation is directly from a pier displacement simulation, while the
    second is from 'responses_to_traffic_array' where the 'TrafficArray' is set
    to 0.

    """
    pier_index = 5
    pier = c.bridge.supports[pier_index]
    response_type = ResponseType.YTranslation
    pier_displacement = DisplacementCtrl(displacement=c.pd_unit_disp, pier=pier_index)

    # Plot responses captured directly from a pier displacement simualtion.
    sim_params = SimParams(
        response_types=[response_type], displacement_ctrl=pier_displacement,
    )
    sim_responses = load_fem_responses(
        c=c, sim_params=sim_params, response_type=response_type, sim_runner=OSRunner(c),
    )
    plt.subplot(2, 1, 1)
    top_view_bridge(c.bridge, lanes=False, outline=False)
    _, _, norm = plot_contour_deck(
        c=c,
        responses=sim_responses,
        ploads=[
            PointLoad(
                x_frac=c.bridge.x_frac(pier.x),
                z_frac=c.bridge.z_frac(pier.z),
                kn=c.pd_unit_load_kn,
            )
        ],
    )
    plt.colorbar(norm=norm)

    points = [
        Point(x=x, y=0, z=z)
        for x, z in itertools.product(
            np.linspace(c.bridge.x_min, c.bridge.x_max, 10),
            np.linspace(c.bridge.z_min, c.bridge.z_max, 10),
        )
    ]
    bridge_scenario = PierDispBridge(pier_displacement)
    wheel_zs = c.bridge.wheel_tracks(c)
    response_array = responses_to_traffic_array(
        c=c,
        traffic_array=np.zeros((10, len(wheel_zs) * c.il_num_loads)),
        response_type=response_type,
        bridge_scenario=bridge_scenario,
        points=points,
        fem_runner=OSRunner(c),
    )
    plt.subplot(2, 1, 2)
    top_view_bridge(c.bridge, lanes=False, outline=False)
    responses = Responses.from_responses(
        response_type=response_type,
        responses=[(response_array[0][p], point) for p, point in enumerate(points)],
    )
    _, _, norm = plot_contour_deck(
        c=c,
        responses=responses,
        ploads=[
            PointLoad(
                x_frac=c.bridge.x_frac(pier.x),
                z_frac=c.bridge.z_frac(pier.z),
                kn=c.pd_unit_load_kn,
            )
        ],
    )
    plt.colorbar(norm=norm)

    plt.savefig(c.get_image_path("system-verification", "pier-displacement"))
