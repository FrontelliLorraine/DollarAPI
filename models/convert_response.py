from pydantic import BaseModel, Field
from datetime import date

class ConvertResponse(BaseModel):
    valor_em_real: float = Field(
        ...,
        example=150.00
    )
    cotacao_usd: float = Field(
        ...,
        example=5.1682
    )
    valor_em_dolar: float = Field(
        ...,
        example=30.45
    )
    data: date = Field(
        ...,
        example="2024-02-26"
    )

def convert_brasil_api_response(data: dict) -> dict:
    cotacoes_convertidas = []

    for item in data.get("cotacoes", []):
        cotacoes_convertidas.append(
            {
                "paridade_compra": item.get("paridadeCompra", 1.0),
                "paridade_venda": item.get("paridadeVenda", 1.0),
                "cotacao_compra": item.get("cotacaoCompra"),
                "cotacao_venda": item.get("cotacaoVenda"),
                "data_hora_cotacao": item.get(
                    "dataHoraCotacao",
                    f"{data.get('data')} 00:00:00"
                ),
                "tipo_boletim": item.get("tipoBoletim"),
            }
        )

    return {
        "moeda": data.get("moeda"),
        "data": data.get("data"),
        "cotacoes": cotacoes_convertidas,
    }

