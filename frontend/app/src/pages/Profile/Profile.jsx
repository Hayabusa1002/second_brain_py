import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  IconPencil,
  IconDeviceFloppy,
  IconLock,
  IconMail,
  IconUser,
  IconShield,
  IconClock,
} from '@tabler/icons-react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'

const EMPTY_PROFILE = {
  id: '',
  name: '',
  email: '',
  role: '',
  status: '',
  created_at: '',
  last_login: '',
}

const ROLE_BADGE = {
  admin: 'bg-purple-lt text-purple',
  owner: 'bg-blue-lt text-blue',
  partner: 'bg-teal-lt text-teal',
}

const STATUS_BADGE = {
  active: 'bg-green-lt text-green',
  pending: 'bg-yellow-lt text-yellow',
  inactive: 'bg-secondary-lt text-secondary',
  banned: 'bg-red-lt text-red',
}

const fmtDateTime = (value) => {
  if (!value) return '—'
  try {
    return new Date(value).toLocaleString('es-CO', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return '—'
  }
}

export default function Profile() {
  const navigate = useNavigate()
  const { user: currentUser, setUser } = useAuth?.() ?? { user: null, setUser: () => {} }

  const [profile, setProfile] = useState(EMPTY_PROFILE)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')
  const [isEditing, setIsEditing] = useState(false)

  useEffect(() => {
    fetchProfile()
  }, [])

  async function fetchProfile() {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/auth/me')
      const user = data.user ?? data

      setProfile({
        id: user.id ?? '',
        name: user.name ?? '',
        email: user.email ?? '',
        role: user.role ?? '',
        status: user.status ?? '',
        created_at: user.created_at ?? '',
        last_login: user.last_login ?? user.last_seen ?? '',
      })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load profile.')
    } finally {
      setLoading(false)
    }
  }

  const setField =
    (field) =>
    (e) =>
      setProfile((prev) => ({ ...prev, [field]: e.target.value }))

  async function handleSave(e) {
    e.preventDefault()
    setSaving(true)
    setFormError('')

    try {
      const userId = currentUser?.id ?? profile.id

      const { data } = await client.put(`/users/${userId}`, {
        name: profile.name,
        email: profile.email,
      })

      const updatedUser = data.user ?? data

      if (setUser) {
        setUser((prev) => ({
          ...prev,
          ...updatedUser,
          name: profile.name,
          email: profile.email,
        }))
      }

      setIsEditing(false)
      fetchProfile()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to update profile.')
    } finally {
      setSaving(false)
    }
  }

  function handleCancel() {
    setIsEditing(false)
    setFormError('')
    fetchProfile()
  }

  return (
    <div className="container-xl py-4">
      <div className="page-header d-print-none mb-4">
        <div className="row align-items-center">
          <div className="col">
            <h2 className="page-title mb-1">Profile</h2>
            <div className="text-secondary">
              Manage your personal information and account access.
            </div>
          </div>

          {!loading && !error && (
            <div className="col-auto ms-auto d-flex gap-2">
              <button
                className="btn btn-outline-secondary d-flex align-items-center gap-1"
                onClick={() => navigate('/profile/change-password')}
              >
                <IconLock size={16} stroke={1.5} />
                Change password
              </button>

              {!isEditing && (
                <button
                  className="btn btn-primary d-flex align-items-center gap-1"
                  onClick={() => setIsEditing(true)}
                >
                  <IconPencil size={16} stroke={1.5} />
                  Edit profile
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      <Alert message={error || formError} />

      {loading ? (
        <div className="card">
          <div className="card-body text-secondary">Loading profile...</div>
        </div>
      ) : (
        <div className="row g-4">
          <div className="col-lg-4">
            <div className="card">
              <div className="card-body text-center py-4">
                <span className="avatar avatar-xl mb-3 bg-primary-lt">
                  {profile.name?.trim()?.charAt(0)?.toUpperCase() || 'U'}
                </span>

                <h3 className="m-0">{profile.name || 'User'}</h3>
                <div className="text-secondary mt-1">{profile.email || '—'}</div>

                <div className="mt-3 d-flex justify-content-center gap-2 flex-wrap">
                  {profile.role ? (
                    <span className={`badge ${ROLE_BADGE[profile.role] ?? 'bg-secondary-lt text-secondary'}`}>
                      {profile.role}
                    </span>
                  ) : null}

                  {profile.status ? (
                    <span className={`badge ${STATUS_BADGE[profile.status] ?? 'bg-secondary-lt text-secondary'}`}>
                      {profile.status}
                    </span>
                  ) : null}
                </div>
              </div>

              <div className="card-footer bg-transparent">
                <div className="list-group list-group-flush list-group-hoverable">
                  <div className="list-group-item px-0">
                    <div className="row align-items-center">
                      <div className="col-auto">
                        <IconUser size={18} stroke={1.5} className="text-secondary" />
                      </div>
                      <div className="col text-truncate">
                        <div className="text-secondary small">User ID</div>
                        <div>{profile.id || '—'}</div>
                      </div>
                    </div>
                  </div>

                  <div className="list-group-item px-0">
                    <div className="row align-items-center">
                      <div className="col-auto">
                        <IconShield size={18} stroke={1.5} className="text-secondary" />
                      </div>
                      <div className="col text-truncate">
                        <div className="text-secondary small">Role</div>
                        <div>{profile.role || '—'}</div>
                      </div>
                    </div>
                  </div>

                  <div className="list-group-item px-0">
                    <div className="row align-items-center">
                      <div className="col-auto">
                        <IconClock size={18} stroke={1.5} className="text-secondary" />
                      </div>
                      <div className="col text-truncate">
                        <div className="text-secondary small">Created</div>
                        <div>{fmtDateTime(profile.created_at)}</div>
                      </div>
                    </div>
                  </div>

                  <div className="list-group-item px-0">
                    <div className="row align-items-center">
                      <div className="col-auto">
                        <IconClock size={18} stroke={1.5} className="text-secondary" />
                      </div>
                      <div className="col text-truncate">
                        <div className="text-secondary small">Last login</div>
                        <div>{fmtDateTime(profile.last_login)}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-8">
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Personal information</h3>
              </div>

              <div className="card-body">
                {!isEditing ? (
                  <div className="row g-4">
                    <div className="col-md-6">
                      <label className="form-label">Name</label>
                      <div className="form-control-plaintext">{profile.name || '—'}</div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Email</label>
                      <div className="form-control-plaintext">{profile.email || '—'}</div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Role</label>
                      <div className="form-control-plaintext">{profile.role || '—'}</div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Status</label>
                      <div className="form-control-plaintext">{profile.status || '—'}</div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Created at</label>
                      <div className="form-control-plaintext">{fmtDateTime(profile.created_at)}</div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Last login</label>
                      <div className="form-control-plaintext">{fmtDateTime(profile.last_login)}</div>
                    </div>
                  </div>
                ) : (
                  <form onSubmit={handleSave}>
                    <div className="row g-3">
                      <div className="col-md-6">
                        <label className="form-label">Name</label>
                        <div className="input-icon">
                          <span className="input-icon-addon">
                            <IconUser size={16} stroke={1.5} />
                          </span>
                          <input
                            type="text"
                            className="form-control"
                            value={profile.name}
                            onChange={setField('name')}
                            required
                          />
                        </div>
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Email</label>
                        <div className="input-icon">
                          <span className="input-icon-addon">
                            <IconMail size={16} stroke={1.5} />
                          </span>
                          <input
                            type="email"
                            className="form-control"
                            value={profile.email}
                            onChange={setField('email')}
                            required
                          />
                        </div>
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Role</label>
                        <input
                          type="text"
                          className="form-control"
                          value={profile.role || ''}
                          disabled
                        />
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Status</label>
                        <input
                          type="text"
                          className="form-control"
                          value={profile.status || ''}
                          disabled
                        />
                      </div>
                    </div>

                    <div className="mt-4 d-flex justify-content-between flex-wrap gap-2">
                      <Link
                        to="/profile/change-password"
                        className="btn btn-outline-secondary d-flex align-items-center gap-1"
                      >
                        <IconLock size={16} stroke={1.5} />
                        Change password
                      </Link>

                      <div className="d-flex gap-2">
                        <button
                          type="button"
                          className="btn btn-link"
                          onClick={handleCancel}
                          disabled={saving}
                        >
                          Cancel
                        </button>

                        <button
                          type="submit"
                          className="btn btn-primary d-flex align-items-center gap-1"
                          disabled={saving}
                        >
                          <IconDeviceFloppy size={16} stroke={1.5} />
                          {saving ? 'Saving...' : 'Save changes'}
                        </button>
                      </div>
                    </div>
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}