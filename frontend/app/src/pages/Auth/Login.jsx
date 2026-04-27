import { Link } from 'react-router-dom'
import { useTheme } from '../../hooks/useTheme'
import useLoginForm from '../../hooks/auth/useLogin'
import PageCenter from '../../components/ui/PageCenter'
import Alert from '../../components/ui/Alert'

import { IconBrain, IconEye, IconEyeOff, IconSun, IconMoon } from '@tabler/icons-react'
import { FcGoogle } from 'react-icons/fc'
import { FaGithub } from 'react-icons/fa'

const API_URL = import.meta.env.VITE_API_URL

export default function Login() {
  const { theme, toggleTheme } = useTheme()

  const {
    form,
    showPassword,
    error,
    fieldErrors,
    loading,
    handleChange,
    handleSubmit,
    togglePassword,
  } = useLoginForm()

  return (
    <PageCenter>
      <div style={{ position: 'fixed', top: '1rem', right: '1rem' }}>
        <button
          onClick={toggleTheme}
          className="btn btn-outline-secondary btn-icon"
          title={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
          type="button"
        >
          {theme === 'light'
            ? <IconMoon size={18} stroke={1.5} />
            : <IconSun size={18} stroke={1.5} />
          }
        </button>
      </div>

      <div className="text-center mb-4">
        <h1 className="h1 d-flex align-items-center justify-content-center gap-2">
          <IconBrain size={36} stroke={1.5} color="#066fd1" />
          Second Brain
        </h1>
      </div>

      <div className="card card-md">
        <div className="card-body">
          <h2 className="h2 text-center mb-4">Login to your account</h2>

          <form onSubmit={handleSubmit} autoComplete="off" noValidate>
            <Alert message={error} />

            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className={`form-control ${fieldErrors.email ? 'is-invalid' : ''}`}
                placeholder="your@email.com"
                value={form.email}
                onChange={handleChange('email')}
                required
              />
              {fieldErrors.email && (
                <div className="invalid-feedback d-block">{fieldErrors.email}</div>
              )}
            </div>

            <div className="mb-2">
              <label className="form-label">
                Password
                <span className="form-label-description">
                  <a href="#">I forgot password</a>
                </span>
              </label>

              <div className="input-group input-group-flat">
                <input
                  type={showPassword ? 'text' : 'password'}
                  className={`form-control ${fieldErrors.password ? 'is-invalid' : ''}`}
                  placeholder="Your password"
                  value={form.password}
                  onChange={handleChange('password')}
                  required
                />
                <span className="input-group-text">
                  <button
                    type="button"
                    className="link-secondary"
                    style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                    onClick={togglePassword}
                    title={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword
                      ? <IconEyeOff size={20} stroke={1.5} />
                      : <IconEye size={20} stroke={1.5} />
                    }
                  </button>
                </span>
              </div>
              {fieldErrors.password && (
                <div className="invalid-feedback d-block">{fieldErrors.password}</div>
              )}
            </div>

            <div className="mb-2">
              <label className="form-check">
                <input type="checkbox" className="form-check-input" />
                <span className="form-check-label">Remember me on this device</span>
              </label>
            </div>

            <div className="form-footer">
              <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
            </div>
          </form>
        </div>

        <div className="hr-text">or</div>

        <div className="card-body">
          <div className="row">
            <div className="col">
              <a href={`${API_URL}/api/auth/github`} className="btn btn-4 w-100">
                <FaGithub size={20} className="me-2" />
                Login with Github
              </a>
            </div>
            <div className="col">
              <a href={`${API_URL}/api/auth/google`} className="btn btn-4 w-100">
                <FcGoogle size={20} className="me-2" />
                Login with Google
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="text-center text-secondary mt-3">
        Don&apos;t have account yet? <Link to="/register">Sign up</Link>
      </div>
    </PageCenter>
  )
}