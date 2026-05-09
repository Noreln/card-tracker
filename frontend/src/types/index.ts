export type Game = 'pokemon' | 'one_piece';
export type Source = 'tcgplayer' | 'cardmarket';
export type Period = '30d' | '6m' | '1y';

export interface Card {
  id: number;
  name: string;
  set_name: string;
  card_number: string;
  game: Game;
  rarity: string | null;
  image_url: string | null;
  current_price: number | null;
  price_change_30d: number | null;
  price_change_6m: number | null;
  price_change_1y: number | null;
}

export interface PricePoint {
  recorded_at: string;
  market_price: number;
  source: Source;
}

export interface PriceSummary {
  current_price: number | null;
  change_30d: number | null;
  change_6m: number | null;
  change_1y: number | null;
}
