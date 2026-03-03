from fastapi import APIRouter, Query
from datetime import date
from services.convert_service import converter_real_para_dolar

router = APIRouter()

@router.get("/convert")
async def convert(
    valor: float = Query(..., gt=0),
    data: date = Query(...)
):
    return await converter_real_para_dolar(valor, data)
