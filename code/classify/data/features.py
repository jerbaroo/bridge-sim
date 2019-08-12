"""Extract events from a time series of responses."""
# TODO: Split between events, event, trigger, recorder.
from typing import Callable, Iterable, List, Optional, NewType, Tuple, Union

import numpy as np

from classify.data.responses import responses_to_mv_loads
from config import Config
from fem.run import FEMRunner
from model import MovingLoad, Point, ResponseType, TimeSeries
from util import *


class Event:
    """A recorded time series of responses."""
    def __init__(
            self, time_series: TimeSeries = None, noise: TimeSeries = None,
            axle_time_series: List[TimeSeries] = None,
            axle_noise: List[TimeSeries] = None, overlap: int = None,
            start_index: int = None):
        self.time_series = time_series
        self.noise = noise
        self.axle_time_series = axle_time_series
        self.axle_noise = axle_noise
        self.overlap = overlap
        self.start_index = start_index

    def get_time_series(self, noise: bool = True):
        """Return the time series optionally with noise."""
        if not noise:
            return self.time_series
        return list(sum(x) for x in zip(self.time_series, self.noise))

    def get_axle_time_series(self, noise: bool = True):
        """Return the axle time series optionally with noise."""
        if not noise:
            return self.axle_time_series
        return list(
            sum(x) for x in zip(self.axle_time_series, self.axle_noise))


class Trigger:
    """A method of deciding when to start and stop recording an event."""
    def __init__(
            self, name: str, description: str,
            start: Callable[[TimeSeries], bool],
            stop: Callable[[TimeSeries, Event], bool] = None):
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
    """Receive real-time responses and emit events, optionally with noise."""
    def __init__(
            self, c: Config, response_type: ResponseType,
            trigger: Trigger = always_trigger(), max_history: int = 10000,
            add_noise: bool = True):
        self.c: Config = c
        self.response_type = response_type
        # Decides to start/stop recording.
        self.trigger: Trigger = trigger
        # Soft-limit on history length.
        self.max_history: int = max_history
        # Add noise to the Event.
        self.add_noise = add_noise
        # If currently recording.
        self.recording: Callable[[], bool] = lambda: len(self.responses) > 0
        # Amount of responses which overlap previous event.
        self.overlap: int = 0
        # Start index of current event.
        self.start_index: int = None
        # Current time index.
        self.index: int = 0
        # Responses prior to the current event.
        self.history: Union[List[float], List[List[float]]] = []
        # Responses of current event so far.
        self.responses: Union[List[float], List[List[float]]] = []

    def receive(
            self, response: Union[float, List[float]], overlap: bool = False):
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

    def maybe_event(self) -> Optional[Event]:
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
                # Return an event with additional info.
                print(type(event[0]))
                by_axle = False
                # TODO: if hasattr(event[0], "__len__")
                try:
                    len(event[0])
                    by_axle = True
                except:
                    pass
                assert isinstance(event, list)
                assert isinstance(event[0], float)
                assert not by_axle
                if self.add_noise:
                    noise = np.random.normal(
                        self.c.noise_mean(self.response_type),
                        self.c.noise_stddev(self.response_type),
                        len(event))
                print_w(f"TODO: Axle noise")
                return Event(
                    time_series = event if not by_axle else None,
                    noise = noise if not by_axle else None,
                    axle_time_series = event if by_axle else None,
                    axle_noise = None,
                    overlap = prev_overlap,
                    start_index = prev_start_index)


def events_from_mv_loads(
        c: Config, mv_loads: List[MovingLoad], response_type: ResponseType,
        fem_runner: FEMRunner, at: Point, per_axle: bool = False,
        trigger: Trigger = always_trigger()) -> Iterable[Event]:
    """Yield events from a moving load."""
    # Map from a list of points to a single point.
    responses = list(map(lambda x: x[0], responses_to_mv_loads(
        c=c, mv_loads=mv_loads, response_type=response_type,
        fem_runner=fem_runner, at=[at])))
    print(np.array(responses).shape)
    print_w(f"**")
    print_w(f"length responses = {len(responses)}")
    print_w(f"**")
    recorder = Recorder(c=c, trigger=trigger, response_type=response_type)
    for response in responses:
        recorder.receive(response)
        maybe_event = recorder.maybe_event()
        if maybe_event is not None:
            yield maybe_event
