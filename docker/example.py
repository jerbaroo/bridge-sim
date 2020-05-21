import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, fem, model, plot, vehicle
from bridge_sim.vehicle import Vehicle

new_vehicle = Vehicle(
    # Load intensity of each axle.
    kn=[5000, 4000, 4000, 5000, 7000],
    # Distance between each pair of axles.
    axle_distances=[2, 2, 2, 1],
    # Width of each axle, distance between point loads.
    axle_width=2.5,
    # Speed of the vehicle.
    kmph=20,
    # Index of a traffic lane on the bridge.
    lane=0,
    # Fraction of the position on the lane at time = 0.
    init_x_frac=0,
)

config = configs.opensees_default(
    bridges.bridge_example, "/root/bin/OpenSees", shorten_paths=True)
point_loads = new_vehicle.to_point_load_pw(time=3.5, bridge=config.bridge, list=True)
responses = fem.responses(config, model.RT.YTranslation, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config, piers=True)
plt.tight_layout()
plt.savefig("docker.png")
