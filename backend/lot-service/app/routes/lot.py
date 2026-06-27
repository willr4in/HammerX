from fastapi import APIRouter, Depends, HTTPException
from app.schemas import LotCreate, LotResponse
from app.services import LotService
from app.dependencies import get_lot_service, get_current_user

router = APIRouter(prefix="/lots", tags=["lots"])

@router.post("", response_model=LotResponse, status_code=201)
async def create_lot(
    data: LotCreate,
    seller_id: int = Depends(get_current_user),
    lot_service: LotService = Depends(get_lot_service)
):
    return await lot_service.create_lot(data, seller_id)

@router.get("", response_model=list[LotResponse])
async def list_lots(lot_service: LotService = Depends(get_lot_service)):
    return await lot_service.get_all()

@router.get("/{lot_id}", response_model=LotResponse)
async def get_lot(lot_id: int, lot_service: LotService = Depends(get_lot_service)):
    lot = await lot_service.get_by_id(lot_id)
    if lot is None:
        raise HTTPException(404, "Лот не найден")
    return lot