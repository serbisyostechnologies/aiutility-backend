from fastapi import APIRouter, File, UploadFile, Form
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.controllers.user_controller import register_user, login_user, upload_photo

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
async def create(data: RegisterSchema):
    response = await register_user(data)
    return response

@router.post("/login")
async def login(data: LoginSchema):
    response = await login_user(data)
    return response

@router.post("/upload-profile-photo")
async def upload_profile_photo(user_id: str = Form(...), file: UploadFile = File(...)):
    result = await upload_photo(user_id, file)
    return result