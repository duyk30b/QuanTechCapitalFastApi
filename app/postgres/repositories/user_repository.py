# app/repositories/user_repository.py
from sqlalchemy.orm import Session

from app.postgres.base_repository import BaseRepository
from app.postgres.entities.user_entity import UserEntity


class UserRepository(BaseRepository[UserEntity]):
    def __init__(self):
        super().__init__(UserEntity)
