from pydantic import BaseModel, Field
from datetime import date
from typing import Any, Dict, List

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

def convert_brasil_api_response(resposta_api: Dict[str, Any]) -> Dict[str, Any]:
    cotacoes: List[Dict[str, Any]] = []

    for item in resposta_api.get("cotacoes", []):
        cotacoes.append({
            "paridade_compra": (
                item.get("paridadeCompra")
                or item.get("paridade_compra")
            ),
            "paridade_venda": (
                item.get("paridadeVenda")
                or item.get("paridade_venda")
            ),
            "cotacao_compra": (
                item.get("cotacaoCompra")
                or item.get("cotacao_compra")
            ),
            "cotacao_venda": (
                item.get("cotacaoVenda")
                or item.get("cotacao_venda")
            ),
            "data_hora_cotacao": (
                item.get("dataHoraCotacao")
                or item.get("data_hora_cotacao")
            ),
            "tipo_boletim": (
                item.get("tipoBoletim")
                or item.get("tipo_boletim")
            ),
        })

    return {
        "moeda": resposta_api.get("moeda"),
        "data": date.fromisoformat(resposta_api.get("data")),
        "cotacoes": cotacoes,
    }

