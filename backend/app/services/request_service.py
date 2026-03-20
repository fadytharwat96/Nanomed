from datetime import datetime
from math import atan2, cos, radians, sin, sqrt
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.nurse import NurseStatusModel
from app.models.profile import FamilyProfileModel
from app.models.request import ServiceRequestModel
from app.schemas.request import ServiceRequest, ServiceRequestIn
from app.services.utils import split_csv


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    earth_radius = 6371.0

    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)

    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c


def create_request(db: Session, *, user_id: str, payload: ServiceRequestIn) -> ServiceRequest:
    profile = db.get(FamilyProfileModel, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile.account_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot create request for another account profile")

    service_request = ServiceRequestModel(
        id=str(uuid4()),
        created_at=datetime.utcnow(),
        profile_id=payload.profile_id,
        service_type=payload.service_type,
        address_text=payload.address_text,
        lat=payload.lat,
        lng=payload.lng,
        notes=payload.notes,
        status="pending",
    )

    candidate_rows = db.scalars(select(NurseStatusModel).where(NurseStatusModel.online.is_(True))).all()
    candidates = [
        (n.nurse_id, haversine_km(payload.lat, payload.lng, n.lat, n.lng))
        for n in candidate_rows
        if payload.service_type in split_csv(n.skills)
    ]

    if candidates:
        service_request.assigned_nurse_id = min(candidates, key=lambda item: item[1])[0]
        service_request.status = "assigned"

    db.add(service_request)
    db.commit()
    db.refresh(service_request)
    return map_request(service_request)


def get_request(db: Session, *, user_id: str, request_id: str) -> ServiceRequest:
    req = db.get(ServiceRequestModel, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    profile = db.get(FamilyProfileModel, req.profile_id)
    if not profile or profile.account_id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another account request")

    return map_request(req)


def list_nurse_requests(db: Session, *, nurse_id: str, status: str | None = None) -> list[ServiceRequest]:
    stmt = select(ServiceRequestModel).where(ServiceRequestModel.assigned_nurse_id == nurse_id)
    if status:
        stmt = stmt.where(ServiceRequestModel.status == status)

    rows = db.scalars(stmt.order_by(ServiceRequestModel.created_at.desc())).all()
    return [map_request(row) for row in rows]


def nurse_transition_request(db: Session, *, nurse_id: str, request_id: str, action: str) -> ServiceRequest:
    req = db.get(ServiceRequestModel, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")

    if req.assigned_nurse_id != nurse_id:
        raise HTTPException(status_code=403, detail="Request is not assigned to current nurse")

    transitions = {
        "arrive": ("assigned", "arrived"),
        "start": ("arrived", "in_progress"),
        "complete": ("in_progress", "completed"),
        "reject": ("assigned", "pending"),
    }

    if action not in transitions:
        raise HTTPException(status_code=400, detail="Unsupported action")

    expected, target = transitions[action]
    if req.status != expected:
        raise HTTPException(status_code=409, detail=f"Cannot '{action}' while status is '{req.status}'")

    req.status = target
    if action == "reject":
        req.assigned_nurse_id = None

    db.add(req)
    db.commit()
    db.refresh(req)
    return map_request(req)


def map_request(req: ServiceRequestModel) -> ServiceRequest:
    return ServiceRequest(
        id=req.id,
        profile_id=req.profile_id,
        service_type=req.service_type,
        address_text=req.address_text,
        lat=req.lat,
        lng=req.lng,
        notes=req.notes,
        status=req.status,
        assigned_nurse_id=req.assigned_nurse_id,
        created_at=req.created_at,
    )
