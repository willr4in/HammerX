from fastapi import FastAPI
from app.routes import notification_router

app = FastAPI()
app.include_router(notification_router)

@app.get("/health")
async def health():
    return {"status": "ok"}