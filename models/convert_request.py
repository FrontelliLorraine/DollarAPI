# models/convert_request.py
from pydantic import BaseModel, Field
from datetime import date

class ConvertRequest(BaseModel):
    valor: float = Field(
        ...,
        gt=0,
        description="Valor em reais a ser convertido",
        example=150.0
    )
    data: date = Field(
        ...,
        description="Data da cotação no formato YYYY-MM-DD",
        example="2024-02-26"
    )
