from app.services.user_service import create_user

async def register_user(user):
    return await create_user(user)