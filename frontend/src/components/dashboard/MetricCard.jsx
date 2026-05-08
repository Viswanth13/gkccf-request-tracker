function MetricCard({ label, value, helperText }) {
  return (
    <article className="metric-card">
      <p className="metric-label">{label}</p>
      <p className="metric-value">{value}</p>
      <p className="metric-helper">{helperText}</p>
    </article>
  )
}

export default MetricCard
