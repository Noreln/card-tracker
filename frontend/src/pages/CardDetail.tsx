import { Link, useParams } from 'react-router-dom';
import PriceChangeCard from '../components/PriceChangeCard';
import PriceChart from '../components/PriceChart';
import { usePriceSummary } from '../hooks/useCards';

export default function CardDetail() {
  const { id } = useParams<{ id: string }>();
  const cardId = Number(id);
  const { summary } = usePriceSummary(cardId);

  return (
    <div className="card-detail">
      <Link to="/" className="back-link">← Back</Link>
      <h2>Price History</h2>
      {summary && (
        <>
          <p className="current-price">
            {summary.current_price != null
              ? `$${summary.current_price.toFixed(2)}`
              : 'No price data'}
          </p>
          <div className="changes">
            <PriceChangeCard label="30 Days" value={summary.change_30d} />
            <PriceChangeCard label="6 Months" value={summary.change_6m} />
            <PriceChangeCard label="1 Year" value={summary.change_1y} />
          </div>
        </>
      )}
      <PriceChart cardId={cardId} />
    </div>
  );
}
