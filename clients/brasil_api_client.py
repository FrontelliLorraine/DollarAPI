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

        cotacao = Cotacao.model_validate(response.json())

        return cotacao

    except httpx.RequestError as exc:
        # erro de rede, timeout, DNS etc
        print("Erro de conexão:", repr(exc))
        return None
