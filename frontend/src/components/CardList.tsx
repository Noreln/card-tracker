import { Link } from 'react-router-dom';
import type { Card } from '../types';
import PriceChangeCard from './PriceChangeCard';

interface Props {
  cards: Card[];
}

export default function CardList({ cards }: Props) {
  if (cards.length === 0) {
    return <p className="empty">No cards found.</p>;
  }

  return (
    <div className="card-list">
      {cards.map((card) => (
        <Link key={card.id} to={`/cards/${card.id}`} className="card-item">
          {card.image_url ? (
            <img src={card.image_url} alt={card.name} className="card-thumb" />
          ) : (
            <div className="card-thumb placeholder" />
          )}
          <div className="card-info">
            <h3>{card.name}</h3>
            <p className="set">
              {card.set_name} · {card.card_number}
            </p>
            <p className="game-badge">{card.game === 'pokemon' ? 'Pokémon' : 'One Piece'}</p>
            <p className="price">
              {card.current_price != null ? `$${card.current_price.toFixed(2)}` : 'No price'}
            </p>
            <div className="changes">
              <PriceChangeCard label="30d" value={card.price_change_30d} />
              <PriceChangeCard label="6m" value={card.price_change_6m} />
              <PriceChangeCard label="1y" value={card.price_change_1y} />
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
