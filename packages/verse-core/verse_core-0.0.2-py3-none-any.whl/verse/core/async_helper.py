import asyncio


class AsyncHelper:
    @classmethod
    def to_async(cls, func, *args, **kwargs):
        return asyncio.to_thread(func, *args, **kwargs)
