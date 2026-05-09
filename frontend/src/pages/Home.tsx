import { useState } from 'react';
import CardList from '../components/CardList';
import { useCards } from '../hooks/useCards';
import type { Game } from '../types';

const FILTERS: { label: string; value: Game | undefined }[] = [
  { label: 'All', value: undefined },
  { label: 'Pokémon', value: 'pokemon' },
  { label: 'One Piece', value: 'one_piece' },
];

export default function Home() {
  const [selectedGame, setSelectedGame] = useState<Game | undefined>(undefined);
  const { cards, loading, error } = useCards(selectedGame);

  const movers = [...cards]
    .filter((c) => c.price_change_30d !== null)
    .sort((a, b) => Math.abs(b.price_change_30d!) - Math.abs(a.price_change_30d!));

  return (
    <div className="home">
      <div className="hero">
        <h1>Card Tracker</h1>
        <p className="subtitle">Track meaningful price changes in One Piece &amp; Pokémon TCG</p>
      </div>
      <div className="game-filter">
        {FILTERS.map((f) => (
          <button
            key={f.label}
            className={selectedGame === f.value ? 'active' : ''}
            onClick={() => setSelectedGame(f.value)}
          >
            {f.label}
          </button>
        ))}
      </div>
      {loading && <p className="loading">Loading cards...</p>}
      {error && <p className="error">Error: {error}</p>}
      {!loading && !error && <CardList cards={movers} />}
    </div>
  );
}
