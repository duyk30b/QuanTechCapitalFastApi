from typing import Any

from app.socket.socket_server import sio


# client emit: "demo:send"
@sio.on("demo:send")  # type: ignore
async def handle_demo_send(sid: str, data: Any) -> None:
    print("Received demo:", data)

    # reply lại client
    await sio.emit("demo:response", {"msg": "hello từ server"}, to=sid)  # type: ignore


# server chủ động emit (function dùng trong code khác)
async def emit_demo() -> None:
    await sio.emit("demo:push", {"msg": "server push"})  # type: ignore
