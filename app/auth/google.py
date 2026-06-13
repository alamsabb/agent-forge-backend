from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def login():
    return {"message": "Google OAuth Login Flow Placeholder"}

@router.get("/callback")
async def callback():
    return {"message": "Google OAuth Callback Placeholder"}
