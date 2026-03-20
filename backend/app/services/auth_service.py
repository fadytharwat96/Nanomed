from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import TokenResponse

OTP_STORE: dict[str, str] = {}
OTP_PLACEHOLDER_CODE = "123456"


def send_otp(phone: str) -> dict[str, str]:
    OTP_STORE[phone] = OTP_PLACEHOLDER_CODE
    return {"message": "OTP generated (placeholder)", "otp_code": OTP_PLACEHOLDER_CODE}


def verify_otp_and_issue_token(
    db: Session,
    *,
    phone: str,
    otp_code: str,
    full_name: str,
    role: str,
) -> TokenResponse:
    expected = OTP_STORE.get(phone)
    if not expected or expected != otp_code:
        raise ValueError("Invalid OTP")

    user = db.scalar(select(User).where(User.phone == phone))
    if not user:
        user = User(id=str(uuid4()), phone=phone, full_name=full_name, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.role != role:
        raise ValueError("Role mismatch for this phone")

    token = create_access_token(subject=user.id, role=user.role)
    return TokenResponse(access_token=token)
