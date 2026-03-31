// src/pages/Profile/ChangePassword.jsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { IconLock, IconEye, IconEyeOff, IconArrowLeft } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'

export default function ChangePassword() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  })
  const [show, setShow] = useState({
    current: false,
    new: false,
    confirm: false,
  })
  const [error, setError]     = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })
  const toggleShow = (field) => setShow(s => ({ ...s, [field]: !s[field] }))

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (form.new_password !== form.confirm_password) {
      setError('New passwords do not match.')
      return
    }
    if (form.new_password.length < 8) {
      setError('New password must be at least 8 characters.')
      return
    }

    setLoading(true)
    try {
      await client.put('/auth/password', {
        current_password: form.current_password,
        new_password: form.new_password,
      })
      setSuccess('Password updated successfully.')
      setForm({ current_password: '', new_password: '', confirm_password: '' })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update password.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container-xl">

      {/* Page header */}
      <div className="page-header d-print-none">
        <div className="row align-items-center">
          <div className="col">
            <div className="page-pretitle">Profile</div>
            <h2 className="page-title">Change Password</h2>
          </div>
          <div className="col-auto ms-auto">
            <button className="btn d-flex align-items-center gap-2"
              onClick={() => navigate(-1)}>
              <IconArrowLeft size={16} stroke={1.5} />
              Back
            </button>
          </div>
        </div>
      </div>

      <div className="page-body">
        <div className="row justify-content-center">
          <div className="col-md-6 col-lg-5">
            <div className="card">
              <div className="card-header">
                <div className="d-flex align-items-center gap-2">
                  <IconLock size={20} stroke={1.5} className="text-muted" />
                  <h3 className="card-title">Update your password</h3>
                </div>
              </div>
              <div className="card-body">
                <form onSubmit={handleSubmit} autoComplete="off" noValidate>

                  <Alert message={error} type="danger" />
                  <Alert message={success} type="success" />

                  {/* Current password */}
                  <div className="mb-3">
                    <label className="form-label">Current password</label>
                    <div className="input-group input-group-flat">
                      <input
                        type={show.current ? 'text' : 'password'}
                        className="form-control"
                        placeholder="Enter current password"
                        value={form.current_password}
                        onChange={set('current_password')}
                        required
                      />
                      <span className="input-group-text">
                        <button type="button" className="link-secondary"
                          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                          onClick={() => toggleShow('current')}>
                          {show.current ? <IconEyeOff size={20} stroke={1.5} /> : <IconEye size={20} stroke={1.5} />}
                        </button>
                      </span>
                    </div>
                  </div>

                  {/* New password */}
                  <div className="mb-3">
                    <label className="form-label">New password</label>
                    <div className="input-group input-group-flat">
                      <input
                        type={show.new ? 'text' : 'password'}
                        className="form-control"
                        placeholder="Enter new password"
                        value={form.new_password}
                        onChange={set('new_password')}
                        required
                      />
                      <span className="input-group-text">
                        <button type="button" className="link-secondary"
                          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                          onClick={() => toggleShow('new')}>
                          {show.new ? <IconEyeOff size={20} stroke={1.5} /> : <IconEye size={20} stroke={1.5} />}
                        </button>
                      </span>
                    </div>
                    <small className="form-hint">Minimum 8 characters.</small>
                  </div>

                  {/* Confirm new password */}
                  <div className="mb-4">
                    <label className="form-label">Confirm new password</label>
                    <div className="input-group input-group-flat">
                      <input
                        type={show.confirm ? 'text' : 'password'}
                        className="form-control"
                        placeholder="Repeat new password"
                        value={form.confirm_password}
                        onChange={set('confirm_password')}
                        required
                      />
                      <span className="input-group-text">
                        <button type="button" className="link-secondary"
                          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                          onClick={() => toggleShow('confirm')}>
                          {show.confirm ? <IconEyeOff size={20} stroke={1.5} /> : <IconEye size={20} stroke={1.5} />}
                        </button>
                      </span>
                    </div>
                  </div>

                  <div className="form-footer">
                    <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                      {loading ? 'Updating...' : 'Update password'}
                    </button>
                  </div>

                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}