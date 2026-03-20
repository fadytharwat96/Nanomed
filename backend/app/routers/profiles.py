from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.profile import FamilyProfile, FamilyProfileIn
from app.services.profile_service import create_profile, list_profiles

router = APIRouter(prefix="/v1/profiles", tags=["profiles"])


@router.post("", response_model=FamilyProfile)
def create_profile_endpoint(
    payload: FamilyProfileIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"patient", "admin"})),
) -> FamilyProfile:
    return create_profile(db, user_id=current_user.id, payload=payload)


@router.get("", response_model=list[FamilyProfile])
def list_profiles_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles({"patient", "admin"})),
) -> list[FamilyProfile]:
    return list_profiles(db, user_id=current_user.id)
