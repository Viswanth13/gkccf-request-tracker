import EmptyState from "../common/EmptyState"
import LoadingState from "../common/LoadingState"
import PriorityBadge from "./PriorityBadge"
import StatusBadge from "./StatusBadge"
import NotesTimeline from "./NotesTimeline"

function formatCurrency(value) {
  if (!value) {
    return null
  }

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(Number(value))
}

function DetailField({ label, value, children }) {
  return (
    <div className="detail-field">
      <p className="detail-label">{label}</p>
      {children || <p className="detail-value">{value}</p>}
    </div>
  )
}

function RequestDetailDrawer({
  isOpen,
  requestDetail,
  loading,
  error,
  onClose,
}) {
  if (!isOpen) {
    return null
  }

  let content = null

  if (loading) {
    content = <LoadingState message="Loading request details from the backend API." />
  } else if (error) {
    content = (
      <EmptyState
        title="Unable to load request details"
        message={error}
      />
    )
  } else if (requestDetail) {
    content = (
      <>
        <div className="drawer-header">
          <div>
            <p className="drawer-request-id">{requestDetail.request_id}</p>
            <h2 className="drawer-title">{requestDetail.title}</h2>
            <p className="drawer-subtitle">
              {requestDetail.requester_name} · {requestDetail.requester_type}
            </p>
          </div>
          <button type="button" className="drawer-close-button" onClick={onClose}>
            Close
          </button>
        </div>

        {requestDetail.missing_information ? (
          <section className="warning-banner">
            <p className="warning-title">Missing information</p>
            <p className="warning-copy">{requestDetail.missing_information}</p>
          </section>
        ) : null}

        <section className="drawer-section">
          <div className="detail-grid">
            <DetailField label="Category" value={requestDetail.category} />
            <DetailField label="Fund Name" value={requestDetail.fund_name} />
            <DetailField label="Owner" value={requestDetail.owner.name} />
            <DetailField label="Priority">
              <PriorityBadge priority={requestDetail.priority} />
            </DetailField>
            <DetailField label="Status">
              <StatusBadge status={requestDetail.status} />
            </DetailField>
            {requestDetail.grant_amount ? (
              <DetailField
                label="Grant Amount"
                value={formatCurrency(requestDetail.grant_amount)}
              />
            ) : null}
            {requestDetail.nonprofit_name ? (
              <DetailField
                label="Nonprofit Name"
                value={requestDetail.nonprofit_name}
              />
            ) : null}
          </div>
        </section>

        <section className="drawer-section">
          <h3 className="drawer-section-title">Request Details</h3>
          <p className="drawer-description">{requestDetail.description}</p>
        </section>

        <section className="drawer-section">
          <h3 className="drawer-section-title">Notes Timeline</h3>
          <NotesTimeline
            items={requestDetail.notes}
            emptyTitle="No notes yet"
            emptyMessage="Internal notes will appear here once the workflow actions are enabled."
          />
        </section>

        <section className="drawer-section">
          <h3 className="drawer-section-title">Status History</h3>
          <NotesTimeline
            items={requestDetail.status_history}
            emptyTitle="No status changes yet"
            emptyMessage="Status history will appear here after request updates."
            variant="history"
          />
        </section>

        <section className="drawer-section">
          <h3 className="drawer-section-title">Latest AI Draft</h3>
          {requestDetail.latest_ai_draft ? (
            <article className="ai-draft-card">
              <p className="ai-draft-warning">
                AI-generated draft. Human review is required before sending.
              </p>
              <pre className="ai-draft-text">{requestDetail.latest_ai_draft.draft_text}</pre>
            </article>
          ) : (
            <div className="drawer-empty-block">
              <p className="drawer-empty-title">No AI draft yet</p>
              <p className="drawer-empty-copy">
                A generated donor-safe draft will appear here once the workflow action is enabled.
              </p>
            </div>
          )}
        </section>
      </>
    )
  }

  return (
    <>
      <button
        type="button"
        className="drawer-backdrop"
        aria-label="Close request detail drawer"
        onClick={onClose}
      />
      <aside className="detail-drawer" aria-label="Request detail drawer">
        {content}
      </aside>
    </>
  )
}

export default RequestDetailDrawer
