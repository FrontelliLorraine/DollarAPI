from fastapi import HTTPException
import httpx
from datetime import date
from typing import Optional

from models.cotacao_model import Cotacao

BRASIL_API_URL = "https://brasilapi.com.br/api/cambio/v1/cotacao/USD/{data}"


async def buscar_cotacao(data: date) -> Optional[Cotacao]:
    try:
        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            response = await client.get(
                BRASIL_API_URL.format(data=data.isoformat())
            )
        
        response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        body = exc.response.json()
        raise HTTPException(
            status_code=exc.response.status_code,
            detail={
                "code": body.get("name", "ERRO_API_EXTERNA"),
                "message": body.get("message", "Erro na consulta à BrasilAPI.")
            }
    )    
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


