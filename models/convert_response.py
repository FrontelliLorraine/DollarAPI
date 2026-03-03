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



