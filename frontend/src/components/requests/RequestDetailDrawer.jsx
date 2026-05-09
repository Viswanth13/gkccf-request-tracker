import { useEffect, useState } from 'react'
import {
  addRequestNote,
  generateDraftResponse,
  updateRequestStatus,
} from '../../api/requestsApi'
import EmptyState from "../common/EmptyState"
import LoadingState from "../common/LoadingState"
import PriorityBadge from "./PriorityBadge"
import StatusBadge from "./StatusBadge"
import NotesTimeline from "./NotesTimeline"

const STATUS_OPTIONS = ['New', 'In Review', 'Waiting on Donor', 'Completed']

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
  onRefreshRequestDetail,
  onRefreshRequests,
}) {
  const [selectedStatus, setSelectedStatus] = useState('New')
  const [noteText, setNoteText] = useState('')
  const [statusLoading, setStatusLoading] = useState(false)
  const [noteLoading, setNoteLoading] = useState(false)
  const [draftLoading, setDraftLoading] = useState(false)
  const [statusMessage, setStatusMessage] = useState('')
  const [statusError, setStatusError] = useState('')
  const [noteMessage, setNoteMessage] = useState('')
  const [noteError, setNoteError] = useState('')
  const [draftMessage, setDraftMessage] = useState('')
  const [draftError, setDraftError] = useState('')

  useEffect(() => {
    if (requestDetail?.status) {
      setSelectedStatus(requestDetail.status)
    }
  }, [requestDetail?.status])

  if (!isOpen) {
    return null
  }

  async function handleStatusUpdate() {
    if (!requestDetail) {
      return
    }

    try {
      setStatusLoading(true)
      setStatusMessage('')
      setStatusError('')

      await updateRequestStatus(requestDetail.id, {
        status: selectedStatus,
        changed_by: 'Sarah Kim',
      })

      await onRefreshRequestDetail(requestDetail.id)
      await onRefreshRequests()
      setStatusMessage('Status updated successfully.')
    } catch (actionError) {
      setStatusError(actionError.message || 'Unable to update status.')
    } finally {
      setStatusLoading(false)
    }
  }

  async function handleSaveNote() {
    if (!requestDetail) {
      return
    }

    const trimmedNote = noteText.trim()

    if (!trimmedNote) {
      setNoteError('Please enter an internal note before saving.')
      setNoteMessage('')
      return
    }

    try {
      setNoteLoading(true)
      setNoteMessage('')
      setNoteError('')

      await addRequestNote(requestDetail.id, {
        author_name: 'Sarah Kim',
        note_text: trimmedNote,
      })

      setNoteText('')
      await onRefreshRequestDetail(requestDetail.id)
      await onRefreshRequests()
      setNoteMessage('Internal note saved.')
    } catch (actionError) {
      setNoteError(actionError.message || 'Unable to save the note.')
    } finally {
      setNoteLoading(false)
    }
  }

  async function handleGenerateDraft() {
    if (!requestDetail) {
      return
    }

    try {
      setDraftLoading(true)
      setDraftMessage('')
      setDraftError('')

      await generateDraftResponse(requestDetail.id, {
        generated_by: 'Sarah Kim',
      })

      await onRefreshRequestDetail(requestDetail.id)
      setDraftMessage('Draft generated successfully.')
    } catch (actionError) {
      setDraftError(actionError.message || 'Unable to generate the draft.')
    } finally {
      setDraftLoading(false)
    }
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
              {requestDetail.requester_name} - {requestDetail.requester_type}
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
          <div className="drawer-section-header">
            <div>
              <h3 className="drawer-section-title">Workflow Actions</h3>
              <p className="drawer-section-copy">
                Update the request, save internal notes, and prepare a donor-safe draft.
              </p>
            </div>
          </div>

          <div className="action-panel">
            <div className="action-block">
              <label className="drawer-control-label" htmlFor="status-select">
                Status
              </label>
              <div className="action-inline-row">
                <select
                  id="status-select"
                  className="drawer-select"
                  value={selectedStatus}
                  onChange={(event) => setSelectedStatus(event.target.value)}
                  disabled={statusLoading}
                >
                  {STATUS_OPTIONS.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
                <button
                  type="button"
                  className="drawer-action-button"
                  disabled={statusLoading}
                  onClick={handleStatusUpdate}
                >
                  {statusLoading ? 'Updating...' : 'Update Status'}
                </button>
              </div>
              {statusMessage ? <p className="drawer-success-text">{statusMessage}</p> : null}
              {statusError ? <p className="drawer-error-text">{statusError}</p> : null}
            </div>

            <div className="action-block">
              <label className="drawer-control-label" htmlFor="internal-note">
                Internal Note
              </label>
              <textarea
                id="internal-note"
                className="drawer-textarea"
                placeholder="Add an internal note for the request timeline"
                value={noteText}
                onChange={(event) => setNoteText(event.target.value)}
                disabled={noteLoading}
                rows={4}
              />
              <div className="action-inline-row action-inline-row-end">
                <button
                  type="button"
                  className="drawer-action-button"
                  disabled={noteLoading}
                  onClick={handleSaveNote}
                >
                  {noteLoading ? 'Saving...' : 'Save Note'}
                </button>
              </div>
              {noteMessage ? <p className="drawer-success-text">{noteMessage}</p> : null}
              {noteError ? <p className="drawer-error-text">{noteError}</p> : null}
            </div>
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
          <div className="drawer-section-header">
            <div>
              <h3 className="drawer-section-title">Latest AI Draft</h3>
              <p className="drawer-section-copy">
                Generate a donor-safe draft for human review.
              </p>
            </div>
            <button
              type="button"
              className="drawer-action-button"
              disabled={draftLoading}
              onClick={handleGenerateDraft}
            >
              {draftLoading ? 'Generating...' : 'Generate Draft Response'}
            </button>
          </div>
          {draftMessage ? <p className="drawer-success-text">{draftMessage}</p> : null}
          {draftError ? <p className="drawer-error-text">{draftError}</p> : null}
          {requestDetail.latest_ai_draft ? (
            <article className="ai-draft-card">
              <p className="ai-draft-warning">
                AI-generated draft. Human review required before sending.
              </p>
              <pre className="ai-draft-text">{requestDetail.latest_ai_draft.draft_text}</pre>
            </article>
          ) : (
            <div className="drawer-empty-block">
              <p className="drawer-empty-title">No AI draft yet</p>
              <p className="drawer-empty-copy">
                A generated donor-safe draft will appear here once the workflow action is used.
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
