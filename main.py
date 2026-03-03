from fastapi import FastAPI
from controllers.convert_controller import router as convert_router

app = FastAPI(
    title="API de Conversão",
    version="1.0.0"
)

app.include_router(
    convert_router,
    prefix="/api/v1",
    tags=["Conversão"]
)
