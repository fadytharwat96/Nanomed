from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FamilyProfileModel(Base):
    __tablename__ = "family_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    relation: Mapped[str] = mapped_column(String(20))
    chronic_conditions: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
