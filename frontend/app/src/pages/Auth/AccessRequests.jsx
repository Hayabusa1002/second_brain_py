import { useEffect, useState } from 'react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Navbar from '../../components/layout/Navbar'

const ROLE_BADGE = {
  admin: 'bg-purple-lt text-purple',
  owner: 'bg-blue-lt text-blue',
  partner: 'bg-teal-lt text-teal',
}

const fmtDate = (d) =>
  d
    ? new Date(d).toLocaleDateString('es-CO', {
        day: '2-digit',
        month: 'numeric',
        year: 'numeric',
      })
    : '—'

export default function AccessRequests() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [actionError, setActionError] = useState('')
  const [processingId, setProcessingId] = useState(null)

  useEffect(() => {
    fetchRequests()
  }, [])

  async function fetchRequests() {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/users/pending')
      setRequests(data.users ?? data.items ?? data)
    } catch (err) {
      if (err.response?.status === 403) {
        setError('You do not have permission to view access requests.')
      } else {
        setError('Failed to load access requests.')
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleApprove(user) {
    setProcessingId(user.id)
    setActionError('')
    try {
      await client.post(`/users/${user.id}/approve`)
      setRequests((prev) => prev.filter((u) => u.id !== user.id))
    } catch (err) {
      setActionError(err.response?.data?.detail || 'Failed to approve request.')
    } finally {
      setProcessingId(null)
    }
  }

  async function handleReject(user) {
    setProcessingId(user.id)
    setActionError('')
    try {
      await client.post(`/users/${user.id}/reject`)
      setRequests((prev) => prev.filter((u) => u.id !== user.id))
    } catch (err) {
      setActionError(err.response?.data?.detail || 'Failed to reject request.')
    } finally {
      setProcessingId(null)
    }
  }

  const isForbidden = error === 'You do not have permission to view access requests.'

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
                                {fmtDate(u.created_at)}
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