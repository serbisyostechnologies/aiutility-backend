from bson import ObjectId
from app.core.database import MongoDB
from app.core.security import hash_password, verify_password, create_access_token
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
from app.utils.upload import upload_image
from bson import ObjectId

async def register_user(data):
    try:
        await MongoDB.connect_db()
        db = MongoDB.get_database()

        user = {
            "name": data.name,
            "email": data.email,
            "mobile": data.mobile,
            "role": data.role,
            "password": hash_password(data.password),
            "is_active": True,
            "is_logged_in": False,
            "profile_url": "",
            "created_at": datetime.now(timezone.utc)
        }

        result = await db.users.insert_one(user)
        await MongoDB.close_db()

        return {
            "success": True,
            "message": "User registered successfully!"
        }

    except DuplicateKeyError as e:
        await MongoDB.close_db()
        error_message = str(e)

        if "email" in error_message:
            message = "Email already exists"

        elif "mobile" in error_message:
            message = "Mobile number already exists"

        else:
            message = "Duplicate value exists"

        return {
            "success": False,
            "message": message
        }

    except Exception as e:
        await MongoDB.close_db()
        return {
            "success": False,
            "message": str(e)
        }
    
async def login_user(data):
    try:
        await MongoDB.connect_db()
        db = MongoDB.get_database()

        user = await db.users.find_one({
                "$or": [
                    {"email": data.emailMobile},
                    {"mobile": data.emailMobile}
                ]
            })
        if not user:
            return {
                "success": False,
                "message": "User do not exist. Please register!"
            }
        
        valid_password = verify_password(
            data.password,
            user["password"]
        )
        if not valid_password:
            return {
                "success": False,
                "message": "Invalid login credentials!"
            }
        
        await db.users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "is_logged_in": True
                }
            }
        )

        access_token = create_access_token({
            "email": user["email"],
            "role": user["role"],
            "mobile": user["mobile"]
        })

        return {
            "success": True,
            "message": "Login successfully!",
            "access_token": access_token,
            "user": user_serializer(user)
        }
    except Exception as e:
        await MongoDB.close_db()
        return {
            "success": False,
            "message": str(e)
        }
    
def user_serializer(user):
    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "mobile": user.get("mobile"),
        "role": user.get("role"),
        "is_active": user.get("is_active"),
        "profile_url": user.get("profile_url"),
    }

async def upload_photo(user_id, file):
    try:
        result = upload_image(file.file)
        image_url = result["url"]

        await MongoDB.connect_db()
        db = MongoDB.get_database()

        await db.users.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile_url": image_url}},
            return_document=True
        )

        return {
            "success": True,
            "message": "Profile photo updated successfully!",
            "profile_url": image_url
        }
    except Exception as e:
        await MongoDB.close_db()
        return {
            "success": False,
            "message": str(e)
        }