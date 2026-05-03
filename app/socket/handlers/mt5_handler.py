from typing import Any

from app.module.mt5_module import Mt5ProcessStatus
from app.socket.socket_constants import SocketMessage
from app.socket.socket_server import sio


class SocketMt5Handler:
    @staticmethod
    async def emit_mt5_status(data: Mt5ProcessStatus) -> None:
        await sio.emit(  # type: ignore
            SocketMessage.SOCKET_MT5_STATUS,
            {
                "name": data["name"],
                "pid": data["pid"],
                "cpuPercent": data["cpu_percent"],
                "memoryMb": data["memory_mb"],
            },
        )
