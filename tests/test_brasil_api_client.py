import pytest
import respx
from httpx import Response
from datetime import date
from fastapi import HTTPException

from clients.brasil_api_client import buscar_cotacao, BRASIL_API_URL

@respx.mock
@pytest.mark.asyncio
async def test_buscar_cotacao_sucesso():
    data = date(2023, 8, 1)

    respx.get(
        BRASIL_API_URL.format(data=data.isoformat())
    ).mock(
        return_value=Response(
            status_code=200,
            json={
                "moeda": "USD",
                "data": "2023-08-01",
                "cotacoes": [
                    {
                        "tipoBoletim": "FECHAMENTO PTAX",
                        "cotacaoVenda": 4.95,
                        "cotacaoCompra": 4.94
                    }
                ]
            }
        )
    )

    cotacao = await buscar_cotacao(data)

    assert cotacao.moeda == "USD"
    assert cotacao.data == data
    assert len(cotacao.cotacoes) == 1
