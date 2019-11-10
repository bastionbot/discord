import asyncio
from asyncio import Future

from unittest.mock import patch, MagicMock

import pytest
from asynctest import CoroutineMock

from bastion.utils.trackers import Timer


async def mock_fn(*args, **kwargs):
    pass


def test_create_timer():
    timeout = 60
    name = 'timer_name'
    args = (1, 2, 3)
    kwargs = {"a": 1}

    timer = Timer(timeout, mock_fn, name, *args, **kwargs)

    assert timer.timeout == timeout
    assert timer.callback == mock_fn
    assert timer.callback_args == args
    assert timer.callback_kwargs == kwargs

    timer_2 = Timer(timeout, mock_fn, name)

    assert timer_2.timeout == timeout
    assert timer_2.callback == mock_fn
    assert timer_2.callback_args == ()
    assert timer_2.callback_kwargs == {}


@patch('asyncio.create_task')
def test_start_calls_asyncio_and_timer_cancellation(create_task_mock):
    timeout = 0
    name = 'timer_name'
    timer = Timer(timeout, mock_fn, name)

    timer.start()

    create_task_mock.assert_called_with(timer.handle_function)


@pytest.mark.asyncio
async def test_handle_function_callback_is_called_with_args():
    start_mock = MagicMock()
    mock_callback = CoroutineMock()
    args = (1, 2, 3)
    kwargs = {"a": 1}
    timeout = 0
    name = 'timer_name'
    timer = Timer(timeout, mock_callback, name, *args, **kwargs)
    timer.start = start_mock

    await timer.handle_function()

    mock_callback.assert_called_once_with(*args, **kwargs)
    start_mock.assert_called_once()

