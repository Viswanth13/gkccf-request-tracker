import React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import RequestsPage from './RequestsPage'

vi.mock('../api/requestsApi', () => ({
  getRequests: vi.fn(),
  getRequestDetail: vi.fn(),
  addRequestNote: vi.fn(),
  updateRequestStatus: vi.fn(),
  generateDraftResponse: vi.fn(),
}))

import {
  addRequestNote,
  generateDraftResponse,
  getRequestDetail,
  getRequests,
  updateRequestStatus,
} from '../api/requestsApi'

const requestRows = [
  {
    id: 1,
    request_id: 'REQ-2025-1042',
    title: 'Grant recommendation help',
    requester_name: 'Mary Smith',
    requester_type: 'Donor',
    category: 'Grant Help',
    fund_name: 'Smith Family Fund',
    grant_amount: '5000.00',
    nonprofit_name: 'Local Youth Arts Collective',
    missing_information: 'Missing EIN and mailing address',
    owner_name: 'Sarah Kim',
    priority: 'Medium',
    status: 'Waiting on Donor',
    updated_at: '2026-05-08T12:00:00Z',
  },
  {
    id: 2,
    request_id: 'REQ-2025-1041',
    title: 'Fund balance question',
    requester_name: 'John Davis',
    requester_type: 'Donor',
    category: 'Fund Question',
    fund_name: 'Davis Family Fund',
    grant_amount: null,
    nonprofit_name: null,
    missing_information: '',
    owner_name: 'Michael Lee',
    priority: 'Low',
    status: 'In Review',
    updated_at: '2026-05-08T09:00:00Z',
  },
]

const requestDetail = {
  id: 1,
  request_id: 'REQ-2025-1042',
  title: 'Grant recommendation help',
  requester_name: 'Mary Smith',
  requester_type: 'Donor',
  category: 'Grant Help',
  fund_name: 'Smith Family Fund',
  grant_amount: '5000.00',
  nonprofit_name: 'Local Youth Arts Collective',
  missing_information: 'Missing EIN and mailing address',
  owner: {
    id: 1,
    name: 'Sarah Kim',
    role: 'Donor Services',
    email: 'sarah.kim@gkccf-demo.org',
    avatar_url: null,
  },
  priority: 'Medium',
  status: 'Waiting on Donor',
  description: 'Grant review blocked on missing nonprofit details.',
  created_at: '2026-05-08T10:00:00Z',
  updated_at: '2026-05-08T12:00:00Z',
  notes: [],
  status_history: [],
  latest_ai_draft: null,
}

function deferredPromise() {
  let resolve
  const promise = new Promise((resolver) => {
    resolve = resolver
  })

  return { promise, resolve }
}

describe('RequestsPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    getRequests.mockResolvedValue(requestRows)
    getRequestDetail.mockResolvedValue(requestDetail)
    addRequestNote.mockResolvedValue({
      id: 99,
      author_name: 'Sarah Kim',
      note_type: 'note',
      note_text: 'Follow-up note',
      created_at: '2026-05-08T12:30:00Z',
    })
    updateRequestStatus.mockResolvedValue({
      id: 1,
      request_id: 'REQ-2025-1042',
      old_status: 'In Review',
      new_status: 'Waiting on Donor',
      message: 'Status updated successfully',
    })
    generateDraftResponse.mockResolvedValue({
      id: 1,
      draft_text: 'AI-generated draft. Human review required before sending.',
      human_review_required: true,
      created_at: '2026-05-08T12:45:00Z',
    })
  })

  it('shows loading state initially', () => {
    const pending = deferredPromise()
    getRequests.mockReturnValueOnce(pending.promise)

    render(<RequestsPage />)

    expect(screen.getByText('Loading dashboard')).toBeInTheDocument()
    expect(
      screen.getByText('Pulling service requests from the backend API.'),
    ).toBeInTheDocument()

    pending.resolve(requestRows)
  })

  it('fetches and renders request rows from mocked API data', async () => {
    render(<RequestsPage />)

    expect(await screen.findByText('REQ-2025-1042')).toBeInTheDocument()
    expect(screen.getByText('REQ-2025-1041')).toBeInTheDocument()
    expect(screen.getByText('Mary Smith')).toBeInTheDocument()
    expect(screen.getByText('John Davis')).toBeInTheDocument()
  })

  it('filters visible request rows with search', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')

    fireEvent.change(screen.getByPlaceholderText(/search by requester/i), {
      target: { value: 'Mary' },
    })

    expect(screen.getByText('REQ-2025-1042')).toBeInTheDocument()
    expect(screen.queryByText('REQ-2025-1041')).not.toBeInTheDocument()
  })

  it('filters visible request rows by category chip', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')

    fireEvent.click(screen.getByRole('button', { name: 'Fund Question' }))

    expect(screen.getByText('REQ-2025-1041')).toBeInTheDocument()
    expect(screen.queryByText('REQ-2025-1042')).not.toBeInTheDocument()
  })

  it('shows empty state when no rows match', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')

    fireEvent.change(screen.getByPlaceholderText(/search by requester/i), {
      target: { value: 'No match value' },
    })

    expect(screen.getByText('No matching requests')).toBeInTheDocument()
  })

  it('clicking a request row fetches detail and opens the drawer', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')

    fireEvent.click(screen.getByText('REQ-2025-1042'))

    await waitFor(() => {
      expect(getRequestDetail).toHaveBeenCalledWith(1)
    })

    expect(await screen.findByText('Grant recommendation help')).toBeInTheDocument()
    expect(screen.getByText('Workflow Actions')).toBeInTheDocument()
  })

  it('drawer shows missing information warning when present', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')
    fireEvent.click(screen.getByText('REQ-2025-1042'))

    expect(await screen.findByText('Missing information')).toBeInTheDocument()
    expect(screen.getByText('Missing EIN and mailing address')).toBeInTheDocument()
  })

  it('empty note submission shows client-side validation', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')
    fireEvent.click(screen.getByText('REQ-2025-1042'))
    await screen.findByText('Workflow Actions')

    fireEvent.click(screen.getByRole('button', { name: 'Save Note' }))

    expect(
      screen.getByText('Please enter an internal note before saving.'),
    ).toBeInTheDocument()
    expect(addRequestNote).not.toHaveBeenCalled()
  })

  it('Generate Draft button renders in the drawer', async () => {
    render(<RequestsPage />)

    await screen.findByText('REQ-2025-1042')
    fireEvent.click(screen.getByText('REQ-2025-1042'))

    expect(
      await screen.findByRole('button', { name: 'Generate Draft Response' }),
    ).toBeInTheDocument()
  })
})
