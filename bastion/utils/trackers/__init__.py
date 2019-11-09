import asyncio

class Timer():

    def __init__(self, timeout, callback, name, *callback_args, **callback_kwargs):
        self.timeout = timeout
        self.name = name
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs
        self.task = None

    def start(self):
        self.task = asyncio.ensure_future(self.handle_function())

    async def handle_function(self):
        await asyncio.sleep(self.timeout)
        await self.callback(*self.callback_args, **self.callback_kwargs)
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
