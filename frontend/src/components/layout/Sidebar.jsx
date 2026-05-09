import React from 'react'

const navItems = [
  { label: 'Dashboard', comingSoon: true },
  { label: 'Requests', active: true },
  { label: 'Donors', comingSoon: true },
  { label: 'Advisors', comingSoon: true },
  { label: 'Companies', comingSoon: true },
  { label: 'Reports', comingSoon: true },
  { label: 'AI Tools', comingSoon: true },
  { label: 'Settings', comingSoon: true },
]

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand-block">
        <div className="brand-mark">GK</div>
        <div>
          <p className="brand-name">GKCCF</p>
          <p className="brand-subtitle">Internal Request Tracker</p>
        </div>
      </div>

      <nav className="sidebar-nav" aria-label="Primary">
        {navItems.map((item) => (
          <button
            key={item.label}
            type="button"
            className={[
              'sidebar-link',
              item.active ? 'is-active' : '',
              item.comingSoon ? 'is-disabled' : '',
            ]
              .filter(Boolean)
              .join(' ')}
            aria-disabled={item.comingSoon ? 'true' : 'false'}
          >
            <span className="sidebar-link-dot" aria-hidden="true" />
            <span>{item.label}</span>
            {item.comingSoon ? (
              <span className="sidebar-link-tag">Coming soon</span>
            ) : null}
          </button>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
