from typing import List
from config import Config
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.response import ResponseType
from model.scenario import BridgeScenario
from plot import plt
from plot.geometry import top_view_bridge
from plot.responses import plot_contour_deck


def damage_scenario_contour_plot(
    c: Config,
    response_types: List[ResponseType],
    damage_scenario: BridgeScenario,
    titles: List[str],
    saves: str
):
    """Save a contour plot of a damage scenario under direct simulation."""
    c, sim_params = damage_scenario.use(c=c, sim_params=SimParams(response_types=response_types))
    for response_type, title, save in zip(response_types, titles, saves):
        sim_responses = load_fem_responses(
            c=c,
            sim_runner=OSRunner(c),
            response_type=response_type,
            sim_params=sim_params,
        )
        top_view_bridge(c.bridge, abutments=True, piers=True)
        plot_contour_deck(c=c, responses=sim_responses, levels=100)
        plt.title(title)
        plt.savefig(save)
        plt.close()
