from typing import Any

from app.api.api_ea_mql5.ea_mql5_request import EaMql5RunTestBody
from app.worker.mt5_status_job.mt5_run_queue import mt5_run_queue


class EaMql5RunTest:
    def __init__(self):
        pass

    async def start_run_test(
        self, ea_mql5_id: str, body: EaMql5RunTestBody
    ) -> dict[str, Any]:
        await mt5_run_queue.add(data=ea_mql5_id)
        return {"message": "Run test started"}

    async def ea_mql5_stop_run_test(self, ea_mql5_id: str) -> dict[str, Any]:
        await mt5_run_queue.remove(ea_mql5_id)
        return {"message": "Run test stopped"}
