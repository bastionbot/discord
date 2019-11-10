import asyncio

async def _handle_function(callback, *callback_args, **callback_kwargs):
    """
    This is the function that actually calls the Timer callback.
    I had to do this so I could actually test that the params were passed correctly
    """
    await callback(*callback_args, **callback_kwargs)


class Timer():

    def __init__(self, timeout, callback, name, *callback_args, **callback_kwargs):
        self.timeout = timeout
        self.name = name
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs
        self.task = None

    def start(self):
        # I couldn't test this function :(
        self.task = asyncio.create_task(self.handle_function())

    async def handle_function(self):
        await asyncio.sleep(self.timeout)
        await _handle_function(self.callback, *self.callback_args, **self.callback_kwargs)
        self.start()

    def cancel(self):
        if self.task:
            self.task.cancel()
            return True
        return False


class TrackManager():
    DEFAULT_TIMEOUT = 60 * 60 * 12 # 12 hours

    def __init__(self):
        self.timers = {}
