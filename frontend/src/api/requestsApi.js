import { fetchJson } from "./client"

export function getRequests() {
  return fetchJson('/api/requests/')
}

export function getRequestDetail(id) {
  return fetchJson(`/api/requests/${id}/`)
}

export function addRequestNote(id, payload) {
  return fetchJson(`/api/requests/${id}/notes/`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateRequestStatus(id, payload) {
  return fetchJson(`/api/requests/${id}/status/`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function generateDraftResponse(id, payload) {
  return fetchJson(`/api/requests/${id}/generate-draft/`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
