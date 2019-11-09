import asyncio
from asyncio import Future

from unittest.mock import patch, Mock

import pytest

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


@patch('bastion.utils.trackers.asyncio.create_task')
def test_start_calls_asyncio(create_task_mock):
    create_task_mock.return_value = 'CREATE_TASK_RETVAL'
    timeout = 60
    name = 'timer_name'
    timer = Timer(timeout, mock_fn, name)

    timer.start()

    assert create_task_mock.is_called_with(timer.handle_function())
    assert timer.task == 'CREATE_TASK_RETVAL'


# @pytest.mark.asyncio
# async def test_handle_function_called_with_args():
#     mock_fn = Mock(return_value=Future())
#     mock_fn.return_value.set_result(None)
#     timeout = 1
#     name = 'timer_name'
#     args = (1, 2, 3)
#     kwargs = {"a": 1}
#     timer = Timer(timeout, mock_fn, name, *args, **kwargs)

#     await timer.handle_function()
#     await asyncio.sleep(timeout)
#     assert timer.task is not None # task is reset in the handle_function
#     timer.cancel()

#     assert mock_fn.assert_called_once_with(*args, **kwargs)

