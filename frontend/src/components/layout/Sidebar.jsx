const navItems = [
  'Dashboard',
  'Requests',
  'Donors',
  'Advisors',
  'Companies',
  'Reports',
  'AI Tools',
  'Settings',
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
            key={item}
            type="button"
            className={`sidebar-link${item === 'Requests' ? ' is-active' : ''}`}
          >
            <span className="sidebar-link-dot" aria-hidden="true" />
            <span>{item}</span>
          </button>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
