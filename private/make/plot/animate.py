from classify.scenario.bridge import HealthyDamage
from classify.scenario.traffic import heavy_traffic_1, normal_traffic
from config import Config
from fem.run.opensees import OSRunner
from model.response import ResponseType
from model.scenario import to_traffic
from plot.animate.traffic import animate_traffic_top_view


def traffic(c: Config):
    """Make animations of different traffic scenarios."""

    max_time, time_step, lam, min_d = 10, 0.1, 5, 2
    c.time_step = time_step
    # for traffic_scenario in [normal_traffic(c=c, lam=lam)]:
    for traffic_scenario in [
        normal_traffic(c=c, lam=lam, min_d=min_d),
        heavy_traffic_1(c=c, lam=lam, min_d=min_d, prob_heavy=0.01),
    ]:

        traffic_sequence, start_time = traffic_scenario.traffic_sequence(
            bridge=c.bridge, max_time=max_time
        )

        traffic = to_traffic(
            bridge=c.bridge,
            traffic_sequence=traffic_sequence,
            max_time=start_time + max_time,
            time_step=time_step,
        )

        start_index = int(start_time / time_step) + 1
        animate_traffic_top_view(
            c=c,
            bridge=c.bridge,
            bridge_scenario=HealthyDamage(),
            traffic_name=traffic_scenario.name,
            traffic=traffic[start_index:],
            start_time=start_index * time_step,
            time_step=time_step,
            fem_runner=OSRunner(c),
            response_type=ResponseType.YTranslation,
            save=c.get_image_path("animations", f"{traffic_scenario.name}.mp4"),
        )
