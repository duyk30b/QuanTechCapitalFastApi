from pydantic import BaseModel, Field


class EaMql5ConfigIniBody(BaseModel):
    symbol: str = Field(...)
    period: str = Field(...)
    fromDate: int = Field(...)
    toDate: int = Field(...)
    deposit: float = Field(...)
    currency: str = Field(...)
    leverage: int = Field(...)
    model: int = Field(...)
    optimization: int = Field(...)
    optimizationCriterion: int = Field(...)


class EaMql5UpsertBody(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    mql5Code: str = Field(...)
    configIni: EaMql5ConfigIniBody = Field(...)


class EaMql5RunTestBody(BaseModel):
    configIniText: str = Field(...)
