from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.request import ServiceRequest, ServiceRequestIn
from app.services.request_service import create_request, get_request

router = APIRouter(prefix="/v1/requests", tags=["requests"])


@router.post("", response_model=ServiceRequest)
def create_request_endpoint(
    payload: ServiceRequestIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"patient", "admin"})),
) -> ServiceRequest:
    return create_request(db, user_id=current_user.id, payload=payload)


@router.get("/{request_id}", response_model=ServiceRequest)
def get_request_endpoint(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"patient", "admin"})),
) -> ServiceRequest:
    return get_request(db, user_id=current_user.id, request_id=request_id)
