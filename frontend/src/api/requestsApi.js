import { fetchJson } from "./client"

export function getRequests() {
  return fetchJson('/api/requests/')
}

export function getRequestDetail(id) {
  return fetchJson(`/api/requests/${id}/`)
}
