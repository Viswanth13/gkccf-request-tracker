import React from 'react'

function Topbar({ searchText, onSearchChange }) {
  return (
    <header className="topbar">
      <label className="search-field" htmlFor="request-search">
        <span className="search-icon" aria-hidden="true">
          Search
        </span>
        <input
          id="request-search"
          type="search"
          value={searchText}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search by requester, fund, nonprofit, request ID, or category"
        />
      </label>

      <div className="topbar-actions">
        <button type="button" className="notification-button" aria-label="Notifications">
          <span className="notification-label">Notifications</span>
          <span className="notification-badge" />
        </button>

        <div className="profile-pill">
          <div className="profile-avatar">SK</div>
          <div>
            <p className="profile-name">Sarah Kim</p>
            <p className="profile-role">Donor Services</p>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Topbar
