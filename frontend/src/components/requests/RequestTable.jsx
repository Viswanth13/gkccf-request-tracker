import PriorityBadge from "./PriorityBadge"
import StatusBadge from "./StatusBadge"

function formatUpdatedAt(value) {
  const date = new Date(value)

  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date)
}

function RequestTable({ requests }) {
  return (
    <div className="table-shell">
      <table className="request-table">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Requester</th>
            <th>Requester Type</th>
            <th>Category</th>
            <th>Fund</th>
            <th>Owner</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Updated</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((request) => (
            <tr key={request.id}>
              <td className="table-primary">{request.request_id}</td>
              <td>{request.requester_name}</td>
              <td>{request.requester_type}</td>
              <td>{request.category}</td>
              <td>{request.fund_name}</td>
              <td>{request.owner_name}</td>
              <td>
                <PriorityBadge priority={request.priority} />
              </td>
              <td>
                <StatusBadge status={request.status} />
              </td>
              <td>{formatUpdatedAt(request.updated_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RequestTable
