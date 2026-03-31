import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const NAV_ITEMS = [
  { path: '/', label: 'Home' },
  { path: '/transactions', label: 'Transactions' },
]

export default function Navbar() {
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <header className="navbar navbar-expand-md navbar-light d-print-none">
      <div className="container-xl">

        <a href="/" className="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
          <span className="fw-bold text-primary fs-4">Second Brain</span>
        </a>

        <div className="navbar-nav flex-row order-md-last">
          <div className="nav-item dropdown">
            <a
              href="#"
              className="nav-link d-flex lh-1 text-reset p-0"
              data-bs-toggle="dropdown"
              aria-label="Open user menu"
            >
              <span
                className="avatar avatar-sm"
                style={{ backgroundImage: 'none', backgroundColor: '#206bc4', color: '#fff' }}
              >
                {user?.name?.charAt(0).toUpperCase() || 'U'}
              </span>
              <div className="d-none d-xl-block ps-2">
                <div>{user?.name || 'User'}</div>
                <div className="mt-1 small text-secondary">{user?.email || ''}</div>
              </div>
            </a>
            <div className="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
              <Link to="/profile" className="dropdown-item">Profile</Link>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item text-danger" onClick={handleLogout}>
                Sign out
              </button>
            </div>
          </div>
        </div>

        <div className="collapse navbar-collapse" id="navbar-menu">
          <div className="d-flex flex-column flex-md-row flex-fill align-items-stretch align-items-md-center">
            <ul className="navbar-nav">
              {NAV_ITEMS.map(({ path, label }) => (
                <li>
                  <Link className="nav-link" to={path}>
                    <span className="nav-link-title">{label}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

      </div>
    </header>
  )
}