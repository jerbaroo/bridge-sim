"""Extract features from a time series of responses."""
from typing import Callable, List, NewType, Tuple, Union

from config import Config
from util import *

# A time series of responses after a trigger.
Event = NewType("Event", List[float]) 

# A more general time series of responses.
TimeSeries = NewType("Responses", List[float])


class Trigger:
    """A method of deciding when to start and stop recording an event."""
    def __init__(
            self, name: str, description: str,
            start: Callable[[TimeSeries], bool],
            end: Callable[[TimeSeries], bool]=None):
        self.name = name
        self.description = description
        self.start = start
        self.end = end if end else lambda _: False


def abs_threshold_trigger(threshold: float) -> Trigger:
    """A trigger that fires when an absolute threshold is exceeded."""
    return Trigger(
        f"abs-threshold-{threshold:.2f}",
        f"When |response| exceeds {threshold:.2f}",
        lambda xs: abs(xs[-1]) > threshold)
        # lambda xs: abs(xs[-1]) < threshold)


def events_from_time_series(
        c: Config, trigger: Trigger, time_series: TimeSeries,
        with_time: bool=False
    ) -> Union[List[Event], Tuple[List[Event], List[int]]]:
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
    event_max_length = c.time_end / c.time_step + 1
    for t in range(len(time_series)):
        time_series_so_far = time_series[:t + 1]
        if event_recording:
            if (t * c.time_step - event_start_time * c.time_step > c.time_end
                    or trigger.end(time_series_so_far)):
                events.append(time_series_so_far[event_start_time:])
                event_start_times.append(event_start_time)
                print_d(f"t - event_start_time = {t - event_start_time}")
                print_d(f"c.time_end = {c.time_end}")
                print_d(f"trigger end = {trigger.end(time_series_so_far)}")
                print_d(f"len events = {len(events)}")
                print_d(f"len event start times = {len(event_start_times)}")
                event_recording = False
        # Not recording.
        else:
            if trigger.start(time_series_so_far):
                event_start_time = t
                event_recording = True
        print_d(f"t = {t}, value = {time_series[t]}, recording = {event_recording}")
    if event_recording:
        events.append(time_series_so_far[event_start_time:])
        event_start_times.append(event_start_time)
    if with_time:
        return events, event_start_times
    return events
