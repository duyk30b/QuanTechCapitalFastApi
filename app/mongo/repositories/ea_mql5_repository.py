from app.mongo.models.ea_mql5_model import (
    EaMql5CreateSchema,
    EaMql5FilterSchema,
    EaMql5Model,
    EaMql5SortSchema,
    EaMql5UpdateSchema,
)
from app.mongo.mongo_repository import MongoRepository


class EaMql5Repository(
    MongoRepository[
        EaMql5Model,
        EaMql5CreateSchema,
        EaMql5UpdateSchema,
        EaMql5FilterSchema,
        EaMql5SortSchema,
    ]
):
    def __init__(self):
        super().__init__(EaMql5Model)


ea_mql5_repository = EaMql5Repository()
