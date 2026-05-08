from typing import Any, cast
import subprocess
import os
import asyncio

from app.api.service_common.service_common import SERVER_EA_FOLDER_NAME, ServiceCommon
from app.core.app_queue import AppQueue, QueueJob

from app.core.exception import BusinessException
from app.mongo.models.setting_model import SettingKey
from app.mongo.repositories.ea_mql5_repository import ea_mql5_repository
from app.utils.time_util import PyTimer


class MT5RunQueue(AppQueue):
    def __init__(self) -> None:
        super().__init__(name="mt5_run_queue_name", maxsize=100)
        super().start()

    async def add(self, data: str, priority: int = 10, max_retries: int = 3) -> None:
        await super().add(data=data, priority=priority, max_retries=max_retries)

    async def execute_job(self, job: QueueJob) -> None:
        eaMql5Id: str = job.data
        settingDict = await ServiceCommon.get_setting_dict()

        mql5FolderPath = cast(str, settingDict.get(SettingKey.MQL5_FOLDER_PATH))
        mt5FolderPath = cast(str, settingDict.get(SettingKey.MT5_FOLDER_PATH))
        mt5Login = cast(str, settingDict.get(SettingKey.MT5_LOGIN))
        mt5Password = cast(str, settingDict.get(SettingKey.MT5_PASSWORD))
        mt5Server = cast(str, settingDict.get(SettingKey.MT5_SERVER))

        eaMql5 = await ea_mql5_repository.find_one_by_id(eaMql5Id)
        if not eaMql5:
            raise BusinessException("EA MQL5 not found")

        eaMql5FolderPath = ServiceCommon.get_ea_mql5_folder_path(
            mql5FolderPath, eaMql5Id
        )

        iniFileName = "config.ini"
        iniFilePath = os.path.join(eaMql5FolderPath, iniFileName)

        configIniText = f"""
[Common]
Login={mt5Login}
Password={mt5Password}
Server={mt5Server}
AutoConfiguration=false

[Tester]
Expert={SERVER_EA_FOLDER_NAME}\\{eaMql5Id}\\{eaMql5Id}.ex5
Symbol={eaMql5.configIni['symbol'] or ''}
Period={eaMql5.configIni['period'] or ''}
FromDate={PyTimer.time_to_text(eaMql5.configIni['fromDate'], 'YYYY.MM.DD') or ''}
ToDate={PyTimer.time_to_text(eaMql5.configIni['toDate'], 'YYYY.MM.DD') or ''}
Deposit={eaMql5.configIni['deposit'] or 0}
Currency={eaMql5.configIni['currency'] or ''}
Leverage={eaMql5.configIni['leverage'] or 0}
Model={eaMql5.configIni['model'] or 0}
Optimization={eaMql5.configIni['optimization'] or 0}
OptimizationCriterion={eaMql5.configIni['optimizationCriterion'] or 0}
ExecutionMode=0
ForwardMode=0
Report=MQL5\\Experts\\{SERVER_EA_FOLDER_NAME}\\{eaMql5Id}\\Report\\report
ReplaceReport=1
ShutdownTerminal=true
Visual=false

[TesterInputs]
lot=0.1||0.1||0.1||1.000000||Y
"""

        with open(iniFilePath, "w", encoding="utf-8") as f:
            f.write(configIniText)

        mt5_terminal_path = os.path.join(mt5FolderPath, "terminal64.exe")

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
            raise BusinessException(f"Run test failed: {str(e)}")


mt5_run_queue = MT5RunQueue()
