import itertools

from bridge_sim.model import PierSettlement
from lib.classify.scenario.bridge import (
    Healthy,
    PierDisp,
    Thermal,
    equal_pier_disp,
    longitudinal_pier_disp,
    transverse_crack,
)

healthy_scenario = Healthy()
cracked_scenario = transverse_crack()

# Each pier displaced by 1mm.
each_pier_scenarios = lambda c: [
    PierDisp([PierSettlement(displacement=0.001, pier=p)])
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

healthy_and_cracked_scenarios = [healthy_scenario, cracked_scenario]

unit_temp_scenario = Thermal(axial_delta_temp=1, moment_delta_temp=1)

all_scenarios = lambda c: (
    healthy_and_cracked_scenarios
    + [unit_temp_scenario]
    + each_pier_scenarios(c)
    + equal_pier_scenarios(c)
    + gradient_pier_scenarios(c)
)
