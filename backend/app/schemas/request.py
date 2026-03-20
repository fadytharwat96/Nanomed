from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import RequestStatus, ServiceType


class ServiceRequestIn(BaseModel):
    profile_id: str
    service_type: ServiceType
    address_text: str
    lat: float
    lng: float
    notes: str | None = None


class ServiceRequest(BaseModel):
    id: str
    profile_id: str
    service_type: ServiceType
    address_text: str
    lat: float
    lng: float
    notes: str | None = None
    status: RequestStatus = "pending"
    assigned_nurse_id: str | None = None
    created_at: datetime
