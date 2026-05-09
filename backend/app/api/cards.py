from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.card import Card, Game
from app.models.price_history import PriceHistory

router = APIRouter()


class CardResponse(BaseModel):
    id: int
    name: str
    set_name: str
    card_number: str
    game: str
    rarity: Optional[str]
    image_url: Optional[str]
    current_price: Optional[float]
    price_change_30d: Optional[float]
    price_change_6m: Optional[float]
    price_change_1y: Optional[float]

    model_config = {"from_attributes": True}


def _pct_change(old_price: Optional[float], new_price: Optional[float]) -> Optional[float]:
    if old_price and new_price:
        return round(((new_price - old_price) / old_price) * 100, 2)
    return None


def _price_at(db: Session, card_id: int, days_ago: int) -> Optional[float]:
    since = datetime.utcnow() - timedelta(days=days_ago)
    row = (
        db.query(PriceHistory)
        .filter(PriceHistory.card_id == card_id, PriceHistory.recorded_at >= since)
        .order_by(PriceHistory.recorded_at)
        .first()
    )
    return row.market_price if row else None


def _enrich(card: Card, db: Session) -> dict:
    latest = (
        db.query(PriceHistory)
        .filter(PriceHistory.card_id == card.id)
        .order_by(PriceHistory.recorded_at.desc())
        .first()
    )
    current = latest.market_price if latest else None
    return {
        **{c.name: getattr(card, c.name) for c in card.__table__.columns},
        "current_price": current,
        "price_change_30d": _pct_change(_price_at(db, card.id, 30), current),
        "price_change_6m": _pct_change(_price_at(db, card.id, 180), current),
        "price_change_1y": _pct_change(_price_at(db, card.id, 365), current),
    }


@router.get("/", response_model=list[CardResponse])
def list_cards(game: Optional[Game] = None, db: Session = Depends(get_db)):
    query = db.query(Card)
    if game:
        query = query.filter(Card.game == game)
    cards = query.all()
    return [_enrich(c, db) for c in cards]


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return _enrich(card, db)
