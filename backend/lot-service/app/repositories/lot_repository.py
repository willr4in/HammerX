from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Lot
from decimal import Decimal
from datetime import datetime

class LotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, lot_id: int) -> Lot | None:
        result = await self.db.execute(select(Lot).where(Lot.id==lot_id))
        return result.scalar_one_or_none()

    async def create_lot(
        self, title: str, description: str | None, start_price: Decimal,
        seller_id: int, ends_at: datetime
    ) -> Lot:
        lot = Lot(
            title=title, description=description, start_price=start_price,
            seller_id=seller_id, ends_at=ends_at
            ) 
        self.db.add(lot)
        await self.db.commit()
        await self.db.refresh(lot)
        return lot
    
    async def get_all(self) -> list[Lot] | None:
        result = await self.db.execute(select(Lot))
        return list(result.scalars().all())