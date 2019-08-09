"""Test features.py."""
import pytest

from classify.data.features import Recorder
from config import Config
from fem.run.opensees import os_runner
from model.bridge_705 import bridge_705_config
from util import print_i

c = bridge_705_config()
fem_runner = os_runner(c)


def test_recorder():
    # Test one response is recorded.
    recorder = Recorder(c)
    response = 1

    def add_response():
        nonlocal response
        recorder.receive(response)
        response += 1

    add_response()
    assert len(recorder.history) == 0
    assert len(recorder.responses) == 1
    assert recorder.maybe_event() is None

    event_length = int(c.time_end / c.time_step)

    # Add until event is one away from being filled.
    for _ in range(event_length - 2):
        add_response()
        assert recorder.maybe_event() is None
    assert len(recorder.history) == 0
    assert len(recorder.responses) == event_length - 1

    # Add one more response, should return an event.
    add_response()
    event = recorder.maybe_event()
    assert isinstance(event, list)
    overlap_length = int(c.time_overlap / c.time_step)
    assert len(recorder.history) == event_length - overlap_length
    assert len(recorder.responses) == overlap_length
    assert recorder.responses[-1] == event[-1]

    # Add responses until a second event is reached.
    event = recorder.maybe_event()
    while event is None:
        add_response()
        event = recorder.maybe_event()
    history_length = event_length * 2 - overlap_length * 2
    assert len(recorder.history) == history_length
    assert recorder.history == list(range(1, history_length + 1))
    assert len(recorder.responses) == overlap_length
    assert recorder.responses == list(range(
        history_length + 1, history_length + overlap_length + 1))
