from fastapi import APIRouter, Query
from datetime import date
from services.convert_service import converter_real_para_dolar
from models.convert_response import ConvertResponse

router = APIRouter(tags=["Conversão"])

@router.get(
    "/convert",
    summary="Converter Real para Dólar",
    description="Converte um valor em **Real (BRL)** para **Dólar (USD)** com base na cotação do dia informado.",
    response_description="Resultado da conversão com a cotação utilizada",
    response_model=ConvertResponse,  # documenta o schema da resposta
    responses={
        200: {
            "description": "Conversão realizada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "valor_original": 100.0,
                        "data": "2024-03-01",
                        "cotacao": 4.95,
                        "valor_convertido": 20.20
                    }
                }
            }
        },
        404: {"description": "Cotação não encontrada para a data informada"},
        422: {"description": "Parâmetros inválidos"},
    }
)
async def convert(
    valor: float = Query(
        ...,
        gt=0,
        description="Valor em Reais a ser convertido",
        examples={
            "valor_padrao": {
                "summary": "Valor comum",
                "value": 100.0
            }
        }
    ),
    data: date = Query(
        ...,
        description="Data de referência para a cotação (não pode ser futura)",
        examples={
            "data_valida": {
                "summary": "Data válida",
                "value": "2024-03-01"
            }
        }
    )
):
    return await converter_real_para_dolar(valor, data)
