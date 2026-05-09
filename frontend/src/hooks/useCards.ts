import axios from 'axios';
import { useEffect, useState } from 'react';
import type { Card, Period, PricePoint, PriceSummary, Game } from '../types';

const API_BASE = '/api';

export function useCards(game?: Game) {
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const params = game ? { game } : {};
    axios
      .get<Card[]>(`${API_BASE}/cards/`, { params })
      .then((res) => setCards(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [game]);

  return { cards, loading, error };
}

export function usePriceHistory(cardId: number, period: Period) {
  const [history, setHistory] = useState<PricePoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios
      .get<PricePoint[]>(`${API_BASE}/prices/${cardId}/history`, { params: { period } })
      .then((res) => setHistory(res.data))
      .finally(() => setLoading(false));
  }, [cardId, period]);

  return { history, loading };
}

export function usePriceSummary(cardId: number) {
  const [summary, setSummary] = useState<PriceSummary | null>(null);

  useEffect(() => {
    axios
      .get<PriceSummary>(`${API_BASE}/prices/${cardId}/summary`)
      .then((res) => setSummary(res.data));
  }, [cardId]);

  return { summary };
}
