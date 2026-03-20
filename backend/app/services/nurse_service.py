from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.nurse import NurseStatusModel
from app.schemas.nurse import NurseStatus
from app.services.utils import split_csv


def list_online_nurses(db: Session, service_type: str | None = None) -> list[NurseStatus]:
    rows = db.scalars(select(NurseStatusModel).where(NurseStatusModel.online.is_(True))).all()
    nurses = [
        NurseStatus(
            nurse_id=row.nurse_id,
            full_name=row.full_name,
            lat=row.lat,
            lng=row.lng,
            online=row.online,
            skills=split_csv(row.skills),
        )
        for row in rows
    ]

    if service_type:
        nurses = [n for n in nurses if service_type in n.skills]
    return nurses
