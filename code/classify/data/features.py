"""Extract features from time series of responses."""
from typing import List, NewType

from config import Config

# A time series of responses after a trigger.
Event = NewType("Event", List[float]) 

# A more general time series of responses.
TimeSeries = NewType("Responses", List[float])


class Trigger:
    """A method of deciding when to start and stop recording an event."""
    def __init__(
            self, name: str, description: str,
            trigger: start[[TimeSeries], bool]):
        self.name = name
        self.description = description
        self.start = start
        self.end = end


def abs_threshold_trigger(threshold: float) -> Trigger:
    """A trigger that fires when an absolute threshold is exceeded."""
    return Trigger(
        f"abs-threshold-{threshold:.2f}",
        f"When |response| exceeds {threshold:.2f}",
        lambda xs: abs(x[-1]) > threshold,
        lambda xs: abs(x[-1]) < threshold)


def events(
        c: Config, trigger: Trigger, time_series: TimeSeries,
        with_time: bool=False) -> Union[List[Event], List[Tuple[Event, int]]]:
    """Return all events found in a time series of responses.

    Args:
        trigger: Trigger, when to start and stop recording an event.
        time_series: TimeSeries, the history of responses to search for events.
        with_time: bool, return the start time of each event. So the return
            type is List[Tuple[Event, int]].

    """
    events = []
    event_start_times = []
    event_start_time = None
    event_recording = False
    event_max_length = c.time_record / c.time_step + 1
    for t in range(len(time_series)):
        time_series_so_far = time_series[:t + 1]
        if event_recording:
            if (t - event_start_time > c.time_record
                    or trigger.end(time_series_so_far)):
                events.append(time_series[event_start_time:])
                event_recording = False
        # Not recording.
        else:
            if trigger.start(time_series_so_far):
                event_start_time = t
                event_start_times.append(t)
                event_recording = True
    if with_time:
        return zip(events, event_start_times)
    return events
