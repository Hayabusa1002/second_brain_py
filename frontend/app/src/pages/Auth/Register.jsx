import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useTheme } from '../../hooks/useTheme'
import client from '../../api/client'
import PageCenter from '../../components/ui/PageCenter'
import Alert from '../../components/ui/Alert'

// Icons
import { IconBrain, IconEye, IconEyeOff, IconSun, IconMoon } from '@tabler/icons-react'

export default function Register() {
  const navigate = useNavigate()
  const { theme, toggleTheme } = useTheme()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await client.post('/auth/register', form)
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageCenter>

      {/* Theme toggle */}
      <div style={{ position: 'fixed', top: '1rem', right: '1rem' }}>
        <button
          onClick={toggleTheme}
          className="btn btn-outline-secondary btn-icon"
          title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
        >
          {theme === 'light'
            ? <IconMoon size={18} stroke={1.5} />
            : <IconSun size={18} stroke={1.5} />
          }
        </button>
      </div>

      {/* Header */}
      <div className="text-center mb-4">
        <h1 className="h1 d-flex align-items-center justify-content-center gap-2">
          <IconBrain size={36} stroke={1.5} color="#066fd1" />
          Second Brain
        </h1>
      </div>

      {/* Card */}
      <div className="card card-md">
        <div className="card-body">
          <h2 className="h2 text-center mb-4">Create new account</h2>

          <form onSubmit={handleSubmit} autoComplete="off" noValidate>
            <Alert message={error} />

            <div className="mb-3">
              <label className="form-label">Name</label>
              <input
                type="text"
                className="form-control"
                placeholder="Enter your name"
                value={form.name}
                onChange={set('name')}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                placeholder="your@email.com"
                value={form.email}
                onChange={set('email')}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Password</label>
              <div className="input-group input-group-flat">
                <input
                  type={showPassword ? 'text' : 'password'}
                  className="form-control"
                  placeholder="Your password"
                  value={form.password}
                  onChange={set('password')}
                  required
                />
                <span className="input-group-text">
                  <button
                    type="button"
                    className="link-secondary"
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                    onClick={() => setShowPassword(!showPassword)}
                    title={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword
                      ? <IconEyeOff size={20} stroke={1.5} />
                      : <IconEye size={20} stroke={1.5} />
                    }
                  </button>
                </span>
              </div>
            </div>

            <div className="form-footer">
              <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                {loading ? 'Creating account...' : 'Create new account'}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center text-secondary mt-3">
        Already have an account? <Link to="/login">Sign in</Link>
      </div>

    </PageCenter>
  )
}