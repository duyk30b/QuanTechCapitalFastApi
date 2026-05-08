from typing import Any

from fastapi import APIRouter, Depends

from app.api.api_ea_mql5.ea_mql5_service import EaMql5Service
from app.api.api_ea_mql5.ea_mql5_request import (
    EaMql5RunTestBody,
    EaMql5UpsertBody,
)
from app.api.api_ea_mql5.service.ea_mql5_compile import EaMql5Compile
from app.api.api_ea_mql5.service.ea_mql5_run_test import EaMql5RunTest
from app.depends.request_depends import RequestDepends, RequestState

ea_mql5_controller = APIRouter(prefix="/ea_mql5", tags=["ea_mql5"])
ea_mql5_compile = EaMql5Compile()
ea_mql5_service = EaMql5Service()
ea_mql5_run_test = EaMql5RunTest()


@ea_mql5_controller.get("/pagination")
async def ea_mql5_pagination(page: int, limit: int) -> dict[str, Any]:
    return await ea_mql5_service.ea_mql5_pagination(page=page, limit=limit)


@ea_mql5_controller.get("/list")
async def ea_mql5_list() -> dict[str, list[Any]]:
    return await ea_mql5_service.ea_mql5_list()


@ea_mql5_controller.get("/detail/{ea_mql5_id}")
async def ea_mql5_detail(ea_mql5_id: str) -> dict[str, Any]:
    data = await ea_mql5_service.ea_mql5_detail(ea_mql5_id=ea_mql5_id)
    return data


@ea_mql5_controller.post("/create")
async def ea_mql5_create(
    body: EaMql5UpsertBody,
    state: RequestState = Depends(RequestDepends.state),
) -> dict[str, Any]:
    data = await ea_mql5_service.ea_mql5_create(body, state)
    return data


@ea_mql5_controller.post("/update/{ea_mql5_id}")
async def ea_mql5_update(
    ea_mql5_id: str,
    body: EaMql5UpsertBody,
    state: RequestState = Depends(RequestDepends.state),
) -> dict[str, Any]:
    data = await ea_mql5_service.ea_mql5_update(ea_mql5_id, body, state)
    return data


@ea_mql5_controller.post("/destroy/{ea_mql5_id}")
async def ea_mql5_destroy(
    ea_mql5_id: str, state: RequestState = Depends(RequestDepends.state)
) -> dict[str, Any]:
    data = await ea_mql5_service.ea_mql5_destroy(ea_mql5_id=ea_mql5_id)
    return data


@ea_mql5_controller.post("/start-compile/{ea_mql5_id}")
async def ea_mql5_compile_and_save(ea_mql5_id: str) -> dict[str, Any]:
    data = await ea_mql5_compile.start_compile(ea_mql5_id)
    return data


@ea_mql5_controller.post("/start-run-test/{ea_mql5_id}")
async def ea_mql5_start_run_test(
    ea_mql5_id: str, body: EaMql5RunTestBody
) -> dict[str, Any]:
    data = await ea_mql5_run_test.start_run_test(ea_mql5_id=ea_mql5_id, body=body)
    return data


@ea_mql5_controller.post("/stop-run-test/{ea_mql5_id}")
async def ea_mql5_stop_run_test(ea_mql5_id: str) -> dict[str, Any]:
    data = await ea_mql5_run_test.ea_mql5_stop_run_test(ea_mql5_id=ea_mql5_id)
    return data
