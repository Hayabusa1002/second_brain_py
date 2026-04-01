import { IconTrash } from '@tabler/icons-react'

const fmtDate = (d) => d
  ? new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'numeric', year: 'numeric' })
  : '—'

const ROLE_BADGE = {
  admin:   'bg-purple-lt text-purple',
  owner:   'bg-blue-lt text-blue',
  partner: 'bg-teal-lt text-teal',
}

const STATUS_BADGE = {
  active:   'bg-green-lt text-green',
  pending:  'bg-yellow-lt text-yellow',
  inactive: 'bg-secondary-lt text-secondary',
  banned:   'bg-red-lt text-red',
}

export default function Table({ users, currentUserId, loading, onEdit, onBan, onDelete, onAdd }) {
  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '20%' }} />
            <col style={{ width: '25%' }} />
            <col style={{ width: '15%' }} />
            <col style={{ width: '15%' }} />
            <col style={{ width: '15%' }} />
            <col style={{ width: '10%' }} />
          </colgroup>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Created</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="text-center py-5 text-secondary">Loading...</td></tr>
            ) : users.length === 0 ? (
              <tr>
                <td colSpan={6} className="text-center py-5 text-secondary">
                  No users yet.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>Create one</button>
                </td>
              </tr>
            ) : users.map(u => {
              const isMe     = u.id === currentUserId
              const isBanned = u.status === 'banned'
              return (
                <tr key={u.id}>
                  <td className="fw-medium">
                    {u.name}
                    {isMe && <span className="badge bg-blue-lt text-blue ms-2">you</span>}
                  </td>
                  <td className="text-secondary">{u.email}</td>
                  <td>
                    <span className={`badge ${ROLE_BADGE[u.role] ?? 'bg-secondary-lt'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${STATUS_BADGE[u.status] ?? 'bg-secondary-lt'}`}>
                      {u.status}
                    </span>
                  </td>
                  <td className="text-secondary">{fmtDate(u.created_at)}</td>
                  <td>
                    <div className="d-flex gap-1 justify-content-end">
                      <button className="btn btn-sm btn-outline-secondary"
                        onClick={() => onEdit(u)}>
                        Edit
                      </button>
                      {!isMe && (
                        <>
                          <button
                            className={`btn btn-sm ${isBanned ? 'btn-outline-success' : 'btn-outline-warning'}`}
                            onClick={() => onBan(u)}>
                            {isBanned ? 'Unban' : 'Ban'}
                          </button>
                          <button className="btn btn-sm btn-outline-danger"
                            onClick={() => onDelete(u)}>
                            <IconTrash size={14} stroke={1.5} />
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}