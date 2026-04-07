import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { useTheme } from '../../hooks/useTheme'
import {
  IconBrain,
  IconHome,
  IconReceipt,
  IconUser,
  IconLogout,
  IconSun,
  IconMoon,
  IconBuildingBank,
  IconUsers,
  IconLock,
  IconShieldPlus,
  IconCategory,
  IconMapPin,
  IconPackage,
  IconBuildingStore,
} from '@tabler/icons-react'

const BASE_NAV_ITEMS = [
  { path: '/', label: 'Home', icon: <IconHome size={16} stroke={1.5} /> },
  { path: '/transactions', label: 'Transactions', icon: <IconReceipt size={16} stroke={1.5} /> },
  { path: '/accounts', label: 'Accounts', icon: <IconBuildingBank size={16} stroke={1.5} /> },
]

const ADMIN_NAV_ITEMS = [
  { path: '/users', label: 'Users', icon: <IconUsers size={16} stroke={1.5} /> },
  { path: '/access-requests', label: 'Access requests', icon: <IconShieldPlus size={16} stroke={1.5} /> },
  { path: '/categories', label: 'Categories', icon: <IconCategory size={16} stroke={1.5} /> },
  { path: '/stores', label: 'Stores', icon: <IconBuildingStore size={16} stroke={1.5} /> },
  { path: '/cities', label: 'Cities', icon: <IconMapPin size={16} stroke={1.5} /> },
  { path: '/items', label: 'Items', icon: <IconPackage size={16} stroke={1.5} /> },
]

export default function Navbar() {
  const { user, logout } = useAuth()
  const location = useLocation()
  const { theme, toggleTheme } = useTheme()
  const [dropdownOpen, setDropdownOpen] = useState(false)

  const navItems =
    user?.role === 'admin'
      ? [...BASE_NAV_ITEMS, ...ADMIN_NAV_ITEMS]
      : BASE_NAV_ITEMS

  useEffect(() => {
    function handleClickOutside(e) {
      if (!e.target.closest('#user-dropdown')) {
        setDropdownOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <>
      <header className="navbar navbar-expand-md d-print-none">
        <div className="container-xl">
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbar-menu"
            aria-controls="navbar-menu"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon" />
          </button>

          <Link to="/" className="navbar-brand navbar-brand-autodark me-auto">
            <IconBrain size={24} stroke={1.5} color="#066fd1" className="me-2" />
            <span className="fw-bold fs-4">Second Brain</span>
          </Link>

          <div className="navbar-nav flex-row order-md-last gap-2 align-items-center">
            <div className="nav-item">
              <button
                className="nav-link px-2 d-flex align-items-center"
                onClick={toggleTheme}
                title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
                style={{ background: 'none', border: 'none', cursor: 'pointer' }}
              >
                {theme === 'light' ? (
                  <IconMoon size={20} stroke={1.5} />
                ) : (
                  <IconSun size={20} stroke={1.5} />
                )}
              </button>
            </div>

            <div className="nav-item d-none d-md-flex align-items-center">
              <div className="text-center" style={{ lineHeight: 1.2 }}>
                <div className="small text-secondary" style={{ fontSize: '0.65rem' }}>
                  Role
                </div>
                <span className="badge bg-blue-lt text-blue">{user?.role ?? 'user'}</span>
              </div>
            </div>

            <div className="d-none d-md-flex">
              <div
                className="nav-item dropdown"
                id="user-dropdown"
                style={{ position: 'relative' }}
              >
                <a
                  href="#"
                  className="nav-link d-flex lh-1 text-reset p-0"
                  onClick={(e) => {
                    e.preventDefault()
                    setDropdownOpen((o) => !o)
                  }}
                  aria-label="Open user menu"
                >
                  <span
                    className="avatar avatar-sm"
                    style={{ backgroundColor: '#206bc4', color: '#fff' }}
                  >
                    {user?.name?.charAt(0).toUpperCase() || 'U'}
                  </span>

                  <div className="d-none d-xl-block ps-2">
                    <div className="fw-medium">{user?.name || 'User'}</div>
                    <div className="mt-1 small text-secondary">{user?.email || ''}</div>
                  </div>
                </a>

                <div
                  className={`dropdown-menu dropdown-menu-end dropdown-menu-arrow ${dropdownOpen ? 'show' : ''}`}
                  style={{ top: '100%', bottom: 'auto' }}
                >
                  <Link
                    to="/profile"
                    className="dropdown-item d-flex align-items-center gap-2"
                    onClick={() => setDropdownOpen(false)}
                  >
                    <IconUser size={16} stroke={1.5} />
                    Profile
                  </Link>

                  <Link
                    to="/profile/change-password"
                    className="dropdown-item d-flex align-items-center gap-2"
                    onClick={() => setDropdownOpen(false)}
                  >
                    <IconLock size={16} stroke={1.5} />
                    Change password
                  </Link>

                  <div className="dropdown-divider" />

                  <button
                    className="dropdown-item d-flex align-items-center gap-2 text-danger"
                    onClick={logout}
                  >
                    <IconLogout size={16} stroke={1.5} />
                    Sign out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <header className="navbar-expand-md">
        <div className="collapse navbar-collapse" id="navbar-menu">
          <div className="navbar">
            <div className="container-xl">
              <ul className="navbar-nav">
                {navItems.map(({ path, label, icon }) => {
                  const isActive =
                    path === '/'
                      ? location.pathname === '/'
                      : location.pathname === path || location.pathname.startsWith(`${path}/`)

                  return (
                    <li key={path} className={`nav-item ${isActive ? 'active' : ''}`}>
                      <Link className="nav-link" to={path}>
                        <span className="nav-link-icon d-md-none d-lg-inline-block">
                          {icon}
                        </span>
                        <span className="nav-link-title">{label}</span>
                      </Link>
                    </li>
                  )
                })}
              </ul>

              <div className="d-md-none border-top pt-2 mt-2 w-100">
                <div className="d-flex align-items-center px-3 py-2 gap-2">
                  <span
                    className="avatar avatar-sm"
                    style={{ backgroundColor: '#206bc4', color: '#fff' }}
                  >
                    {user?.name?.charAt(0).toUpperCase() || 'U'}
                  </span>

                  <div className="flex-fill">
                    <div className="fw-medium">{user?.name || 'User'}</div>
                    <div className="small text-secondary">{user?.email || ''}</div>
                  </div>

                  <span className="badge bg-blue-lt text-blue">{user?.role ?? 'user'}</span>
                </div>

                <Link to="/profile" className="dropdown-item d-flex align-items-center gap-2">
                  <IconUser size={16} stroke={1.5} />
                  Profile
                </Link>

                <Link
                  to="/profile/change-password"
                  className="dropdown-item d-flex align-items-center gap-2"
                >
                  <IconLock size={16} stroke={1.5} />
                  Change password
                </Link>

                <div className="dropdown-divider" />

                <button
                  className="dropdown-item d-flex align-items-center gap-2 text-danger w-100"
                  onClick={logout}
                >
                  <IconLogout size={16} stroke={1.5} />
                  Sign out
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>
    </>
  )
}