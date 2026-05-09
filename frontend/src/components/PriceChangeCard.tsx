interface Props {
  label: string;
  value: number | null;
}

export default function PriceChangeCard({ label, value }: Props) {
  if (value === null) {
    return (
      <div className="price-change-card neutral">
        <span className="label">{label}</span>
        <span className="value">N/A</span>
      </div>
    );
  }
  const positive = value >= 0;
  return (
    <div className={`price-change-card ${positive ? 'positive' : 'negative'}`}>
      <span className="label">{label}</span>
      <span className="value">
        {positive ? '+' : ''}
        {value.toFixed(2)}%
      </span>
    </div>
  );
}
