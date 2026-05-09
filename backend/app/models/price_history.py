import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Source(str, enum.Enum):
    tcgplayer = "tcgplayer"
    pricecharting = "pricecharting"


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    source = Column(Enum(Source))
    market_price = Column(Float)
    low_price = Column(Float, nullable=True)
    mid_price = Column(Float, nullable=True)
    high_price = Column(Float, nullable=True)
    foil_price = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    recorded_at = Column(DateTime, default=datetime.utcnow)

    card = relationship("Card", back_populates="price_history")
