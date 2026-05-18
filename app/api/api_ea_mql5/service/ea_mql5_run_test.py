import logging
from typing import Any, cast
import subprocess
import os
import asyncio

from app.api.api_ea_mql5.ea_mql5_request import EaMql5RunTestBody
from app.api.service_common.service_common import ServiceCommon
from app.core.exception import BusinessException
from app.mongo.models.setting_model import SettingKey
from app.mongo.repositories.ea_mql5_repository import ea_mql5_repository
from app.worker.mt5_status_job.mt5_run_queue import mt5_run_queue

logger = logging.getLogger(__name__)


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

    async def start_run_test_old(
        self, ea_mql5_id: str, body: EaMql5RunTestBody
    ) -> dict[str, Any]:
        eaMql5Id: str = ea_mql5_id
        settingDict = await ServiceCommon.get_setting_dict()

        mql5FolderPath = cast(str, settingDict.get(SettingKey.MQL5_FOLDER_PATH))
        mt5FolderPath = cast(str, settingDict.get(SettingKey.MT5_FOLDER_PATH))
        mt5Login = cast(str, settingDict.get(SettingKey.MT5_LOGIN))
        mt5Password = cast(str, settingDict.get(SettingKey.MT5_PASSWORD))
        mt5Server = cast(str, settingDict.get(SettingKey.MT5_SERVER))

        eaMql5 = await ea_mql5_repository.find_one_by_id(ea_mql5_id)
        if not eaMql5:
            raise BusinessException("EA MQL5 not found")

        eaMql5FolderPath = ServiceCommon.get_ea_mql5_folder_path(
            mql5FolderPath, ea_mql5_id
        )

        iniFileName = "config.ini"
        iniFilePath = os.path.join(eaMql5FolderPath, iniFileName)
        with open(iniFilePath, "w", encoding="utf-8") as f:
            f.write(body.configIniText)

        logger.info(f"Config INI written to {iniFilePath}")

        mt5_terminal_path = os.path.join(mt5FolderPath, "terminal64.exe")

        command = [
            mt5_terminal_path,
            f"/config:{iniFilePath}",
        ]
        try:
            result = await asyncio.to_thread(
                subprocess.run, command, capture_output=True, text=True
            )

            logger.info(f"MT5 process completed with return code {result.returncode}")

            if result.returncode != 0:
                logger.error(f"MT5 process failed with error: {result.stderr}")
                raise Exception(f"MT5 failed: {result.stderr}")
        except Exception as e:
            logger.error(f"Run test failed: {str(e)}")
            raise BusinessException(f"Run test failed: {str(e)}")

        return {
            "eaMql5Id": ea_mql5_id,
        }
