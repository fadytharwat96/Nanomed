from pydantic import BaseModel, Field

from app.schemas.common import ServiceType


class NurseStatus(BaseModel):
    nurse_id: str
    full_name: str
    lat: float
    lng: float
    online: bool = True
    skills: list[ServiceType] = Field(default_factory=list)
