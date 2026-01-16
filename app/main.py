from fastapi import FastAPI
from app.routes import router
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)


@app.get("/")
async def root():
    return {"status": "running"}
