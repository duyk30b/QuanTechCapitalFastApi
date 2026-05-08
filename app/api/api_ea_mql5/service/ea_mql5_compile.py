from typing import Any, cast

from fastapi import HTTPException
from app.api.service_common.service_common import ServiceCommon
from app.mongo.models.ea_mql5_model import EaMql5Model, EaMql5Status
from app.mongo.models.setting_model import SettingKey
from app.mongo.repositories.ea_mql5_repository import ea_mql5_repository
import subprocess
import os
import asyncio


class EaMql5Compile:
    def __init__(self):
        pass

    async def start_compile(self, ea_mql5_id: str) -> dict[str, Any]:
        settingDict = await ServiceCommon.get_setting_dict()
        mqlFolderPath = cast(str, settingDict.get(SettingKey.MQL5_FOLDER_PATH))
        mt5FolderPath = cast(str, settingDict.get(SettingKey.MT5_FOLDER_PATH))

        eaMql5 = await ea_mql5_repository.find_one_by_id(ea_mql5_id)
        if not eaMql5:
            raise HTTPException(status_code=404, detail="EA MQL5 not found")
        mql5Code = eaMql5.mql5Code

        eaMql5FolderPath = ServiceCommon.get_ea_mql5_folder_path(
            mqlFolderPath, ea_mql5_id
        )

        mq5FilePath = os.path.join(eaMql5FolderPath, f"{eaMql5.id}.mq5")
        with open(mq5FilePath, "w", encoding="utf-8") as f:
            f.write(mql5Code)

        metaEditorPath = os.path.join(mt5FolderPath, "MetaEditor64.exe")
        logCompileFilePath = os.path.join(eaMql5FolderPath, f"{eaMql5.id}_compile.log")

        command = [
            metaEditorPath,
            f"/compile:{mq5FilePath}",
            f"/log:{logCompileFilePath}",
        ]
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                command,
                capture_output=True,
                text=True,
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Compile failed to start: {str(e)}"
            )

        if not os.path.exists(logCompileFilePath):
            raise HTTPException(status_code=400, detail="Log file not found")

        with open(logCompileFilePath, "r", encoding="utf-16", errors="ignore") as f:
            log_lines = f.readlines()

        importantLogs: list[str] = []
        compileSuccess = False
        for line in log_lines:
            line = line.strip()
            if (
                "error" in line.lower()
                or "warning" in line.lower()
                or "result" in line.lower()
                or "failed" in line.lower()
                or "success" in line.lower()
            ):
                importantLogs.append(line)

            if "Result: 0 errors" in line:
                compileSuccess = True

        ex5Path = mq5FilePath.replace(".mq5", ".ex5")
        compiledFileExists = os.path.exists(ex5Path)

        compileSuccess = compileSuccess and compiledFileExists

        eaMql5Modified: EaMql5Model | None = None
        if compileSuccess:
            eaMql5Modified = await ea_mql5_repository.update_one_by_id(
                ea_mql5_id,
                {"status": EaMql5Status.Compiled},
            )

        return {
            "compileSuccess": compileSuccess,
            "eaMql5": eaMql5Modified.to_response() if eaMql5Modified else None,
            "eaMql5FolderPath": eaMql5FolderPath,
            "logs": importantLogs,
        }
