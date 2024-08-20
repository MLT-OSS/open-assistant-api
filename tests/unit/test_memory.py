import pytest
from app.core.runner.memory import find_memory


@pytest.mark.parametrize(
    "data",
    [
        [{"type": "naive"}, [], []],
        [
            {"type": "naive"},
            [{"role": "user", "content": "text1"}],
            [{"role": "user", "content": "text1"}],
        ],
        [
            {"type": "naive"},
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
        ],
        [{"type": "zero"}, [], []],
        [
            {"type": "zero"},
            [{"role": "user", "content": "text1"}],
            [{"role": "user", "content": "text1"}],
        ],
        [
            {"type": "zero"},
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
            [{"role": "user", "content": "text2"}],
        ],
        [
            {"type": "zero"},
            [{"role": "user", "content": "text1"}, {"role": "assistant", "content": "text2"}],
            [{"role": "user", "content": "text1"}, {"role": "assistant", "content": "text2"}],
        ],
        [{"type": "window"}, [], []],
        [
            {"type": "window", "window_size": 1, "max_token_size": 100},
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
            [{"role": "user", "content": "text2"}],
        ],
        [
            {"type": "window", "window_size": 1, "max_token_size": 100},
            [{"role": "user", "content": "text1"}],
            [{"role": "user", "content": "text1"}],
        ],
        [
            {"type": "window", "window_size": 2, "max_token_size": 6},
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
        ],
        [
            {"type": "window", "window_size": 2, "max_token_size": 5},
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
            [{"role": "user", "content": "text2"}],
        ],
        [
            {"type": "window", "window_size": 2, "max_token_size": 1},
            [{"role": "user", "content": "text1"}, {"role": "user", "content": "text2"}],
            [{"role": "user", "content": "text2"}],
        ],
    ],
)
def test_memory(data):
    (memory, messages, expect_result) = data
    memory = find_memory(assistants_metadata=memory)
    result = memory.integrate_context(messages=messages)
    assert result == expect_result


@pytest.mark.parametrize(
    "kwargs",
    [
        {"window_size": 0, "max_token_size": 2000},
        {"window_size": -1, "max_token_size": 2000},
        {"window_size": 20, "max_token_size": 0},
        {"window_size": 20, "max_token_size": -1},
        {"window_size": 0, "max_token_size": 0},
    ],
)
def test_window_memory_initial_exception(kwargs):
    with pytest.raises(ValueError):
        kwargs["type"] = "window"
        memory = find_memory(assistants_metadata=kwargs)
