from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from app.security import decode_token
from app.services import AuthService
from app.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_auth_service(db: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(db)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        payload = decode_token(token)
    except InvalidTokenError:
        raise HTTPException(401, "Невалидный или истёкший токен")
    
    if payload.get("type") != "access":
        raise HTTPException(401, "Ожидается access token")
    
    user = await auth_service.get_user_by_id(int(payload["sub"]))
    if user is None:
        raise HTTPException(401, "Пользователь не найден")
    
    return user