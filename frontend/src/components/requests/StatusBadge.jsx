import React from 'react'

function StatusBadge({ status }) {
  const statusClassName = status
    .toLowerCase()
    .replaceAll(' ', '-')

  return (
    <span className={`badge badge-status badge-status-${statusClassName}`}>
      {status}
    </span>
  )
}

export default StatusBadge
