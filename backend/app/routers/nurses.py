from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.schemas.nurse import NurseStatus
from app.services.nurse_service import list_online_nurses

router = APIRouter(prefix="/v1/nurses", tags=["nurses"])


@router.get("/online", response_model=list[NurseStatus])
def list_online_nurses_endpoint(
    service_type: str | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_roles({"patient", "nurse", "admin"})),
) -> list[NurseStatus]:
    return list_online_nurses(db, service_type=service_type)
