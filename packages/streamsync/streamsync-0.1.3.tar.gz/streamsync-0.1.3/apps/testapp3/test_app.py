from streamsync.core import StreamsyncState
import main


class TestApp:

    initial_state = main.ss.initial_state
    artificial_state = StreamsyncState({
        "a": 3,
        "b": 2
    })

    def test_counter_must_start_from_zero(self):
        assert self.initial_state["counter"] == 0

    def test_handle_multiplication(self):
        main.handle_multiplication(self.artificial_state)
        assert self.artificial_state["n"] == 6
