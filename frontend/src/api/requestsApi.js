import { fetchJson } from "./client"

export function getRequests() {
  return fetchJson('/api/requests/')
}
