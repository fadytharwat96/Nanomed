from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import RoleType


class UserOut(BaseModel):
    id: str
    phone: str
    full_name: str
    role: RoleType
    created_at: datetime
