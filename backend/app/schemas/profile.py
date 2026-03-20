from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import RelationType


class FamilyProfileIn(BaseModel):
    full_name: str
    relation: RelationType
    chronic_conditions: list[str] = Field(default_factory=list)


class FamilyProfile(BaseModel):
    id: str
    account_id: str
    full_name: str
    relation: RelationType
    chronic_conditions: list[str]
    created_at: datetime
