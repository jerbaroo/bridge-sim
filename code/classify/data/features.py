"""Extract features from a time series of responses."""
from typing import Callable, List, Optional, NewType, Tuple, Union

from classify.data.responses import responses_to_mv_load
from config import Config
from fem.run import FEMRunner
from model import MovingLoad, Point, ResponseType
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
        self.stop = (lambda _e, _h: False) if stop is None else stop


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
    """Receive real-time responses and emit events."""
    def __init__(
            self, c: Config, trigger: Trigger = always_trigger(),
            max_history: int = 10000):
        self.c = c
        self.trigger = trigger  # Decides to start/stop recording.
        self.max_history = max_history  # Soft-limit on history length.
        self.recording = lambda: len(self.responses) > 0  # If currently recording.
        self.overlap = 0  # Amount of current event which overlaps previous event.
        self.start_index = None  # Start index of current event.
        self.index = 0  # Current time index.
        self.history = []  # Responses prior to the current event.
        self.responses = []  # Responses of current event so far.

    def receive(self, response: float, overlap: bool = False):
        """Receive a new response."""
        # If already recording, record the response.
        if self.recording():
            self.responses.append(response)
            if overlap:
                self.overlap += 1
        # Else if not recording.
        else:
            # Add the response to history, unless we..
            self.history.append(response)
            # ..need to start recording, then move the response
            # to the new current event, and save the start index.
            if self.trigger.start(self.history):
                self.responses = [self.history.pop()]
                self.start_index = self.index
                if overlap:
                    self.overlap += 1
        # Increment time index.
        self.index += 1

    def maybe_event(self, info: bool = False) -> Optional[TimeSeries]:
        """Return an event if a new event is available."""
        if self.recording():
            event_time = len(self.responses) * self.c.time_step
            # Check if an event is ready to be returned.
            if (event_time >= self.c.time_end or
                    self.trigger.stop(self.responses, self.history)):
                # Split the event into new overlap and new history.
                event = self.responses
                overlap_length = int(self.c.time_overlap / self.c.time_step)
                new_history = event[:-overlap_length]
                new_overlap = event[-overlap_length:]
                assert len(new_overlap) + len(new_history) == len(event)
                # Reset event, and update history with the current event.
                self.responses = []
                self.history.extend(new_history)
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]
                # Determine overlap of this event, and start time.
                prev_overlap = self.overlap
                prev_start_index = self.start_index
                # Reset overlap and index and "receive" overlap.
                self.overlap = 0
                self.index -= len(new_overlap)
                for response in new_overlap:
                    self.receive(response, overlap=True)
                # Structure and return result.
                if info:
                    return [event, prev_overlap, prev_start_index]
                return event


def events_from_mv_load(
        c: Config, mv_load: MovingLoad, response_type: ResponseType,
        fem_runner: FEMRunner, at: List[Point], per_axle: bool = False,
        trigger: Trigger = always_trigger(), info: bool = False) -> List[Event]:
    """Yield events from a moving load."""
    responses = responses_to_mv_load(
        c=c, mv_load=mv_load, response_type=response_type,
        fem_runner=fem_runner, at=at)
    print_w(f"**")
    print_w(f"length responses = {len(responses)}")
    print_w(f"**")
    recorder = Recorder(c, trigger)
    for response in responses:
        recorder.receive(response)
        maybe_event = recorder.maybe_event(info=info)
        if maybe_event is not None:
            yield maybe_event


# def events_from_time_series(
#         c: Config, trigger: Trigger, time_series: TimeSeries,
#         with_time: bool=False
#     ) -> Union[List[Event], Tuple[List[Event], List[int]]]:
#     """Return all events found in a time series of responses.

#     Args:
#         trigger: Trigger, when to start and stop recording an event.
#         time_series: TimeSeries, the history of responses to search for events.
#         with_time: bool, return the start time of each event. So the return
#             type is List[Tuple[Event, int]].

#     TODO: Rewrite using recorder or deprecate.

#     """
#     events = []
#     event_start_times = []
#     event_start_time = None
#     event_recording = False
#     event_max_length = c.time_end / c.time_step + 1
#     for t in range(len(time_series)):
#         time_series_so_far = time_series[:t + 1]
#         if event_recording:
#             if (t * c.time_step - event_start_time * c.time_step > c.time_end
#                     or trigger.end(time_series_so_far)):
#                 events.append(time_series_so_far[event_start_time:])
#                 event_start_times.append(event_start_time)
#                 print_d(f"t - event_start_time = {t - event_start_time}")
#                 print_d(f"c.time_end = {c.time_end}")
#                 print_d(f"trigger end = {trigger.end(time_series_so_far)}")
#                 print_d(f"len events = {len(events)}")
#                 print_d(f"len event start times = {len(event_start_times)}")
#                 event_recording = False
#         # Not recording.
#         else:
#             if trigger.start(time_series_so_far):
#                 event_start_time = t
#                 event_recording = True
#         print_d(f"t = {t}, value = {time_series[t]}, recording = {event_recording}")
#     if event_recording:
#         events.append(time_series_so_far[event_start_time:])
#         event_start_times.append(event_start_time)
#     if with_time:
#         return events, event_start_times
#     return events
