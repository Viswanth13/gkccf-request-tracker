import React from 'react'

function LoadingState({ message = 'Loading requests...' }) {
  return (
    <div className="feedback-card">
      <div className="loading-spinner" aria-hidden="true" />
      <p className="feedback-title">Loading dashboard</p>
      <p className="feedback-copy">{message}</p>
    </div>
  )
}

export default LoadingState
