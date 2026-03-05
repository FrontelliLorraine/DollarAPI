from datetime import date
from fastapi import HTTPException

from clients.brasil_api_client import buscar_cotacao
from models.convert_response import ConvertResponse


async def converter_real_para_dolar(valor: float, data: date) -> ConvertResponse:
    cotacao = await buscar_cotacao(data)

    cotacao_ptax = next(
        (c for c in cotacao.cotacoes if c.tipo_boletim == "FECHAMENTO PTAX"),
        None
    )

    if cotacao_ptax is None:
        raise HTTPException(
            status_code=502,
            detail="Cotação PTAX não encontrada"
        )

    valor_em_dolar = valor / cotacao_ptax.cotacao_venda

    return ConvertResponse(
        valor_em_real=valor,
        cotacao_usd=cotacao_ptax.cotacao_venda,
        valor_em_dolar=round(valor_em_dolar, 2),
        data=cotacao.data
    )
