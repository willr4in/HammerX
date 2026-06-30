from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories import NotificationRepository
from app.models import Notification

class NotificationService:
    def __init__(self, db: AsyncSession):
        self.notification_repository = NotificationRepository(db)

    async def get_my_notifications(self, user_id) -> list[Notification]:
        return await self.notification_repository.get_by_user_id(user_id)
        
    async def mark_as_read(self, notification_id, user_id) -> Notification:
        result = await self.notification_repository.get_by_id(notification_id)
        if result is None:
            raise HTTPException(404, "Нет такого уведомления")
        if result.user_id != user_id:
            raise HTTPException(403, "Нельзя получить чужие уведомления")
        return await self.notification_repository.mark_as_read(notification_id)
        
