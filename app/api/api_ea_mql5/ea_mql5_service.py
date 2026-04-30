from calendar import c
import shutil
from typing import Any

from fastapi import HTTPException

from app.api.api_ea_mql5.ea_mql5_request import EaMql5UpsertBody
from app.api.api_ea_mql5.service.ea_mql5_common import EaMql5Common
from app.depends.request_depends import RequestState
from app.mongo.models.ea_mql5_model import EaMql5CreateSchema, EaMql5Status
from app.mongo.repositories.ea_mql5_repository import ea_mql5_repository
import os


class EaMql5Service:
    def __init__(self):
        pass

    async def ea_mql5_pagination(self, page: int, limit: int) -> dict[str, Any]:
        result = await ea_mql5_repository.pagination(page=page, limit=limit)
        return {
            "eaMql5List": [ea_mql5.to_response() for ea_mql5 in result.data],
            "total": result.total,
            "limit": result.limit,
            "page": result.page,
        }

    async def ea_mql5_list(self) -> dict[str, Any]:
        result = await ea_mql5_repository.list()
        return {"eaMql5List": [ea_mql5.to_response() for ea_mql5 in result]}

    async def ea_mql5_detail(self, ea_mql5_id: str) -> dict[str, Any]:
        ea_mql5 = await ea_mql5_repository.find_one_by_id(ea_mql5_id)
        if not ea_mql5:
            return {"eaMql5": None}

        return {"eaMql5": ea_mql5.to_response() if ea_mql5 else None}

    async def ea_mql5_create(
        self,
        body: EaMql5UpsertBody,
        state: RequestState,
    ) -> dict[str, Any]:
        userId = state["userId"] or 0

        id = await ea_mql5_repository.insert_one(
            EaMql5CreateSchema(
                name=body.name,
                description=body.description,
                mql5Code=body.mql5Code,
                userId=userId,
                status=EaMql5Status.Init,
                configIni={
                    "symbol": body.configIni.symbol,
                    "period": body.configIni.period,
                    "fromDate": body.configIni.fromDate,
                    "toDate": body.configIni.toDate,
                    "deposit": body.configIni.deposit,
                    "currency": body.configIni.currency,
                    "leverage": body.configIni.leverage,
                    "model": body.configIni.model,
                    "optimization": body.configIni.optimization,
                    "optimizationCriterion": body.configIni.optimizationCriterion,
                },
            )
        )
        eaMql5 = await ea_mql5_repository.find_one_by_id(id)
        return {"eaMql5": eaMql5.to_response() if eaMql5 else None}

    async def ea_mql5_update(
        self, ea_mql5_id: str, body: EaMql5UpsertBody, state: RequestState
    ) -> dict[str, Any]:
        userId = state["userId"] or 0
        eaMql5 = await ea_mql5_repository.update_one_by_id(
            ea_mql5_id,
            {
                "name": body.name,
                "description": body.description,
                "mql5Code": body.mql5Code,
                "userId": userId,
                "status": EaMql5Status.Init,
                "configIni": {
                    "symbol": body.configIni.symbol,
                    "period": body.configIni.period,
                    "fromDate": body.configIni.fromDate,
                    "toDate": body.configIni.toDate,
                    "deposit": body.configIni.deposit,
                    "currency": body.configIni.currency,
                    "leverage": body.configIni.leverage,
                    "model": body.configIni.model,
                    "optimization": body.configIni.optimization,
                    "optimizationCriterion": body.configIni.optimizationCriterion,
                },
            },
        )
        return {"eaMql5": eaMql5.to_response() if eaMql5 else None}

    async def ea_mql5_destroy(
        self,
        ea_mql5_id: str,
    ) -> dict[str, Any]:
        mqlFolderPath = await EaMql5Common.get_mql5_folder_path()
        eaMql5FolderPath = EaMql5Common.get_ea_mql5_folder_path(
            mqlFolderPath, ea_mql5_id
        )
        if os.path.isdir(eaMql5FolderPath):
            try:
                shutil.rmtree(eaMql5FolderPath)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to delete EA MQL5 folder: {str(e)}",
                )

        deleted_count = await ea_mql5_repository.delete(ea_mql5_id)

        return {"eaMql5Id": ea_mql5_id, "deletedCount": deleted_count}

    async def ea_mql5_stop_run_test(self, ea_mql5_id: str) -> dict[str, Any]:
        # Placeholder for logic to stop running a test for the specified EA MQL5 item
        return {
            "message": f"Stopped running test for EA MQL5 item with ID: {ea_mql5_id}"
        }
