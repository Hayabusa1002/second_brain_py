import { useState } from 'react'
import { IconEye, IconEyeOff } from '@tabler/icons-react'

const ROLES = ['partner', 'owner', 'admin']

export default function FormModal({
  form,
  mode,
  saving,
  error,
  onChange,
  onSave,
  onCancel,
}) {
  const [showPassword, setShowPassword] = useState(false)

  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              {mode === 'edit' ? 'Edit user' : 'New user'}
            </h5>
            <button className="btn-close" onClick={onCancel} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger mb-3">{error}</div>}

            <form id="user-form" onSubmit={onSave}>
              <div className="mb-3">
                <label className="form-label">Name</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Full name"
                  value={form.name ?? ''}
                  onChange={onChange('name')}
                  required
                />
              </div>

              <div className="mb-3">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  placeholder="email@example.com"
                  value={form.email ?? ''}
                  onChange={onChange('email')}
                  required
                />
              </div>

              {mode === 'add' && (
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <div className="input-group">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      className="form-control"
                      placeholder="Password"
                      value={form.password ?? ''}
                      onChange={onChange('password')}
                      required
                    />
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={() => setShowPassword((v) => !v)}
                    >
                      {showPassword ? (
                        <IconEyeOff size={16} />
                      ) : (
                        <IconEye size={16} />
                      )}
                    </button>
                  </div>
                </div>
              )}

              <div className="mb-3">
                <label className="form-label">Role</label>
                <select
                  className="form-select"
                  value={form.role ?? 'partner'}
                  onChange={onChange('role')}
                  required
                >
                  {ROLES.map((r) => (
                    <option key={r} value={r}>
                      {r.charAt(0).toUpperCase() + r.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
            </form>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-outline-secondary"
              onClick={onCancel}
            >
              Cancel
            </button>
            <button
              type="submit"
              form="user-form"
              className="btn btn-primary"
              disabled={saving}
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}