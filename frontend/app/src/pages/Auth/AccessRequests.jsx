import Alert from '../../components/ui/Alert'
import Navbar from '../../components/layout/Navbar'
import useAccessRequests from '../../hooks/auth/useAccessRequests'
import formatDate from '../../utils/auth/accessRequests/formatDate'

const ROLE_BADGE = {
  admin: 'bg-purple-lt text-purple',
  owner: 'bg-blue-lt text-blue',
  partner: 'bg-teal-lt text-teal',
}

export default function AccessRequests() {
  const {
    requests,
    loading,
    error,
    actionError,
    processingId,
    isForbidden,
    handleApprove,
    handleReject,
  } = useAccessRequests()

  return (
    <div className="page">
      <Navbar />

      <div className="page-wrapper">
        <div className="page-body">
          <div className="container-xl py-4">
            <div className="d-flex align-items-center justify-content-between mb-4">
              <h2 className="mb-0">Access requests</h2>
            </div>

            <Alert message={error || actionError} />

            {isForbidden ? null : (
              <div className="card">
                <div className="table-responsive">
                  <table className="table table-vcenter table-hover card-table">
                    <colgroup>
                      <col style={{ width: '20%' }} />
                      <col style={{ width: '30%' }} />
                      <col style={{ width: '15%' }} />
                      <col style={{ width: '15%' }} />
                      <col style={{ width: '20%' }} />
                    </colgroup>

                    <thead>
                      <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Registered</th>
                        <th />
                      </tr>
                    </thead>

                    <tbody>
                      {loading ? (
                        <tr>
                          <td colSpan={5} className="text-center py-5 text-secondary">
                            Loading...
                          </td>
                        </tr>
                      ) : requests.length === 0 ? (
                        <tr>
                          <td colSpan={5} className="text-center py-5 text-secondary">
                            No access requests.
                          </td>
                        </tr>
                      ) : (
                        requests.map((u) => {
                          const busy = processingId === u.id

                          return (
                            <tr key={u.id}>
                              <td className="fw-medium">{u.name}</td>
                              <td className="text-secondary">{u.email}</td>
                              <td>
                                <span
                                  className={`badge ${
                                    ROLE_BADGE[u.role] ?? 'bg-secondary-lt text-secondary'
                                  }`}
                                >
                                  {u.role}
                                </span>
                              </td>
                              <td className="text-secondary">
                                {formatDate(u.created_at)}
                              </td>
                              <td>
                                <div className="d-flex gap-2 justify-content-end">
                                  <button
                                    type="button"
                                    className="btn btn-sm btn-success"
                                    onClick={() => handleApprove(u)}
                                    disabled={busy}
                                  >
                                    {busy ? 'Processing...' : 'Approve'}
                                  </button>

                                  <button
                                    type="button"
                                    className="btn btn-sm btn-danger"
                                    onClick={() => handleReject(u)}
                                    disabled={busy}
                                  >
                                    {busy ? 'Processing...' : 'Reject'}
                                  </button>
                                </div>
                              </td>
                            </tr>
                          )
                        })
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}