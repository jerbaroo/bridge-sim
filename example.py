# Example 1.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot

# config = configs.opensees_default(bridges.bridge_example)
# point_loads = [model.PointLoad(config, x=5, z=0, load=100)]
# responses = fem.responses(config, model.RT.YTranslation, point_loads)
# plot.contour_responses(config, responses, point_loads)
# plot.top_view_bridge(config, piers=True)
# plt.tight_layout()
# plt.show()

# Example 2.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot, vehicle

# config = configs.opensees_default(bridges.bridge_example, shorten_paths=True)
# point_loads = vehicle.wagen1.to_point_load_pw(time=3.5, bridge=config.bridge, list=True)
# responses = fem.responses(config, model.RT.YTranslation, point_loads)
# plot.contour_responses(config, responses, point_loads)
# plot.top_view_bridge(config, piers=True)
# plt.tight_layout()
# plt.show()

# Example 3.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot

# config = configs.opensees_default(bridges.bridge_wide)
# responses = fem.responses(
#     config,
#     model.RT.YTranslation,
#     pier_settle=model.PierSettlement(0, 1)
# )
# plot.contour_responses(config, responses)
# plot.top_view_bridge(config, piers=True, lanes=True)
# plt.tight_layout()
# plt.show()

# Example 4.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot

# config = configs.opensees_default(bridges.bridge_wide)
# plt.figure(figsize=(16, 10))  # Increase plot size.
# for response_type, subplot in [
#         (model.RT.YTranslation, 1),
#         (model.RT.ZTranslation, 2),
#         (model.RT.Strain, 3),  # Will be renamed to StrainXXB.
#         (model.RT.StrainZZB, 4),
#     ]:
#     responses = fem.responses(
#         config,
#         response_type,
#         pier_settle=model.PierSettlement(0, 1)
#     ).resize()  # Make units more readable, m -> mm, strain to microstrain.
#     plt.subplot(2, 2, subplot)
#     plot.contour_responses(config, responses)
#     plot.top_view_bridge(config, piers=True, lanes=True)

# plt.tight_layout()
# plt.show()

# Example 5.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot
# from bridge_sim.bridges import Bridge, Lane, MaterialDeck, MaterialSupport, Support


# def new_bridge():
#     return Bridge(
#         name="example",   # Name used to identify saved/loaded data.
#         length=40,  # Length of this bridge.
#         width=3,  # Width of this bridge.
#         supports=[
#             Support(
#                 x=20,  # X position of center of the support.
#                 z=0,  # Z position of center of the support.
#                 length=2,  # Length between support columns (X direction).
#                 height=2,  # Height from top to bottom of support.
#                 width_top=2,  # Width of support column at top (Z direction).
#                 width_bottom=1,  # Width of support column at bottom (Z direction).
#                 materials=[  # List of materials for the support columns.
#                     MaterialSupport(
#                         density=0.7,
#                         thickness=0.7,
#                         youngs=40000,
#                         poissons=0.2,
#                         start_frac_len=0,
#                     )
#                 ],
#                 fix_z_translation=True,
#                 fix_x_translation=True,
#             )
#         ],
#         # List of materials for the bridge deck.
#         materials=[MaterialDeck(thickness=0.7, youngs=40000, poissons=0.2,)],
#         # List of lanes where traffic can drive on the bridge.
#         lanes=[Lane(-1, 1, True)],
#     )

# config = configs.opensees_default(new_bridge)
# point_loads = [model.PointLoad(config, x=18, z=0, load=100)]
# responses = fem.responses(config, model.RT.YTranslation, point_loads)
# plot.contour_responses(config, responses, point_loads)
# plot.top_view_bridge(config, piers=True)
# plt.tight_layout()
# plt.show()

# Example 6.

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

config = configs.opensees_default(bridges.bridge_example, shorten_paths=True)
point_loads = new_vehicle.to_point_load_pw(time=3.5, bridge=config.bridge, list=True)
responses = fem.responses(config, model.RT.YTranslation, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config, piers=True)
plt.tight_layout()
plt.show()
