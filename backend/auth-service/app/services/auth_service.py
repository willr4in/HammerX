from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from jwt import InvalidTokenError
from app.repositories import UserRepository, RefreshTokenRepository
from app.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.schemas import UserCreate, Token
from app.security import decode_token
from datetime import datetime, timezone
from app.models import User

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)
        self.refresh_token_repository = RefreshTokenRepository(db)

    async def register(self, data: UserCreate) -> User:
        existing = await self.user_repository.get_by_email(data.email)
        if existing:
            raise HTTPException(409, "Email уже зарегистрирован")
        hashed = hash_password(data.password)
        return await self.user_repository.create_user(data.email, data.username, hashed)
    
    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Неверный email или пароль")
        return user

    async def login(self, email: str, password: str) -> Token:
        user = await self.authenticate(email, password)
        token = Token(
            access_token = create_access_token(user.id),
            refresh_token = create_refresh_token(user.id)
        )
        payload = decode_token(token.refresh_token)
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await self.refresh_token_repository.save(user.id, token.refresh_token, expires_at)
        return token
    
    async def logout(self, refresh_token: str, user_id: int) -> None:
        stored = await self.refresh_token_repository.get_by_token(refresh_token)
        if stored is None:
            return
        if stored.user_id != user_id:
            raise HTTPException(403, "Нельзя отозвать чужой токен")
        await self.refresh_token_repository.revoke(stored)
            
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_by_id(user_id)
    
    async def refresh_access(self, refresh_token: str) -> Token:
        try:
            payload = decode_token(refresh_token)
        except InvalidTokenError:
            raise HTTPException(401, "Невалидный или истекший refresh токен")
        
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Ожидается refresh токен")
        
        stored = await self.refresh_token_repository.get_by_token(refresh_token)
        if stored is None or stored.revoked:
            raise HTTPException(401, "Refresh токен отозван или не найден")
        
        user_id = int(payload["sub"])
        return Token(
            access_token=create_access_token(user_id),
            refresh_token=refresh_token
        )