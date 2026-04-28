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
import Alert from '../../components/ui/Alert'
import useProfile from '../../hooks/profile/useProfile'
import formatDateTime from '../../utils/profile/profile/formatDateTime'

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

export default function Profile() {
  const navigate = useNavigate()

  const {
    profile,
    loading,
    error,
    saving,
    formError,
    fieldErrors,
    success,
    isEditing,
    setIsEditing,
    setField,
    handleSave,
    handleCancel,
  } = useProfile()

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
                type="button"
                className="btn btn-outline-secondary d-flex align-items-center gap-1"
                onClick={() => navigate('/profile/change-password')}
              >
                <IconLock size={16} stroke={1.5} />
                Change password
              </button>

              {!isEditing && (
                <button
                  type="button"
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

      <Alert message={error || formError} type="danger" />
      <Alert message={success} type="success" />

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
                    <span
                      className={`badge ${
                        ROLE_BADGE[profile.role] ?? 'bg-secondary-lt text-secondary'
                      }`}
                    >
                      {profile.role}
                    </span>
                  ) : null}

                  {profile.status ? (
                    <span
                      className={`badge ${
                        STATUS_BADGE[profile.status] ?? 'bg-secondary-lt text-secondary'
                      }`}
                    >
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
                        <div>{formatDateTime(profile.created_at)}</div>
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
                        <div>{formatDateTime(profile.last_login)}</div>
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
                      <div className="form-control-plaintext">
                        {profile.role ? (
                          <span
                            className={`badge ${
                              ROLE_BADGE[profile.role] ?? 'bg-secondary-lt text-secondary'
                            }`}
                          >
                            {profile.role}
                          </span>
                        ) : '—'}
                      </div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Status</label>
                      <div className="form-control-plaintext">
                        {profile.status ? (
                          <span
                            className={`badge ${
                              STATUS_BADGE[profile.status] ?? 'bg-secondary-lt text-secondary'
                            }`}
                          >
                            {profile.status}
                          </span>
                        ) : '—'}
                      </div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Created at</label>
                      <div className="form-control-plaintext">
                        {formatDateTime(profile.created_at)}
                      </div>
                    </div>

                    <div className="col-md-6">
                      <label className="form-label">Last login</label>
                      <div className="form-control-plaintext">
                        {formatDateTime(profile.last_login)}
                      </div>
                    </div>
                  </div>
                ) : (
                  <form onSubmit={handleSave} noValidate>
                    <div className="row g-3">
                      <div className="col-md-6">
                        <label className="form-label">Name</label>
                        <div className="input-icon">
                          <span className="input-icon-addon">
                            <IconUser size={16} stroke={1.5} />
                          </span>
                          <input
                            type="text"
                            className={`form-control ${fieldErrors.name ? 'is-invalid' : ''}`}
                            value={profile.name}
                            onChange={setField('name')}
                            required
                          />
                        </div>
                        {fieldErrors.name && (
                          <div className="invalid-feedback d-block">{fieldErrors.name}</div>
                        )}
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Email</label>
                        <div className="input-icon">
                          <span className="input-icon-addon">
                            <IconMail size={16} stroke={1.5} />
                          </span>
                          <input
                            type="email"
                            className={`form-control ${fieldErrors.email ? 'is-invalid' : ''}`}
                            value={profile.email}
                            onChange={setField('email')}
                            required
                          />
                        </div>
                        {fieldErrors.email && (
                          <div className="invalid-feedback d-block">{fieldErrors.email}</div>
                        )}
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Role</label>
                        <div className="form-control-plaintext">
                          {profile.role ? (
                            <span
                              className={`badge ${
                                ROLE_BADGE[profile.role] ?? 'bg-secondary-lt text-secondary'
                              }`}
                            >
                              {profile.role}
                            </span>
                          ) : '—'}
                        </div>
                      </div>

                      <div className="col-md-6">
                        <label className="form-label">Status</label>
                        <div className="form-control-plaintext">
                          {profile.status ? (
                            <span
                              className={`badge ${
                                STATUS_BADGE[profile.status] ?? 'bg-secondary-lt text-secondary'
                              }`}
                            >
                              {profile.status}
                            </span>
                          ) : '—'}
                        </div>
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