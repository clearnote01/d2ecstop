import asyncio
from concurrent.futures import Future

class async_view():
    def __init__(self, inner):
        self.inner = inner
        self.event_loop = None
        try:
            self.event_loop = asyncio.get_event_loop()
        except RuntimeError:
            pass

    def __call__(self, *args, **kwargs):
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            pass
        else:
            if self.event_loop.is_running():
                raise RuntimeError('Cannot access the event loop')
        future_val = Future()
        if self.event_loop == None or not self.event_loop.is_running():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.outer(args, kwargs, future_val))
            loop.close()
            asyncio.set_event_loop(self.event_loop)
        else:
            self.event_loop.call_soon_threadsafe(
                    self.event_loop.create_task,
                    self.outer(args, kwargs, future_val)
            )
        return future_val.result()

    async def outer(self, args, kwargs, future_val):
        try:
            result = await self.inner(*args, **kwargs)
        except:
            pass
        else:
            future_val.set_result(result)
