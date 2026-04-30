from typing import Any
from unittest import result

from fastapi import HTTPException

from app.api.api_ea_mql5.ea_mql5_request import EaMql5RunTestBody
from app.api.api_ea_mql5.service.ea_mql5_common import EaMql5Common
from app.mongo.repositories.ea_mql5_repository import ea_mql5_repository
import subprocess
import os
import asyncio


class EaMql5RunTest:
    def __init__(self):
        pass

    async def start_run_test(
        self, ea_mql5_id: str, body: EaMql5RunTestBody
    ) -> dict[str, Any]:
        mql5Path = await EaMql5Common.get_mql5_folder_path()
        mt5Path = await EaMql5Common.get_mt5_folder_path()

        eaMql5 = await ea_mql5_repository.find_one_by_id(ea_mql5_id)
        if not eaMql5:
            raise HTTPException(status_code=404, detail="EA MQL5 not found")

        eaMql5FolderPath = EaMql5Common.get_ea_mql5_folder_path(mql5Path, ea_mql5_id)

        iniFileName = "config.ini"
        iniFilePath = os.path.join(eaMql5FolderPath, iniFileName)
        with open(iniFilePath, "w", encoding="utf-8") as f:
            f.write(body.configIniText)

        mt5_terminal_path = os.path.join(mt5Path, "terminal64.exe")

        command = [
            mt5_terminal_path,
            f"/config:{iniFilePath}",
        ]
        try:
            result = await asyncio.to_thread(
                subprocess.run, command, capture_output=True, text=True
            )

            if result.returncode != 0:
                raise Exception(f"MT5 failed: {result.stderr}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Run test failed: {str(e)}")

        return {
            "eaMql5Id": ea_mql5_id,
        }
