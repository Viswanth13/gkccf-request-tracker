function formatTimestamp(value) {
  const date = new Date(value)

  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date)
}

function NotesTimeline({ items, emptyTitle, emptyMessage, variant = 'notes' }) {
  if (!items.length) {
    return (
      <div className="drawer-empty-block">
        <p className="drawer-empty-title">{emptyTitle}</p>
        <p className="drawer-empty-copy">{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className="timeline-list">
      {items.map((item) => (
        <article key={`${variant}-${item.id}`} className="timeline-item">
          <div className="timeline-marker" aria-hidden="true" />
          <div className="timeline-content">
            <div className="timeline-meta">
              <span className="timeline-author">
                {variant === 'history'
                  ? `${item.old_status} → ${item.new_status}`
                  : item.author_name}
              </span>
              <span className="timeline-time">{formatTimestamp(item.created_at)}</span>
            </div>
            <p className="timeline-body">
              {variant === 'history'
                ? `Changed by ${item.changed_by}`
                : item.note_text}
            </p>
            {variant === 'notes' && item.note_type !== 'note' ? (
              <p className="timeline-tag">{item.note_type.replace('_', ' ')}</p>
            ) : null}
          </div>
        </article>
      ))}
    </div>
  )
}

export default NotesTimeline
