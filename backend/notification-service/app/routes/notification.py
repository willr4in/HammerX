from fastapi import APIRouter, Depends
from app.schemas import NotificationResponse
from app.services import NotificationService
from app.dependencies import get_notification_service, get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("", response_model=list[NotificationResponse])
async def notifications(
    user_id: int = Depends(get_current_user), 
    notification_service: NotificationService = Depends(get_notification_service)
):
    return await notification_service.get_my_notifications(user_id)

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def notification_is_read(
    notification_id: int,
    user_id: int = Depends(get_current_user),
    notification_service: NotificationService = Depends(get_notification_service)
):
    return await notification_service.mark_as_read(notification_id, user_id)