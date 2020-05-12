# Example 1.

# import matplotlib.pyplot as plt
# from bridge_sim import bridges, configs, fem, model, plot

# config = configs.opensees_default(bridges.bridge_example)
# point_loads = [model.PointLoad(config, x=5, z=0, kn=100)]
# responses = fem.responses(config, model.RT.YTranslation, point_loads)
# plot.contour_responses(config, responses, point_loads)
# plot.top_view_bridge(config, piers=True)
# plt.tight_layout()
# plt.show()

# Example 2.

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, fem, model, plot, vehicle

config = configs.opensees_default(bridges.bridge_example, shorten_paths=True)
point_loads = vehicle.wagen1.to_point_load_pw(time=3.5, bridge=config.bridge, list=True)
responses = fem.responses(config, model.RT.YTranslation, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config, piers=True)
plt.tight_layout()
plt.show()

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
