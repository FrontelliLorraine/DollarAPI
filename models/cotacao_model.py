from pydantic import BaseModel
from typing import List
from datetime import date


class CotacaoItem(BaseModel):
    paridade_compra: float
    paridade_venda: float
    cotacao_compra: float
    cotacao_venda: float
    data_hora_cotacao: str
    tipo_boletim: str


class Cotacao(BaseModel):
    moeda: str
    data: date
    cotacoes: List[CotacaoItem]
