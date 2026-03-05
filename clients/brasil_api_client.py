from fastapi import HTTPException
import httpx
from datetime import date
from typing import Optional

from models.cotacao_model import Cotacao

BRASIL_API_URL = "https://brasilapi.com.br/api/cambio/v1/cotacao/USD/{data}"


async def buscar_cotacao(data: date) -> Optional[Cotacao]:
    hoje = date.today()

    if data > hoje:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "DATA_FUTURA",
                "message": "A data informada não pode ser futura."
            }
        )

    if data == hoje:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "DATA_HOJE",
                "message": "A cotação do dia atual ainda não está disponível."
            }
        )
    
    try:
        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            response = await client.get(
                BRASIL_API_URL.format(data=data.isoformat())
            )
        
        if response.status_code == 400:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "DATA_INVALIDA",
                    "message": "Data inválida para consulta de cotação."
                }
            )
        
        response.raise_for_status()

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "code": "API_EXTERNA_INDISPONIVEL",
                "message": "Falha ao consultar a BrasilAPI."
            }
        )

    cotacao = Cotacao.model_validate(response.json())

    return cotacao


