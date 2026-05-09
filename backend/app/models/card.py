import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Game(str, enum.Enum):
    pokemon = "pokemon"
    one_piece = "one_piece"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    set_name = Column(String)
    set_code = Column(String)
    card_number = Column(String)
    game = Column(Enum(Game))
    rarity = Column(String, nullable=True)
    tcgplayer_id = Column(String, unique=True, nullable=True)
    pricecharting_id = Column(String, unique=True, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    price_history = relationship("PriceHistory", back_populates="card")
