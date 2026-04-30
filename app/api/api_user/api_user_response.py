from typing import List

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    fullName: str
    username: str
    userType: int
    isActive: int
    createdAt: int
    updatedAt: int


class UserListResponse(BaseModel):
    userList: List[UserResponse]


class UserCreateResponse(BaseModel):
    user: UserResponse


class UserUpdateResponse(BaseModel):
    user: UserResponse
