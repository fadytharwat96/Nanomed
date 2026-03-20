from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.profile import FamilyProfileModel
from app.schemas.profile import FamilyProfile, FamilyProfileIn
from app.services.utils import join_csv, split_csv


def create_profile(db: Session, *, user_id: str, payload: FamilyProfileIn) -> FamilyProfile:
    profile = FamilyProfileModel(
        id=str(uuid4()),
        created_at=datetime.utcnow(),
        account_id=user_id,
        full_name=payload.full_name,
        relation=payload.relation,
        chronic_conditions=join_csv(payload.chronic_conditions),
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return FamilyProfile(
        id=profile.id,
        account_id=profile.account_id,
        full_name=profile.full_name,
        relation=profile.relation,
        chronic_conditions=split_csv(profile.chronic_conditions),
        created_at=profile.created_at,
    )


def list_profiles(db: Session, *, user_id: str) -> list[FamilyProfile]:
    rows = db.scalars(select(FamilyProfileModel).where(FamilyProfileModel.account_id == user_id)).all()
    return [
        FamilyProfile(
            id=row.id,
            account_id=row.account_id,
            full_name=row.full_name,
            relation=row.relation,
            chronic_conditions=split_csv(row.chronic_conditions),
            created_at=row.created_at,
        )
        for row in rows
    ]
