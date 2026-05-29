from fastapi import APIRouter
from app.core.database import MongoDB

router = APIRouter()


@router.get("/health")
async def health_check():

    try:
        await MongoDB.client.admin.command("ping")

        return {
            "status": "success",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "failed",
            "database": str(e)
        }