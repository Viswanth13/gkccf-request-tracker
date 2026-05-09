import React from 'react'

function EmptyState({ title, message }) {
  return (
    <div className="feedback-card">
      <p className="feedback-title">{title}</p>
      <p className="feedback-copy">{message}</p>
    </div>
  )
}

export default EmptyState
