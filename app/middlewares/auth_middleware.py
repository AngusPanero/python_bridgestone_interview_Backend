from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.db.token_blacklist import revoked_tokens

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing"
        )

    try:
        token = auth_header.split(" ")[1]

        # 🔴 Chequeo de logout
        if token in revoked_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revoked (logout)"
            )

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        request.state.user = payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )