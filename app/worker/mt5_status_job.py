import asyncio

from app.module.mt5_module import mt5_module
from app.socket.handlers.mt5_handler import SocketMt5Handler


class Mt5StatusJob:
    def __init__(self):
        self._task: asyncio.Task[None] | None = None
        self._interval_seconds = 2

    async def _run(self):
        while True:
            process_status = mt5_module.get_proc_status()
            await SocketMt5Handler.emit_mt5_status(data=process_status)
            await asyncio.sleep(self._interval_seconds)

    async def start(self):
        if self._task is not None and not self._task.done():
            return
        self._task = asyncio.create_task(self._run(), name="mt5_status_job")

    async def stop(self):
        if self._task is None:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        finally:
            self._task = None
