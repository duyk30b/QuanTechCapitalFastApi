from codeop import Compile
from enum import IntEnum
from typing import ClassVar, Optional, TypedDict

from alembic import config

from app.mongo.mongo_model import (
    MongoCreateSchema,
    MongoFilterSchema,
    MongoModel,
    MongoSortSchema,
    MongoUpdateSchema,
)


class EaMql5Status(IntEnum):
    Init = 0
    Compiled = 1
    Testing = 2
    Finished = 3


class EaConfigIni(TypedDict, total=True):
    symbol: str
    period: str
    fromDate: int
    toDate: int
    deposit: float
    currency: str
    leverage: int
    model: int
    optimization: int
    optimizationCriterion: int


class EaMql5Model(MongoModel):
    collection_name: ClassVar[str] = "ea_mql5"
    indexes: ClassVar = [
        {"keys": [("name", 1)], "unique": True},
        {"keys": [("mql5_code", 1)]},
    ]

    name: str
    description: str
    mql5Code: str
    userId: int
    status: EaMql5Status
    configIni: EaConfigIni


class EaMql5CreateSchema(MongoCreateSchema):
    name: str
    description: str
    mql5Code: str
    userId: int
    status: EaMql5Status
    configIni: EaConfigIni


class EaMql5UpdateSchema(MongoUpdateSchema, total=False):
    name: str
    description: str
    mql5Code: str
    userId: int
    status: EaMql5Status
    configIni: EaConfigIni


class EaMql5FilterSchema(MongoFilterSchema, total=False):
    name: Optional[str]
    userId: Optional[int]
    status: Optional[EaMql5Status]


class EaMql5SortSchema(MongoSortSchema, total=False):
    name: Optional[int]  # 1 for ascending, -1 for descending
    userId: Optional[int]
