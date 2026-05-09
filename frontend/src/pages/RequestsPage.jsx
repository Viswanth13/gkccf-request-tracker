import { useEffect, useState } from 'react'
import { getRequestDetail, getRequests } from '../api/requestsApi'
import EmptyState from '../components/common/EmptyState'
import LoadingState from '../components/common/LoadingState'
import CategoryFilters from '../components/dashboard/CategoryFilters'
import MetricCard from '../components/dashboard/MetricCard'
import Sidebar from '../components/layout/Sidebar'
import Topbar from '../components/layout/Topbar'
import RequestDetailDrawer from '../components/requests/RequestDetailDrawer'
import RequestTable from '../components/requests/RequestTable'

function isCompletedThisWeek(request) {
  if (request.status !== 'Completed') {
    return false
  }

  const updatedAt = new Date(request.updated_at)
  const now = new Date()
  const sevenDaysAgo = new Date(now)
  sevenDaysAgo.setDate(now.getDate() - 7)

  return updatedAt >= sevenDaysAgo
}

function formatAverageResponseTime(requests) {
  if (requests.length === 0) {
    return '--'
  }

  const now = new Date()
  const totalHours = requests.reduce((sum, request) => {
    const updatedAt = new Date(request.updated_at)
    const diffInHours = Math.max(1, (now - updatedAt) / (1000 * 60 * 60))
    return sum + diffInHours
  }, 0)
  const averageHours = Math.round(totalHours / requests.length)

  if (averageHours < 24) {
    return `${averageHours}h`
  }

  return `${Math.round(averageHours / 24)}d`
}

function matchesSearch(request, searchText) {
  const normalizedSearch = searchText.trim().toLowerCase()

  if (!normalizedSearch) {
    return true
  }

  const searchableFields = [
    request.request_id,
    request.requester_name,
    request.requester_type,
    request.category,
    request.fund_name,
    request.nonprofit_name,
    request.owner_name,
    request.title,
  ]

  return searchableFields.some((field) =>
    String(field || '').toLowerCase().includes(normalizedSearch),
  )
}

function RequestsPage() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchText, setSearchText] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All Categories')
  const [selectedRequestId, setSelectedRequestId] = useState(null)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [requestDetail, setRequestDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState('')

  async function refreshRequests({ showLoading = false } = {}) {
    try {
      if (showLoading) {
        setLoading(true)
      }

      setError('')
      const data = await getRequests()
      setRequests(data)
    } catch (loadError) {
      setError(
        loadError.message ||
          'Unable to load requests. Please confirm the backend is running.',
      )
    } finally {
      if (showLoading) {
        setLoading(false)
      }
    }
  }

  async function refreshRequestDetail(requestId = selectedRequestId) {
    if (!requestId) {
      return
    }

    try {
      setDetailLoading(true)
      setDetailError('')
      const data = await getRequestDetail(requestId)
      setRequestDetail(data)
    } catch (loadError) {
      setDetailError(
        loadError.message ||
          'Unable to load request details. Please confirm the backend is running.',
      )
    } finally {
      setDetailLoading(false)
    }
  }

  useEffect(() => {
    refreshRequests({ showLoading: true })
  }, [])

  useEffect(() => {
    if (!isDrawerOpen || !selectedRequestId) {
      return
    }

    refreshRequestDetail(selectedRequestId)
  }, [isDrawerOpen, selectedRequestId])

  function handleRowSelect(requestId) {
    setSelectedRequestId(requestId)
    setRequestDetail(null)
    setDetailError('')
    setIsDrawerOpen(true)
  }

  function handleCloseDrawer() {
    setIsDrawerOpen(false)
  }

  const filteredRequests = requests.filter((request) => {
    const matchesCategory =
      selectedCategory === 'All Categories' || request.category === selectedCategory

    return matchesCategory && matchesSearch(request, searchText)
  })

  const openRequests = requests.filter((request) => request.status !== 'Completed').length
  const waitingOnDonor = requests.filter(
    (request) => request.status === 'Waiting on Donor',
  ).length
  const completedThisWeek = requests.filter(isCompletedThisWeek).length
  const averageResponseTime = formatAverageResponseTime(requests)

  let content = (
    <RequestTable
      requests={filteredRequests}
      selectedRequestId={selectedRequestId}
      onRowSelect={handleRowSelect}
    />
  )

  if (loading) {
    content = <LoadingState message="Pulling service requests from the backend API." />
  } else if (error) {
    content = (
      <EmptyState
        title="Backend unavailable"
        message={`${error} Start the Django server at http://127.0.0.1:8000 and refresh this page.`}
      />
    )
  } else if (filteredRequests.length === 0) {
    content = (
      <EmptyState
        title="No matching requests"
        message="Try a different search term or switch back to All Categories."
      />
    )
  }

  return (
    <div className={`dashboard-layout${isDrawerOpen ? ' has-drawer-open' : ''}`}>
      <Sidebar />

      <div className="dashboard-panel">
        <Topbar searchText={searchText} onSearchChange={setSearchText} />

        <main className="dashboard-content">
          <section className="page-heading">
            <div>
              <p className="eyebrow">Internal workflow dashboard</p>
              <h1>Service Requests</h1>
            </div>
            <p className="page-summary">
              Track donor and advisor requests, spot missing information, and
              prepare the team for the next workflow actions.
            </p>
          </section>

          <section className="metrics-grid" aria-label="Dashboard metrics">
            <MetricCard
              label="Open Requests"
              value={openRequests}
              helperText="All requests still in progress"
            />
            <MetricCard
              label="Waiting on Donor"
              value={waitingOnDonor}
              helperText="Cases blocked on external follow-up"
            />
            <MetricCard
              label="Completed This Week"
              value={completedThisWeek}
              helperText="Completed in the last 7 days"
            />
            <MetricCard
              label="Average Response Time"
              value={averageResponseTime}
              helperText="Based on recent request activity"
            />
          </section>

          <section className="table-section">
            <div className="section-header">
              <div>
                <h2>Request Queue</h2>
                <p className="section-copy">
                  Search and filter the current service request pipeline.
                </p>
              </div>
              <div className="result-pill">{filteredRequests.length} visible</div>
            </div>

            <CategoryFilters
              selectedCategory={selectedCategory}
              onCategoryChange={setSelectedCategory}
            />

            {content}
          </section>
        </main>
      </div>

      <RequestDetailDrawer
        isOpen={isDrawerOpen}
        requestDetail={requestDetail}
        loading={detailLoading}
        error={detailError}
        onClose={handleCloseDrawer}
        onRefreshRequestDetail={refreshRequestDetail}
        onRefreshRequests={refreshRequests}
      />
    </div>
  )
}

export default RequestsPage
