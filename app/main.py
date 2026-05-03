from contextlib import asynccontextmanager
import asyncio
import logging
import socketio
from app.core.exception import AppExceptionHandler
from app.core.middleware import AppMiddleware
from app.socket.socket_server import sio
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_auth.auth_controller import auth_controller
from app.api.api_ea_mql5.ea_mql5_controller import ea_mql5_controller
from app.api.api_me.me_controller import me_controller
from app.api.api_setting.setting_controller import setting_controller
from app.api.api_user.api_user_controller import user_controller
from app.api.api_role.role_controller import role_controller
from app.api.api_user_role.user_role_controller import user_role_controller
from app.mongo.mongo_connection import mongodb
from app.postgres.postgres_connection import pgConn
from app.redis.redis_connection import redisConnection
from app.worker.worker import AppWorker
import app.socket.socket_events  # register socket handlers
from app.core.logger import ColorFormatter

logger = logging.getLogger(__name__)
app_worker = AppWorker()


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        logger.debug("Connecting PostgreSQL, MongoDB, and Redis...")
        await asyncio.gather(
            pgConn.connect(),
            mongodb.connect(),
            redisConnection.connect(),
        )
        logger.debug("Successfully connected to PostgreSQL, MongoDB, and Redis.")
        await app_worker.start()
    except Exception as exc:
        logger.error(
            f"Application startup failed: {type(exc).__module__}.{type(exc).__name__}: {str(exc)}"
        )
        # traceback.print_exception(exc, limit=-3)
        raise RuntimeError(str(exc)) from None

    yield

    await app_worker.stop()

    await asyncio.gather(
        mongodb.close(),
        redisConnection.close(),
    )
    pgConn.close()


app = FastAPI(lifespan=lifespan)


app.add_middleware(AppMiddleware)
# CORSMiddleware cần khai báo cuối cùng, để cho client đọc response, bất kể statusCode là gì
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost:5174",
    #     "http://127.0.0.1:5174",
    #     "http://192.168.1.21:5174",
    # ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(setting_controller)
app.include_router(auth_controller)
app.include_router(me_controller)
app.include_router(user_controller)
app.include_router(role_controller)
app.include_router(user_role_controller)
app.include_router(ea_mql5_controller)

app.add_exception_handler(RequestValidationError, AppExceptionHandler.build_response)


@app.get("/")
async def root():
    return {"message": "Hello World"}


socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
