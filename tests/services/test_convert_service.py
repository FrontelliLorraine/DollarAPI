from datetime import date
import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from models.cotacao_model import Cotacao, CotacaoItem
from services.convert_service import converter_real_para_dolar

@pytest.mark.asyncio
async def test_converter_real_para_dolar_sucesso(mocker):
    data = date(2023, 8, 1)

    cotacao_mock = Cotacao(
        moeda="USD",
        data=data,
        cotacoes=[
            CotacaoItem(
                paridade_compra= 1,
                paridade_venda= 1,
                cotacao_compra= 4.7738,
                cotacao_venda= 4.7744,
                data_hora_cotacao= "2023-08-01",
                tipo_boletim= "ABERTURA"
            ),
            CotacaoItem(
                paridade_compra= 1,
                paridade_venda= 1,
                cotacao_compra= 4.7646,
                cotacao_venda= 4.7652,
                data_hora_cotacao= "2023-08-01",
                tipo_boletim= "INTERMEDIÁRIO"
            ),
            CotacaoItem(
                paridade_compra= 1,
                paridade_venda= 1,
                cotacao_compra= 4.77,
                cotacao_venda= 4.77,
                data_hora_cotacao= "2023-08-01",
                tipo_boletim= "FECHAMENTO PTAX"
            ),
        ],
    )

    mocker.patch(
        "services.convert_service.buscar_cotacao",
        new=AsyncMock(return_value=cotacao_mock)
    )

    resultado = await converter_real_para_dolar(100.0, data)

    assert resultado.valor_em_real == 100.0
    assert resultado.cotacao_usd == 4.77
    assert resultado.valor_em_dolar == round(100 / 4.77, 2)
    assert resultado.data == data

@pytest.mark.asyncio
async def test_converter_real_para_dolar_sem_ptax(mocker):
    data = date(2023, 8, 1)

    cotacao_mock = Cotacao(
        moeda="USD",
        data=data,
        cotacoes=[
            CotacaoItem(
                paridade_compra=1,
                paridade_venda=1,
                cotacao_compra=4.77,
                cotacao_venda=4.77,
                data_hora_cotacao="2023-08-01",
                tipo_boletim="ABERTURA",
            ),
            CotacaoItem(
                paridade_compra=1,
                paridade_venda=1,
                cotacao_compra=4.76,
                cotacao_venda=4.76,
                data_hora_cotacao="2023-08-01",
                tipo_boletim="INTERMEDIÁRIO",
            ),
        ],
    )

    mocker.patch(
        "services.convert_service.buscar_cotacao",
        new=AsyncMock(return_value=cotacao_mock),
    )

    with pytest.raises(HTTPException) as exc:
        await converter_real_para_dolar(100.0, data)

    erro = exc.value

    assert erro.status_code == 502
    assert erro.detail == "Cotação PTAX não encontrada"