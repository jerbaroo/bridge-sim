import itertools

from classify.scenario.bridge import (
    HealthyBridge,
    PierDispBridge,
    center_lane_crack,
    equal_pier_disp,
    longitudinal_pier_disp,
    start_lane_crack,
)
from model.load import DisplacementCtrl

healthy_scenario = HealthyBridge()

cracked_scenario = center_lane_crack()
cracked_scenario2 = start_lane_crack()

# Each pier displaced by 1mm.
each_pier_scenarios = lambda c: [
    PierDispBridge([DisplacementCtrl(displacement=0.001, pier=p)])
    for p, _ in enumerate(c.bridge.supports)
]

equal_pier_scenarios = lambda c: [
    equal_pier_disp(bridge=c.bridge, displacement=displacement)
    for displacement in [0.1, 0.01]
]

gradient_pier_scenarios = lambda c: [
    longitudinal_pier_disp(bridge=c.bridge, start=start, step=step)
    for start, step in itertools.product([0.01, 0.02, 0.05], [0.01, 0.02, 0.05])
]

healthy_and_cracked_scenarios = lambda c: (
    [healthy_scenario] + [cracked_scenario] + [cracked_scenario2]
)

all_scenarios = lambda c: (
    healthy_and_cracked_scenarios(c)
    + each_pier_scenarios(c)
    + equal_pier_scenarios(c)
    + gradient_pier_scenarios(c)
)
