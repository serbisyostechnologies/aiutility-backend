from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserModel(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    role: str
    password: str
    is_active: bool
    is_logged_in: bool
    profile_url: str
    created_at: datetime