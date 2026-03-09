import pytest
import respx
import httpx
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
                        "paridade_compra": 1,
                        "paridade_venda": 1,
                        "cotacao_compra": 4.7738,
                        "cotacao_venda": 4.7744,
                        "data_hora_cotacao": "2023-08-01",
                        "tipo_boletim": "ABERTURA"
                    },
                    {
                        "paridade_compra": 1,
                        "paridade_venda": 1,
                        "cotacao_compra": 4.7646,
                        "cotacao_venda": 4.7652,
                        "data_hora_cotacao": "2023-08-01",
                        "tipo_boletim": "INTERMEDIÁRIO"
                    },
                    {
                        "paridadeCompra": 1,
                        "paridadeVenda": 1,
                        "cotacaoCompra": 4.77,
                        "cotacaoVenda": 4.77,
                        "dataHoraCotacao": "2023-08-03",
                        "tipoBoletim": "FECHAMENTO PTAX"
                    }
                ]
            }
        )
    )

    cotacao = await buscar_cotacao(data)

    assert cotacao.moeda == "USD"
    assert cotacao.data == data
    assert len(cotacao.cotacoes) == 3

    assert {c.tipo_boletim for c in cotacao.cotacoes} == {
        "ABERTURA",
        "INTERMEDIÁRIO",
        "FECHAMENTO PTAX",
    }

@respx.mock
@pytest.mark.asyncio
async def test_buscar_cotacao_400_bad_request():
    data = date(2023, 8, 1)

    respx.get(
        BRASIL_API_URL.format(data=data.isoformat())
    ).mock(
        return_value=Response(
            status_code=400,
            json={
                "name": "BAD_REQUEST",
                "message": "Data inválida"
            }
        )
    )

    with pytest.raises(HTTPException) as exc:
        await buscar_cotacao(data)

    erro = exc.value

    assert erro.status_code == 400
    assert erro.detail["code"] == "BAD_REQUEST"
    assert erro.detail["message"] == "Data inválida"

@respx.mock
@pytest.mark.asyncio
async def test_buscar_cotacao_404_not_found():
    data = date(1900, 1, 1)

    respx.get(
        BRASIL_API_URL.format(data=data.isoformat())
    ).mock(
        return_value=Response(
            status_code=404,
            json={
                "name": "NOT_FOUND",
                "message": "Cotação não encontrada"
            } 
        )
    )

    with pytest.raises(HTTPException) as exc:
        await buscar_cotacao(data)

    erro = exc.value

    assert erro.status_code == 404
    assert erro.detail["code"] == "NOT_FOUND"
    assert erro.detail["message"] == "Cotação não encontrada"

@respx.mock
@pytest.mark.asyncio
async def test_buscar_cotacao_api_externa_indisponivel():
    data = date(2023, 8, 1)

    respx.get(
        BRASIL_API_URL.format(data=data.isoformat())
    ).mock(
        side_effect=httpx.RequestError("Timeout ao conectar")
    )

    with pytest.raises(HTTPException) as exc:
        await buscar_cotacao(data)

    erro = exc.value

    assert erro.status_code == 502
    assert erro.detail["code"] == "API_EXTERNA_INDISPONIVEL"
    assert erro.detail["message"] == "Falha ao consultar a BrasilAPI."
