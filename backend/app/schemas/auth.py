from pydantic import BaseModel, Field

from app.schemas.common import RoleType


class SendOtpRequest(BaseModel):
    phone: str = Field(..., min_length=8, max_length=20)


class VerifyOtpRequest(BaseModel):
    phone: str = Field(..., min_length=8, max_length=20)
    otp_code: str = Field(..., min_length=4, max_length=10)
    full_name: str
    role: RoleType


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    role: RoleType
    exp: int
