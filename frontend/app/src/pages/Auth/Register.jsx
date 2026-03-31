import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import client from '../../api/client'
import PageCenter from '../../components/ui/PageCenter'
import Card from '../../components/ui/Card'
import Alert from '../../components/ui/Alert'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [agreed, setAgreed] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  async function handleSubmit(e) {
    e.preventDefault()
    if (!agreed) {
      setError('You must agree to the terms and policy.')
      return
    }
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
      <div className="text-center mb-4">
        <span className="h2 fw-bold text-primary">Second Brain</span>
      </div>

      <Card>
        <h2 className="card-title text-center mb-4">Create new account</h2>

        <form onSubmit={handleSubmit}>
          <Alert message={error} />

          <div className="mb-3">
            <label className="form-label">Name</label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter name"
              value={form.name}
              onChange={set('name')}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Email address</label>
            <input
              type="email"
              className="form-control"
              placeholder="Enter email"
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
                placeholder="Password"
                value={form.password}
                onChange={set('password')}
                required
              />
              <span className="input-group-text">
                <button
                  type="button"
                  className="link-secondary"
                  style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                  onClick={() => setShowPassword(!showPassword)}
                  title={showPassword ? 'Hide password' : 'Show password'}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    {showPassword
                      ? <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755q-.247.248-.517.486z M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829m-3.58 1.261C3.001 11.246 2 9.986 2 8c0-1 .5-2 1-3" />
                      : <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z" />
                    }
                    {!showPassword && <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0" />}
                  </svg>
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
      </Card>

      <div className="text-center text-secondary mt-3">
        Already have account? <Link to="/login">Sign in</Link>
      </div>
    </PageCenter>
  )
}