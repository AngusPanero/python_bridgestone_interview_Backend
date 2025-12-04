from fastapi import Request, APIRouter, Depends
from app.schemas.user_schema import UserCreate, UserResponse, Token
from app.controllers.user_controller import register_user
from app.middlewares.auth_middleware import verify_token
from app.db.token_blacklist import revoked_tokens
from app.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    new_user = await register_user(user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(dep=Depends(verify_token)):
    return {"message": "Ruta protegida con JWT ✅"}

@router.post("/logout")
async def logout(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {"message": "No token provided"}

    token = auth_header.split(" ")[1]

    revoked_tokens.add(token)

    return {"message": "Logout successful ✅"}