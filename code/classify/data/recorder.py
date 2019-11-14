"""Record events from real-time responses."""
from typing import Callable, List, Optional, Union

import numpy as np

from classify.data.trigger import Trigger
from config import Config
from model.response import Event, ResponseType
from util import print_w


class Recorder:
    """Receive a stream of responses and emit events, optionally with noise.

    Args:
        c: Config, global configuration object.
        response_type: ResponseType, the type of response being recorded.
        trigger: Trigger, decides whether to start/stop recording.
        max_history: int, soft-limit on history length.
        add_noise: bool, whether to add noise to an event.

    """

    def __init__(
        self,
        c: Config,
        response_type: ResponseType,
        trigger: Trigger,
        max_history: int = 10000,
        add_noise: bool = True,
    ):
        self.c: Config = c
        self.response_type = response_type
        self.trigger: Trigger = trigger
        self.max_history: int = max_history
        self.add_noise = add_noise

        # If currently recording.
        self.recording: Callable[[], bool] = lambda: len(self.responses) > 0
        # Amount of responses which overlap previous event.
        self.overlap: int = 0
        # Start index of current event.
        self.start_index: Optional[int] = None
        # Current time index.
        self.index: int = 0
        # Responses prior to the current event.
        self.history: Union[List[float], List[List[float]]] = []
        # Responses of current event so far.
        self.responses: Union[List[float], List[List[float]]] = []

    def receive(
        self, response: Union[float, List[float]], overlap: bool = False
    ):
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
            if event_time >= self.c.time_end or self.trigger.stop(
                self.responses, self.history
            ):
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
                    self.history = self.history[-self.max_history :]
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
                except TypeError:
                    pass
                assert isinstance(event, list)
                print_w(type(event[0]))
                assert isinstance(event[0], float) or isinstance(event[0], int)
                assert not by_axle
                noise = (
                    None
                    if not self.add_noise
                    else np.random.normal(
                        self.c.noise_mean(self.response_type),
                        self.c.noise_stddev(self.response_type),
                        len(event),
                    )
                )
                print_w(f"TODO: Axle noise")
                return Event(
                    time_series=event if not by_axle else None,
                    noise=noise if not by_axle else None,
                    axle_time_series=event if by_axle else None,
                    axle_noise=None,
                    overlap=prev_overlap,
                    start_index=prev_start_index,
                )
