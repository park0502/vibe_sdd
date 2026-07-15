from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("title must not be empty")
        return normalized


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    completed: Optional[bool] = None


class TodoOut(TodoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool
