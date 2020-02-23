from collections import defaultdict
from sklearn import mixture
import numpy as np

from config import Config
from classify.util import flip
from classify.data.responses import responses_to_traffic_array
from classify.data.traffic import load_traffic
from classify.scenario.traffic import normal_traffic
from classify.scenario.bridge import healthy_damage, pier_disp_damage
from fem.run.opensees import OSRunner
from model.bridge import Point
from model.response import ResponseType
from plot import plt
from util import print_i


def cluster_damage(c: Config, mins: float):
    # Create the traffic.
    traffic_scenario = normal_traffic(c=c, lam=5, min_d=2)
    traffic_sequence, traffic, traffic_array = load_traffic(
        c=c,
        traffic_scenario=traffic_scenario,
        max_time=mins * 60,
    )
    point = Point(x=21, y=0, z=-8.4)  # Point to investigate.
    # Collect vertical translation and strain for all damage scenarios.
    responses_y = []
    responses_s = []
    for damage_scenario in [healthy_damage, pier_disp_damage([(5, 0.5 / 1000)])]:
        responses_y.append(responses_to_traffic_array(
            c=c,
            traffic_array=traffic_array,
            response_type=ResponseType.YTranslation,
            damage_scenario=damage_scenario,
            points=[point],
            sim_runner=OSRunner(c),
        ).T[0] * 1000)
        assert len(responses_y[-1]) == len(traffic_array)
        responses_s.append(responses_to_traffic_array(
            c=c,
            traffic_array=traffic_array,
            response_type=ResponseType.Strain,
            damage_scenario=damage_scenario,
            points=[point],
            sim_runner=OSRunner(c),
        ).T[0])
        assert len(responses_s[-1]) == len(traffic_array)
    # Calculate features per damage.
    damage_features = []
    damage_labels = []
    for damage_ind in range(len(responses_y)):
        y = responses_y[damage_ind]
        s = responses_s[damage_ind]
        for response_ind in range(len(y)):
            damage_features.append([y[response_ind], s[response_ind]])
            damage_labels.append(damage_ind)
    damage_features = np.array(damage_features)
    damage_labels = np.array(damage_labels)
    print_i(f"Dimensions of feature array = {damage_features.shape}")
    # Plot the reference data.
    plt.landscape()
    plt.scatter(damage_features[:, 0], damage_features[:, 1], c=damage_labels)
    plt.title("Reference")
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify/cluster", "cluster-ref.pdf"))
    plt.close()
    # Plot the gaussian mixture results.
    gmm = mixture.GaussianMixture(n_components=2).fit(damage_features)
    labels = flip(l=gmm.predict(damage_features), ref=damage_labels)
    plt.landscape()
    plt.scatter(damage_features[:, 0], damage_features[:, 1], c=labels)
    plt.title("Gaussian mixture n = 2")
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify/cluster", "cluster-model.pdf"))
    plt.close()
    # Plot and print the accuracy.
    # https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/custom_legends.html
    acc = abs(labels - damage_labels)
    total = defaultdict(lambda: 0)
    correct = defaultdict(lambda: 0)
    for ind, label in enumerate(damage_labels):
        total[label] += 1
        if acc[ind] == 0:
            correct[label] += 1
    for k, t in total.items():
        print_i(f"k = {k}: {correct[k]} / {t} = {correct[k] / t}")
    plt.scatter(damage_features[:, 0], damage_features[:, 1], c=acc)
    plt.tight_layout()
    plt.savefig(c.get_image_path("classify/cluster", "cluster-acc.pdf"))
    plt.close()
