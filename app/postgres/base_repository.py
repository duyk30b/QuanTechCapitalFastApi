from sqlalchemy.orm import Session
from typing import Any, Generic, TypeVar, Type, List

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_by_id(self, db: Session, id: int) -> T | None:
        return db.get(self.model, id)

    def get_all(self, db: Session) -> List[T]:
        return db.query(self.model).all()

    def get_many(self, db: Session, limit: int = 100) -> List[T]:
        return db.query(self.model).limit(limit).all()

    def create(self, db: Session, data: dict[str, Any]) -> T:
        obj = self.model(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, id: int, data: dict[str, Any]) -> T | None:
        obj = db.get(self.model, id)
        if not obj:
            return None
        for k, v in data.items():
            setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int) -> bool:
        obj = db.get(self.model, id)
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
