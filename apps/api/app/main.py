from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import annotations, categories, quran, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Mushafi API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,        prefix="/api/v1/auth",        tags=["auth"])
app.include_router(annotations.router, prefix="/api/v1/annotations", tags=["annotations"])
app.include_router(categories.router,  prefix="/api/v1/categories",  tags=["categories"])
app.include_router(quran.router,       prefix="/api/v1/quran",       tags=["quran"])


@app.get("/health")
async def health():
    return {"status": "ok"}
