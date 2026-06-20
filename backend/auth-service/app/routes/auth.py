from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.services import AuthService
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, RefreshRequest
from app.dependencies import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register(data)

@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(form.username, form.password)

@router.post("/logout", status_code=204)
async def logout(
    data: RefreshRequest, 
    auth_service: AuthService = Depends(get_auth_service),
    user: User = Depends(get_current_user)
):
    await auth_service.logout(data.refresh_token, user.id)

@router.post("/refresh", response_model=Token)
async def refresh(data: RefreshRequest, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh_access(data.refresh_token)

@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return user