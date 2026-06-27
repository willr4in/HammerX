from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class LotBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str | None = None
    start_price: Decimal = Field(..., gt=0)

class LotCreate(LotBase):
    pass

class LotResponse(LotBase):
    id: int
    seller_id: int
    status: str
    starts_at: datetime
    ends_at: datetime
    winner_id: int | None
    final_price: Decimal | None
    
    model_config = {"from_attributes": True}