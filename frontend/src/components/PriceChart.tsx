import { useState } from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { usePriceHistory } from '../hooks/useCards';
import type { Period } from '../types';

interface Props {
  cardId: number;
}

const PERIODS: { label: string; value: Period }[] = [
  { label: '30 Days', value: '30d' },
  { label: '6 Months', value: '6m' },
  { label: '1 Year', value: '1y' },
];

export default function PriceChart({ cardId }: Props) {
  const [period, setPeriod] = useState<Period>('30d');
  const { history, loading } = usePriceHistory(cardId, period);

  const data = history.map((p) => ({
    date: new Date(p.recorded_at).toLocaleDateString(),
    price: p.market_price,
  }));

  return (
    <div className="price-chart">
      <div className="period-selector">
        {PERIODS.map((p) => (
          <button
            key={p.value}
            className={period === p.value ? 'active' : ''}
            onClick={() => setPeriod(p.value)}
          >
            {p.label}
          </button>
        ))}
      </div>
      {loading ? (
        <p className="loading">Loading chart...</p>
      ) : data.length === 0 ? (
        <p className="no-data">No price data available for this period.</p>
      ) : (
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="date" tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <YAxis tickFormatter={(v: number) => `$${v}`} tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <Tooltip
              contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }}
              formatter={(v: number) => [`$${v.toFixed(2)}`, 'Price']}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#6366f1"
              dot={false}
              strokeWidth={2}
              activeDot={{ r: 4, fill: '#6366f1' }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
