import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.api_user.api_user_request import UserCreateBody, UserUpdateBody
from app.api.api_user.api_user_response import (
    UserCreateResponse,
    UserListResponse,
    UserUpdateResponse,
)
from app.core.security import hash_password
from app.postgres.entities.user_entity import UserEntity
from app.postgres.postgres_connection import pgConn
from app.redis.cache.user_data_cache import userDataCache
from app.redis.cache.user_login_cache import userLoginCache

user_controller = APIRouter(prefix="/user", tags=["User"])


@user_controller.get("/pagination")
async def user_pagination():
    return {"message": "pagination of User"}


@user_controller.get("/list", response_model=UserListResponse)
async def user_list(
    skip: int = 0, limit: int = 10, db: Session = Depends(pgConn.get_db)
):
    user_list = db.query(UserEntity).offset(skip).limit(limit).all()
    return {"userList": user_list}


@user_controller.get("/detail")
async def user_detail(user_id: int, db: Session = Depends(pgConn.get_db)):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_controller.post("/create", response_model=UserCreateResponse)
async def user_create(body: UserCreateBody, db: Session = Depends(pgConn.get_db)):
    existed = (
        db.query(UserEntity)
        .filter(UserEntity.username == body.account.username)
        .first()
    )
    if existed:
        raise HTTPException(status_code=400, detail="Username already exists")

    nowTimestamp = int(time.time() * 1000)

    user = UserEntity(
        full_name=body.user.fullName,
        username=body.account.username,
        password_hash=hash_password(
            body.account.password
        ),  # In production, hash the password!
        user_type=body.user.userType,
        is_active=body.user.isActive,
        created_at=nowTimestamp,  # Set this to the current timestamp
        updated_at=nowTimestamp,  # Set this to the current timestamp
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    await userDataCache.set_user(
        {
            "id": user.id,
            "userType": user.userType,
            "isActive": user.isActive,
        }
    )

    return {"user": user}


@user_controller.post("/update/{user_id}", response_model=UserUpdateResponse)
async def user_update(
    user_id: int, body: UserUpdateBody, db: Session = Depends(pgConn.get_db)
):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.fullName = body.user.fullName or user.fullName
    user.username = body.account.username if body.account else user.username
    user.passwordHash = (
        hash_password(body.account.password) if body.account else user.passwordHash
    )
    user.userType = body.user.userType or user.userType
    user.isActive = body.user.isActive or user.isActive
    user.updatedAt = int(time.time() * 1000)

    db.commit()
    db.refresh(user)

    await userDataCache.set_user(
        {
            "id": user.id,
            "userType": user.userType,
            "isActive": user.isActive,
        }
    )

    return {"user": user}


@user_controller.post("/delete/{user_id}")
async def user_delete(user_id: int, db: Session = Depends(pgConn.get_db)):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    await userDataCache.delete_user(user.id)

    return {"message": "User deleted successfully"}


@user_controller.post("/force-logout/{user_id}")
async def user_force_logout(
    user_id: int,
):
    await userLoginCache.logout_all(user_id)
    return {
        "message": f"Force-logged out user {user_id}",
    }
