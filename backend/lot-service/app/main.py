from fastapi import FastAPI
from app.routes import lot_router

app = FastAPI()
app.include_router(lot_router)

@app.get("/health")
async def health():
    return {"status": "ok"}