from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from app.security import decode_token
from app.services import LotService
from app.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_lot_service(db: AsyncSession = Depends(get_session)) -> LotService:
    return LotService(db)

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_token(token)
    except InvalidTokenError:
        raise HTTPException(401, "Невалидный или истёкший токен")
    
    if payload.get("type") != "access":
        raise HTTPException(401, "Ожидается access токен")
    
    return int(payload["sub"])