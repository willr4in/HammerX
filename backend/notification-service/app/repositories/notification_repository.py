from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Notification

class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> list[Notification]:
        result = await self.db.execute(select(Notification).where(Notification.user_id==user_id))
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> Notification | None:
        result = await self.db.execute(select(Notification).where(Notification.id==id))
        return result.scalar_one_or_none()
    
    async def mark_as_read(self, notification_id: int) -> Notification | None:
        result = await self.db.execute(select(Notification).where(Notification.id==notification_id))
        notification = result.scalar_one_or_none()
        if notification is None:
            return None
        notification.is_read = True
        await self.db.commit()
        await self.db.refresh(notification)
        return notification