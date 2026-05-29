from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    role: str
    mobile: str = Field(
        ...,
        pattern=r"^[6-9]\d{9}$"
    )
    password: str = Field(
        ...,
        min_length=8
    )

class LoginSchema(BaseModel):
    emailMobile: str
    password: str


class UserResponseSchema(BaseModel):
    name: str
    email: str
    mobile: str
    role: str
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"