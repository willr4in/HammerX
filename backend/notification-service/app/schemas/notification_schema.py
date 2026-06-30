from pydantic import BaseModel, Field
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    lot_id: int | None
    message: str
    is_read: bool
    created_at: datetime

    model_config = {'from_attributes': True}