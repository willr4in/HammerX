from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from app.security import decode_token
from app.services import NotificationService
from app.database import get_session

bearer_scheme = HTTPBearer()

def get_notification_service(db: AsyncSession = Depends(get_session)) -> NotificationService:
    return NotificationService(db)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    token = creds.credentials
    try:
        payload = decode_token(token)
    except InvalidTokenError:
        raise HTTPException(401, "Невалидный или истёкший токен")
    
    if payload.get("type") != "access":
        raise HTTPException(401, "Ожидается access токен")
    
    return int(payload["sub"])