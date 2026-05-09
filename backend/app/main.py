from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.api import cards, prices
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Card Tracker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
app.include_router(prices.router, prefix="/api/prices", tags=["prices"])


@app.get("/health")
def health():
    return {"status": "ok"}
