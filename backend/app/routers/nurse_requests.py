from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.request import ServiceRequest
from app.services.request_service import list_nurse_requests, nurse_transition_request

router = APIRouter(prefix="/v1/nurse/requests", tags=["nurse-requests"])


@router.get("", response_model=list[ServiceRequest])
def list_my_requests(
    status: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"nurse", "admin"})),
) -> list[ServiceRequest]:
    return list_nurse_requests(db, nurse_id=current_user.id, status=status)


@router.post("/{request_id}/arrive", response_model=ServiceRequest)
def arrive_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"nurse", "admin"})),
) -> ServiceRequest:
    return nurse_transition_request(db, nurse_id=current_user.id, request_id=request_id, action="arrive")


@router.post("/{request_id}/start", response_model=ServiceRequest)
def start_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"nurse", "admin"})),
) -> ServiceRequest:
    return nurse_transition_request(db, nurse_id=current_user.id, request_id=request_id, action="start")


@router.post("/{request_id}/complete", response_model=ServiceRequest)
def complete_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"nurse", "admin"})),
) -> ServiceRequest:
    return nurse_transition_request(db, nurse_id=current_user.id, request_id=request_id, action="complete")


@router.post("/{request_id}/reject", response_model=ServiceRequest)
def reject_request(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"nurse", "admin"})),
) -> ServiceRequest:
    return nurse_transition_request(db, nurse_id=current_user.id, request_id=request_id, action="reject")
