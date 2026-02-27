from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import date
import httpx

app = FastAPI(
    title="Dollar Converter API",
    description="API para conversão de Real para Dólar usando a BrasilAPI"
)

class ConvertRequest(BaseModel):
    valor_real: float = Field(
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

class ConvertResponse(BaseModel):
    valor_real: str
    valor_dolar: str


BRASIL_API_URL = "https://brasilapi.com.br/api/cambio/v1/cotacao/USD/{data}"

async def buscar_cotacao_dolar(data: str) -> float:
    try:
        async with httpx.AsyncClient(verify=False,timeout=5) as client:
            response = await client.get(
                BRASIL_API_URL.format(data=data)
            )

        response.raise_for_status()
        return response.json()["cotacaoVenda"]

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Erro de conexão com a BrasilAPI"
        )
    except KeyError:
        raise HTTPException(
            status_code=500,
            detail="Resposta inesperada da BrasilAPI"
        )

@app.get("/")
async def root():
    return {"status": "API no ar"}

@app.post("/convert", response_model=ConvertResponse)
async def converter(request: ConvertRequest):

    cotacao = await buscar_cotacao_dolar(request.data.isoformat())
    valor_dolar = request.valor_real / cotacao

    return ConvertResponse(
        valor_real=f"R$ {request.valor_real:.2f}",
        valor_dolar=f"US$ {valor_dolar:.2f}"
    )
