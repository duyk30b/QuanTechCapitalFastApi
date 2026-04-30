from typing import Any, Optional, Dict, Union
from pydantic import BaseModel, field_validator, ConfigDict
import json


class GetQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    limit: int
    relation: Optional[Dict[str, Any]] = None
    filter: Optional[Dict[str, Any]] = None
    sort: Optional[Dict[str, Any]] = None

    @field_validator("page")
    @classmethod
    def validate_page(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("page must be > 0")
        return v

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: int) -> int:
        if v <= 0 or v > 100:
            raise ValueError("limit must be between 1 and 100")
        return v

    @field_validator("relation", "filter", "sort", mode="before")
    @classmethod
    def parse_json(cls, v: Any) -> Union[Dict[str, Any], None]:
        if v is None:
            return None

        if isinstance(v, dict):
            return v

        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError as e:
                raise ValueError("Must be valid JSON string") from e

        raise ValueError("Invalid type for JSON field")
