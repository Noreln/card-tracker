from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models.price_history import PriceHistory, Source

router = APIRouter()

PERIOD_DAYS = {"30d": 30, "6m": 180, "1y": 365}


class PricePoint(BaseModel):
    recorded_at: datetime
    market_price: float
    source: str

    model_config = {"from_attributes": True}


@router.get("/{card_id}/history", response_model=list[PricePoint])
def get_price_history(
    card_id: int,
    period: str = Query("30d", pattern="^(30d|6m|1y)$"),
    source: Optional[Source] = None,
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=PERIOD_DAYS[period])
    query = db.query(PriceHistory).filter(
        PriceHistory.card_id == card_id,
        PriceHistory.recorded_at >= since,
    )
    if source:
        query = query.filter(PriceHistory.source == source)
    return query.order_by(PriceHistory.recorded_at).all()


@router.get("/{card_id}/summary")
def get_price_summary(card_id: int, db: Session = Depends(get_db)):
    def price_at(days: int) -> Optional[float]:
        since = datetime.utcnow() - timedelta(days=days)
        row = (
            db.query(PriceHistory)
            .filter(PriceHistory.card_id == card_id, PriceHistory.recorded_at >= since)
            .order_by(PriceHistory.recorded_at)
            .first()
        )
        return row.market_price if row else None

    current_row = (
        db.query(PriceHistory)
        .filter(PriceHistory.card_id == card_id)
        .order_by(PriceHistory.recorded_at.desc())
        .first()
    )
    current = current_row.market_price if current_row else None

    def pct(old: Optional[float]) -> Optional[float]:
        if old and current:
            return round(((current - old) / old) * 100, 2)
        return None

    return {
        "current_price": current,
        "change_30d": pct(price_at(30)),
        "change_6m": pct(price_at(180)),
        "change_1y": pct(price_at(365)),
    }
