import os

from fastapi import HTTPException

from app.mongo.models.setting_model import SettingKey
from app.mongo.repositories.setting_repository import setting_repository

SERVER_EA_FOLDER_NAME = "PYTHON_SERVER"


class ServiceCommon:
    @staticmethod
    async def get_setting_dict():
        settings = await setting_repository.find_many()
        return {setting.key: setting.value for setting in settings}

    @staticmethod
    def get_ea_mql5_folder_path(mql5FolderPath: str, eaMql5Id: str):
        eaMql5FolderPath = os.path.join(
            mql5FolderPath, "Experts", SERVER_EA_FOLDER_NAME, eaMql5Id
        )
        eaMql5ReportFolderPath = os.path.join(eaMql5FolderPath, "Report")
        os.makedirs(eaMql5FolderPath, exist_ok=True)
        os.makedirs(eaMql5ReportFolderPath, exist_ok=True)
        return eaMql5FolderPath
