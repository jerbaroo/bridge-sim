########################################
# Example 1: responses to a point-load #
########################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, plot, sim

config = configs.opensees_default(bridges.bridge_narrow)
point_loads = [model.PointLoad(x=5, z=0, load=100)]
responses = sim.responses.load(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config.bridge, piers=True)
plt.tight_layout()
plt.show()

############################################
# Example 2: responses to a static vehicle #
############################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, plot, sim

config = configs.opensees_default(bridges.bridge_narrow, shorten_paths=True)
point_loads = model.Vehicle(
    # Load intensity of each axle.
    load=[5000, 4000, 4000, 5000, 7000],
    # Distance between each pair of axles.
    axle_distances=[2, 2, 2, 1],
    # Width of each axle, distance between point loads.
    axle_width=2.5,
    # Speed of the vehicles.
    kmph=20,
).point_load_pw(config=config, time=3.5, list=True)
responses = sim.responses.load(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config.bridge, piers=True)
plt.tight_layout()
plt.show()

###########################################
# Example 3: responses to pier settlement #
###########################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, sim, model, plot

config = configs.opensees_default(bridges.bridge_wide)
responses = sim.responses.load(
    config,
    model.RT.YTrans,
    pier_settlement=[model.PierSettlement(0, 1.2)]
)
plot.contour_responses(config, responses)
plot.top_view_bridge(config.bridge, piers=True)
plt.tight_layout()
plt.show()

################################################
# Example 4: plotting different response types #
################################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, plot, sim

config = configs.opensees_default(bridges.bridge_wide)
plt.figure(figsize=(12, 8))
for subplot, response_type in enumerate([
        model.RT.YTrans, model.RT.ZTrans,
        model.RT.StrainXXB, model.RT.StrainZZB,
    ]):
    responses = sim.responses.load(
        config,
        response_type,
        pier_settlement=[model.PierSettlement(0, 1.2)],
    )
    plt.subplot(2, 2, subplot + 1)
    plot.contour_responses(config, responses, interp=(200, 60))
    plot.top_view_bridge(config.bridge, piers=True)
    plt.title(response_type.name())
plt.tight_layout()
plt.show()

#######################################
# Example 5: creating a custom bridge #
#######################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, plot, sim
from bridge_sim.bridges import Bridge, Lane, MaterialDeck, MaterialSupport, Support


def new_bridge():
    return Bridge(
        name="square",  # Name used to identify saved/loaded data.
        msl=0.5,  # Maximum shell length.
        length=10,  # Length of this bridge.
        width=10,  # Width of this bridge.
        supports=[
            Support(
                x=5,  # X position of center of the support.
                z=0,  # Z position of center of the support.
                length=2,  # Length between support columns (X direction).
                height=2,  # Height from top to bottom of support.
                width_top=2,  # Width of support column at top (Z direction).
                width_bottom=1,  # Width of support column at bottom (Z direction).
                materials=[  # List of materials for the support columns.
                    MaterialSupport(
                        density=0.7,
                        thickness=0.7,
                        youngs=40000,
                        poissons=0.2,
                        start_frac_len=0,
                    )
                ],
                fix_z_translation=True,
                fix_x_translation=True,
            )
        ],
        # List of materials for the bridge deck.
        materials=[MaterialDeck(thickness=0.7, youngs=40000, poissons=0.2,)],
        # List of lanes where traffic can drive on the bridge.
        lanes=[Lane(-1, 1, True)],
    )
config = configs.opensees_default(new_bridge)
point_loads = [model.PointLoad(x=8, z=0, load=100)]
responses = sim.responses.load(config, model.RT.YTrans, point_loads)
plot.contour_responses(config, responses, point_loads)
plot.top_view_bridge(config.bridge, piers=True, lanes=True)
plt.tight_layout()
plt.show()

##########################################################
# Example 6: simple animation of traffic over bridge 705 #
##########################################################

from bridge_sim import bridges, configs, plot, traffic

config = configs.opensees_default(bridges.bridge_705(0.5))
time = 10
config.sensor_freq = 1 / 10
traffic_scenario = traffic.normal_traffic(config)
traffic_sequence = traffic_scenario.traffic_sequence(config, time)
traffic = traffic_sequence.traffic()
plot.animate.animate_traffic(
    config=config,
    traffic_sequence=traffic_sequence,
    traffic=traffic,
    save="animation.mp4"
)

################################################
# Example 7: animation of responses to traffic #
################################################

from bridge_sim import bridges, configs, model, plot, temperature, traffic

config = configs.opensees_default(bridges.bridge_705(10), il_num_loads=100)
time = 10
config.sensor_freq = 1 / 10
traffic_scenario = traffic.normal_traffic(config)
traffic_sequence = traffic_scenario.traffic_sequence(config, time)
weather = temperature.load("holly-springs-19")
weather["temp"] = temperature.resize(weather["temp"], tmin=-5, tmax=35)
plot.animate.animate_responses(
    config=config,
    traffic_sequence=traffic_sequence,
    response_type=model.ResponseType.YTrans,
    units="mm",
    save="traffic-responses.mp4",
    pier_settlement=[
        (model.PierSettlement(4, 1.2), model.PierSettlement(4, 2))],
    weather=weather,
    start_date="01/05/2019 00:00",
    end_date="01/05/2019 23:59",
    install_day=30,
    start_day=365,
    end_day=366,
    with_creep=True,
)

#################################################
# Example 8: contour plot of temperature effect #
#################################################

import matplotlib.pyplot as plt
import numpy as np
from bridge_sim import bridges, configs, model, sim, plot, temperature

config = configs.opensees_default(bridges.bridge_705(msl=10))
bridge = config.bridge
response_type = model.RT.StrainXXB

points = [
    model.Point(x=x, y=0, z=z)
    for x in np.linspace(bridge.x_min, bridge.x_max, num=int(bridge.length * 2))
    for z in np.linspace(bridge.z_min, bridge.z_max, num=int(bridge.width * 2))
]
temp_effect = temperature.effect(
    config=config, response_type=response_type, points=points, temps_bt=[[20], [22]]
).T[0]  # Only considering a single temperature profile.
responses = sim.model.Responses(  # Converting to "Responses" for plotting.
    response_type=response_type,
    responses=[(temp_effect[p], points[p]) for p in range(len(points))],
).without_nan_inf()
plot.contour_responses(config, responses)
plot.top_view_bridge(config.bridge, piers=True)
plt.tight_layout()
plt.show()

###################################################
# Example 9: time series, traffic and temperature #
###################################################

import matplotlib.pyplot as plt
from bridge_sim import bridges, configs, model, sim, temperature, traffic

config = configs.opensees_default(bridges.bridge_705(10), il_num_loads=100)
points = [model.Point(x=10), model.Point(x=20)]
response_type = model.RT.YTrans

# First generate some traffic data.
traffic_sequence = traffic.normal_traffic(config).traffic_sequence(config, 10)
traffic_array = traffic_sequence.traffic_array()
responses_to_traffic = sim.responses.to_traffic_array(
    config=config,
    traffic_array=traffic_array,
    response_type=response_type,
    points=points,
)

# And responses to temperature.
weather = temperature.load("holly-springs-19")
weather["temp"] = temperature.resize(weather["temp"], tmin=-5, tmax=31)
temp_responses = sim.responses.to_temperature(
    config=config,
    points=points,
    responses_array=responses_to_traffic,
    response_type=response_type,
    weather=weather,
    start_date="01/05/2019 00:00",
    end_date="02/05/2019 00:00",
)

plt.plot((responses_to_traffic + temp_responses).T)
plt.show()
