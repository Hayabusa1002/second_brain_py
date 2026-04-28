import { useNavigate } from 'react-router-dom'
import { IconLock, IconEye, IconEyeOff, IconArrowLeft } from '@tabler/icons-react'
import Alert from '../../components/ui/Alert'
import useChangePassword from '../../hooks/profile/useChangePassword'

export default function ChangePassword() {
  const navigate = useNavigate()

  const {
    form,
    show,
    error,
    success,
    fieldErrors,
    loading,
    handleChange,
    toggleShow,
    handleSubmit,
  } = useChangePassword()

  return (
    <div className="container-xl">
      <div className="page-header d-print-none">
        <div className="row align-items-center">
          <div className="col">
            <div className="page-pretitle">Profile</div>
            <h2 className="page-title">Change Password</h2>
          </div>
          <div className="col-auto ms-auto">
            <button
              type="button"
              className="btn d-flex align-items-center gap-2"
              onClick={() => navigate(-1)}
            >
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

                  <div className="mb-3">
                    <label className="form-label">Current password</label>
                    <div className="input-group input-group-flat">
                      <input
                        type={show.current ? 'text' : 'password'}
                        className={`form-control ${fieldErrors.current_password ? 'is-invalid' : ''}`}
                        placeholder="Enter current password"
                        value={form.current_password}
                        onChange={handleChange('current_password')}
                        required
                      />
                      <span className="input-group-text">
                        <button
                          type="button"
                          className="link-secondary"
                          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                          onClick={() => toggleShow('current')}
                          title={show.current ? 'Hide password' : 'Show password'}
                        >
                          {show.current ? <IconEyeOff size={20} stroke={1.5} /> : <IconEye size={20} stroke={1.5} />}
                        </button>
                      </span>
                    </div>
                    {fieldErrors.current_password && (
                      <div className="invalid-feedback d-block">
                        {fieldErrors.current_password}
                      </div>
                    )}
                  </div>

                  <div className="mb-3">
                    <label className="form-label">New password</label>
                    <div className="input-group input-group-flat">
                      <input
                        type={show.new ? 'text' : 'password'}
                        className={`form-control ${fieldErrors.new_password ? 'is-invalid' : ''}`}
                        placeholder="Enter new password"
                        value={form.new_password}
                        onChange={handleChange('new_password')}
                        required
                      />
                      <span className="input-group-text">
                        <button
                          type="button"
                          className="link-secondary"
                          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                          onClick={() => toggleShow('new')}
                          title={show.new ? 'Hide password' : 'Show password'}
                        >
                          {show.new ? <IconEyeOff size={20} stroke={1.5} /> : <IconEye size={20} stroke={1.5} />}
                        </button>
                      </span>
                    </div>
                    {fieldErrors.new_password && (
                      <div className="invalid-feedback d-block">
                        {fieldErrors.new_password}
                      </div>
                    )}
                    <small className="form-hint">Minimum 8 characters.</small>
                  </div>

                  <div className="mb-4">
                    <label className="form-label">Confirm new password</label>
                    <div className="input-group input-group-flat">
                      <input
                        type={show.confirm ? 'text' : 'password'}
                        className={`form-control ${fieldErrors.confirm_password ? 'is-invalid' : ''}`}
                        placeholder="Repeat new password"
                        value={form.confirm_password}
                        onChange={handleChange('confirm_password')}
                        required
                      />
                      <span className="input-group-text">
                        <button
                          type="button"
                          className="link-secondary"
                          style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                          onClick={() => toggleShow('confirm')}
                          title={show.confirm ? 'Hide password' : 'Show password'}
                        >
                          {show.confirm ? <IconEyeOff size={20} stroke={1.5} /> : <IconEye size={20} stroke={1.5} />}
                        </button>
                      </span>
                    </div>
                    {fieldErrors.confirm_password && (
                      <div className="invalid-feedback d-block">
                        {fieldErrors.confirm_password}
                      </div>
                    )}
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