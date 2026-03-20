from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import SendOtpRequest, TokenResponse, VerifyOtpRequest
from app.schemas.user import UserOut
from app.services.auth_service import send_otp, verify_otp_and_issue_token

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/send-otp")
def send_otp_endpoint(payload: SendOtpRequest) -> dict[str, str]:
    return send_otp(payload.phone)


@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp_endpoint(payload: VerifyOtpRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        return verify_otp_and_issue_token(
            db,
            phone=payload.phone,
            otp_code=payload.otp_code,
            full_name=payload.full_name,
            role=payload.role,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut(
        id=current_user.id,
        phone=current_user.phone,
        full_name=current_user.full_name,
        role=current_user.role,
        created_at=current_user.created_at,
    )
