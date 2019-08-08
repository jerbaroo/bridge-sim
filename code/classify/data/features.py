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
            stop: Callable[[TimeSeries, Event], bool]=None):
        self.name = name
        self.description = description
        self.start = start
        self.stop = (lambda _, _: False) if stop is None else stop


def always_trigger() -> Trigger:
    """A trigger that always fires."""
    return Trigger("always", "always", lambda _: True)


def abs_threshold_trigger(threshold: float) -> Trigger:
    """A trigger that fires when an absolute threshold is exceeded."""
    return Trigger(
        f"abs-threshold-{threshold:.2f}",
        f"when |response| exceeds {threshold:.2f}",
        lambda xs: abs(xs[-1]) > threshold)


class Recorder:
    """Receives real-time responses and emits events."""
    def __init__(self, c: Config, trigger: Trigger, max_history: int=10000):
        self.c = c
        self.trigger = trigger
        self.recording = lambda: len(responses) > 0
        self.history = []
        self.responses = []

    def receive(self, response):
        """Receive a new response."""
        # If recording, record the response.
        if self.recording():
            self.responses.append(response)
        # Else if not recording.
        else:
            self.history.append(response)
            # Start recording.
            if trigger.start(self.history):
                self.responses.append(self.history.pop())
            # Do not start recording.

    def maybe_event(self) -> Optional[TimeSeries]:
        """Return an event if a new event is available."""
        if self.recording():
            event_time = len(responses) * c.time_step
            print_d(f"event time = {event_time}")
            # Check if an event is ready to be returned.
            if (event_time => self.c.time_end or
                    trigger.stop(self.responses, self.history)):
                event = self.responses
                overlap_length = int(self.c.time_overlap / self.c.time_step)
                print_d(f"overlap length = {overlap_length}")
                new_history = event[:-overlap_length]
                overlap = event[-overlap_length:]
                assert len(overlap) + len(new_history) == len(event)
                # Reset responses, receive the overlap and update history.
                self.responses = []
                self.history.extend(new_history)
                if len(self.history) > self.max_history:
                    print_w(f"Shortening history")
                    self.history = self.history[-self.max_history:]
                for response in overlap:
                    self.receive(response)


# def events_from_mv_load(
#         c: Config, trigger: Trigger, mv_load: MovingLoad):


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

    TODO: Rewrite using recorder or deprecate.

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
