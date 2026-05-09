import React from 'react'

function PriorityBadge({ priority }) {
  const priorityClassName = priority.toLowerCase()

  return (
    <span className={`badge badge-priority badge-priority-${priorityClassName}`}>
      {priority}
    </span>
  )
}

export default PriorityBadge
