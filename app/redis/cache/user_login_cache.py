from app.redis.redis_base import RedisBase


def _key_user_login(userId: int) -> str:
    return f"user:{userId}:login"


class UserLoginCache(RedisBase):
    def __init__(self) -> None:
        super().__init__()

    async def login(self, userId: int, clientId: str) -> None:
        await self._set_add(_key_user_login(userId), clientId)

    async def logout(self, userId: int, clientId: str) -> None:
        await self._set_remove(_key_user_login(userId), clientId)

    async def logout_all(self, userId: int) -> None:
        await self._set_remove_all(_key_user_login(userId))

    async def check_client(self, userId: int, clientId: str) -> bool:
        return await self._set_is_member(_key_user_login(userId), clientId)


userLoginCache = UserLoginCache()
