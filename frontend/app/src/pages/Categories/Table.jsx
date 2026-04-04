const fmtDate = (d) =>
  d
    ? new Date(d).toLocaleDateString('es-CO', {
        day: '2-digit',
        month: 'numeric',
        year: 'numeric',
      })
    : '—'

const TYPE_BADGE = {
  income: 'bg-green-lt text-green',
  expense: 'bg-red-lt text-red',
}

export default function Table({ categories, loading, onEdit, onDelete, onAdd }) {
  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '35%' }} />
            <col style={{ width: '20%' }} />
            <col style={{ width: '25%' }} />
            <col style={{ width: '20%' }} />
          </colgroup>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Parent category</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={4} className="text-center py-5 text-secondary">
                  Loading...
                </td>
              </tr>
            ) : categories.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center py-5 text-secondary">
                  No categories yet.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>
                    Create one
                  </button>
                </td>
              </tr>
            ) : (
              categories.map((c) => {
                const parent = categories.find((p) => p.id === c.parent_id)
                return (
                  <tr key={c.id}>
                    <td className="fw-medium">{c.name}</td>
                    <td>
                      <span
                        className={`badge ${
                          TYPE_BADGE[c.type] ?? 'bg-secondary-lt'
                        }`}
                      >
                        {c.type}
                      </span>
                    </td>
                    <td className="text-secondary">
                      {parent ? parent.name : '—'}
                    </td>
                    <td className="text-end">
                      <div className="d-flex gap-1 justify-content-end flex-wrap">
                        <button
                          className="btn btn-sm btn-outline-secondary"
                          onClick={() => onEdit(c)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => onDelete(c)}
                        >
                          Delete
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
  )
}