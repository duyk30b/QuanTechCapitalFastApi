import os

from fastapi import HTTPException

from app.mongo.models.setting_model import SettingKey
from app.mongo.repositories.setting_repository import setting_repository


class EaMql5Common:
    @staticmethod
    async def get_mt5_folder_path():
        mt5FolderPathSetting = await setting_repository.find_one(
            filter={"key": SettingKey.MT5_FOLDER_PATH}
        )
        mt5FolderPath = (
            str(mt5FolderPathSetting.value) if mt5FolderPathSetting else None
        )
        if not mt5FolderPath:
            raise HTTPException(
                status_code=400, detail="MT5_FOLDER_PATH setting not found"
            )
        return mt5FolderPath

    @staticmethod
    async def get_mql5_folder_path():
        mql5FolderPathSetting = await setting_repository.find_one(
            filter={"key": SettingKey.MQL5_FOLDER_PATH}
        )
        mql5FolderPath = (
            str(mql5FolderPathSetting.value) if mql5FolderPathSetting else None
        )
        if not mql5FolderPath:
            raise HTTPException(
                status_code=400, detail="MQL5_FOLDER_PATH setting not found"
            )
        return mql5FolderPath

    @staticmethod
    def get_ea_mql5_folder_path(mql5FolderPath: str, ea_mql5_id: str):
        eaMql5FolderPath = os.path.join(
            mql5FolderPath, "Experts", "PYTHON_SERVER", ea_mql5_id
        )
        eaMql5ReportFolderPath = os.path.join(eaMql5FolderPath, "Report")
        os.makedirs(eaMql5FolderPath, exist_ok=True)
        os.makedirs(eaMql5ReportFolderPath, exist_ok=True)
        return eaMql5FolderPath
