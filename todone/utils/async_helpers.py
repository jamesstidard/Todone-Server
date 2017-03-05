import asyncio


def wait(coroutine):
    asyncio.get_event_loop().run_until_complete(coroutine)
