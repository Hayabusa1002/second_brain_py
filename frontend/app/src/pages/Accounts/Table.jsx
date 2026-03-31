import { IconEdit, IconTrash, IconUsers } from '@tabler/icons-react'

const fmtDate = (d) => d
  ? new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'numeric', year: 'numeric' })
  : '—'

const TYPE_BADGE = {
  individual: 'bg-blue-lt text-blue',
  shared:     'bg-teal-lt text-teal',
}

export default function Table({ accounts, loading, onEdit, onDelete, onOwners, onAdd }) {
  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '15%' }} />
            <col style={{ width: '15%' }} />
            <col style={{ width: '15%' }} />
            <col style={{ width: '15%' }} />
            <col style={{ width: '10%' }} />
          </colgroup>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Owners</th>
              <th>Created</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="text-center py-5 text-secondary">Loading...</td></tr>
            ) : accounts.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center py-5 text-secondary">
                  No accounts yet.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>Create one</button>
                </td>
              </tr>
            ) : accounts.map(acc => (
              <tr key={acc.id}>
                <td className="fw-medium">{acc.name}</td>
                <td>
                  <span className={`badge ${TYPE_BADGE[acc.type] ?? 'bg-secondary-lt'}`}>
                    {acc.type}
                  </span>
                </td>
                <td className="text-secondary">
                  {acc.owners?.map(o => o.name).join(', ') ?? '—'}
                </td>
                <td className="text-secondary">{fmtDate(acc.created_at)}</td>
                <td>
                  <div className="d-flex gap-1 justify-content-end">
                    <button className="btn btn-sm btn-outline-secondary d-flex align-items-center gap-1"
                      onClick={() => onOwners(acc)}>
                      <IconUsers size={14} stroke={1.5} /> Owners
                    </button>
                    <button className="btn btn-sm btn-outline-secondary"
                      onClick={() => onEdit(acc)}>
                      Edit
                    </button>
                    <button className="btn btn-sm btn-danger"
                      onClick={() => onDelete(acc)}>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}