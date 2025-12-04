from app.db.mongo import users_collection
from app.core.security import hash_password

async def create_user(user):
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["is_active"] = True  

    await users_collection.insert_one(user_dict)

    return {
        "email": user_dict["email"],
        "is_active": True
    }