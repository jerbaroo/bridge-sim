import os

import numpy as np

from classify.scenario.bridge import HealthyDamage
from fem.build import get_bridge_nodes, get_bridge_shells
from fem.model import Node, Shell
from fem.params import SimParams
from fem.responses import load_fem_responses
from fem.run.opensees import OSRunner
from model.load import PointLoad
from model.bridge import Point
from model.bridge.bridge_705 import (
    bridge_705_3d,
    bridge_705_med_config,
    bridge_705_low_config,
)
from model.response import ResponseType
from util import flatten, round_m


def test_interpolate():
    return
    # c = bridge_705_med_config(bridge_705_3d)
    # responses = load_fem_responses(
    #     c=c,
    #     sim_params=SimParams(ploads=[PointLoad(
    #         x_frac=0.5, z_frac=0.5, kn=100,
    #     )]),
    #     response_type=ResponseType.YTranslation,
    #     sim_runner=OSRunner,
    # )
    # nodes = flatten(get_bridge_nodes(c.bridge), Node)
    # for node in nodes:
    # interp_response = responses.at_deck(Point(x=node.x, z=node.z), interp=True)
    # snap_response = responses.at_deck(Point(x=node.x, z=node.z), interp=False)
    # print(interp_response, snap_response)
    # assert np.isclose(interp_response, snap_response)


def test_strain_locations():
    if "NO_OS_TESTS" in os.environ:
        return
    c = bridge_705_low_config(bridge_705_3d)
    # Get the shells used in the model.
    shells = flatten(get_bridge_shells(c.bridge), Shell)
    # Pick a shell and setup calculation of integration point positions.
    shell = shells[len(shells) // 2]
    print(shell.center())
    xs = list(set([node.x for node in shell.nodes()]))
    zs = list(set([node.z for node in shell.nodes()]))
    assert len(xs) == 2
    assert len(zs) == 2
    x_dist, z_dist = abs(xs[0] - xs[1]), abs(zs[0] - zs[1])
    assert x_dist == shell.length()
    assert z_dist == shell.width()
    # Load simulation responses, with a point load at a shell node.
    node = shell.nodes()[0]
    responses = load_fem_responses(
        c=c,
        sim_params=SimParams(
            ploads=[
                PointLoad(
                    x_frac=c.bridge.x_frac(node.x),
                    z_frac=c.bridge.z_frac(node.z),
                    kn=100,
                )
            ]
        ),
        response_type=ResponseType.Strain,
        sim_runner=OSRunner,
        run=True,
    )
    # For each integration point, check if it's in responses.
    response_xzs = []
    int_responses = []
    for xmul, zmul in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
        delta_x = xmul * x_dist / (2 * np.sqrt(3))
        delta_z = zmul * z_dist / (2 * np.sqrt(3))
        integration_x = round_m(shell.center().x + delta_x)
        integration_z = round_m(shell.center().z + delta_z)
        response_x = None
        for deck_x in responses.deck_xs:
            if np.isclose(deck_x, integration_x):
                response_x = deck_x
                break
        if response_x is None:
            assert False
        deck_zs = responses.zs[response_x][0]
        print(integration_x, integration_z, response_x)
        print(deck_zs)
        response_z = None
        for deck_z in deck_zs:
            print(deck_z)
            if np.isclose(deck_z, integration_z):
                response_z = deck_z
                break
        if response_z is None:
            assert False
        response_xzs.append((response_x, response_z))
        int_responses.append(responses.responses[0][response_x][0][response_z])
    print(int_responses)
    assert len(list(set(int_responses))) == 4
    # Place a point load at each node, and ensure the opposite integration point
    # has the least response of all the integration points.
    assert shell.nodes()[0].x < shell.nodes()[1].x
    assert shell.nodes()[1].z < shell.nodes()[2].z
    assert shell.nodes()[2].x > shell.nodes()[3].x
    assert shell.nodes()[3].z > shell.nodes()[0].z
    # for node_i, node in enumerate(shell.nodes()):
    #     responses = load_fem_responses(
    #         c=c,
    #         sim_params=SimParams(ploads=[PointLoad(
    #             x_frac=c.bridge.x_frac(node.x),
    #             z_frac=c.bridge.z_frac(node.z),
    #             kn=100,
    #         )]),
    #         response_type=ResponseType.Strain,
    #         sim_runner=OSRunner,
    #         run=True,
    #     )
    #     integration_point_responses = []
    #     for response_x, response_z in response_xzs:
    #         integration_point_responses.append(responses.responses[0][response_x][0][response_z])
    # close_response = integration_point_responses[node_i]
    # for i in range(4):
    #     if i != node_i:
    #         assert integration_point_responses[i] < close_response
    # print()
    # print(response_i)
    # print(node.x, node.z)
    # print(response_xzs)
    # print(integration_point_responses)
    # import sys; sys.exit()
    # responses = load_fem_responses( c=c,
    # sim_params=healthy_damage.use(c)[1], response_type=ResponseType.Strain,
    # sim_runner=OSRunner, run=True, )
