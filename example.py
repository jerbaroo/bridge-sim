# Example 1.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot

# config = configs.opensees_default(bridges.narrow_bridge)
# point_loads = [model.PointLoad(x=5, z=0, load=100)]
# responses = fem.responses(config, model.RT.YTrans, point_loads)
# plot.contour_responses(config, responses, point_loads)
# plot.top_view_bridge(config, piers=True)
# plt.tight_layout()
# plt.show()

# Example 2.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot, vehicles

# config = configs.opensees_default(bridges.narrow_bridge, shorten_paths=True)
# point_loads = vehicles.wagen1.to_point_load_pw(time=3.5, bridge=config.bridge, list=True)
# responses = fem.responses(config, model.RT.YTrans, point_loads)
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
#     model.RT.YTrans,
#     pier_settlement=model.PierSettlement(0, 1.2)
# )
# plot.contour_responses(config, responses)
# plot.top_view_bridge(config, piers=True, lanes=True)
# plt.tight_layout()
# plt.show()

# Example 4.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot
#
# config = configs.opensees_default(bridges.bridge_wide)
# plt.figure(figsize=(16, 10))
# for subplot, response_type in enumerate([
#         model.RT.YTrans, model.RT.ZTrans,
#         model.RT.StrainXXB, model.RT.StrainZZB,
#     ]):
#     responses = fem.responses(
#         config,
#         response_type,
#         pier_settlement=model.PierSettlement(0, 1)
#     ).resize()
#     plt.subplot(2, 2, subplot + 1)
#     plot.contour_responses(config, responses)
#     plot.top_view_bridge(config, piers=True, lanes=True)
#     plt.title(response_type.name())
#
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
# point_loads = [model.PointLoad(x=18, z=0, load=100)]
# responses = fem.responses(config, model.RT.YTrans, point_loads)
# plot.contour_responses(config, responses, point_loads)
# plot.top_view_bridge(config, piers=True)
# plt.tight_layout()
# plt.show()

# Example 6.

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, fem, model, plot
from bridge_sim.model import Vehicle

new_vehicle = Vehicle(
    # Load intensity of each axle.
    kn=[5000, 4000, 4000, 5000, 7000],
    # Distance between each pair of axles.
    axle_distances=[2, 2, 2, 1],
    # Width of each axle, distance between point loads.
    axle_width=2.5,
    # Speed of the vehicles.
    kmph=20,
)

config = configs.opensees_default(bridges.bridge_narrow, shorten_paths=True)
point_loads = new_vehicle.to_point_load_pw(time=3.5, bridge=config.bridge, list=True)
responses = fem.responses(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config, piers=True)
plt.tight_layout()
plt.show()
