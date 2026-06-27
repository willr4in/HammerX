from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import LotRepository
from app.schemas import LotCreate
from app.models import Lot
from datetime import datetime, timezone, timedelta
from app.config import settings

class LotService:
    def __init__(self, db: AsyncSession):
        self.lot_repository = LotRepository(db)

    async def create_lot(self, data: LotCreate, seller_id: int) -> Lot:
        ends_at = datetime.now(timezone.utc) + timedelta(minutes=settings.auction_duration_time)
        return await self.lot_repository.create_lot(
            title=data.title,
            description=data.description,
            start_price=data.start_price,
            seller_id=seller_id,
            ends_at=ends_at
        )
    
    async def get_by_id(self, lot_id: int) -> Lot | None:
        return await self.lot_repository.get_by_id(lot_id)
    
    async def get_all(self) -> list[Lot]:
        return await self.lot_repository.get_all()
