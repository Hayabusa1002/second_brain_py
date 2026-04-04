export default function Table({ cities, loading, onEdit, onDelete, onAdd }) {
  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '40%' }} />
            <col style={{ width: '40%' }} />
            <col style={{ width: '20%' }} />
          </colgroup>
          <thead>
            <tr>
              <th>Name</th>
              <th>Country</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={3} className="text-center py-5 text-secondary">
                  Loading...
                </td>
              </tr>
            ) : cities.length === 0 ? (
              <tr>
                <td colSpan={3} className="text-center py-5 text-secondary">
                  No cities yet.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>
                    Create one
                  </button>
                </td>
              </tr>
            ) : (
              cities.map((c) => (
                <tr key={c.id}>
                  <td className="fw-medium">{c.name}</td>
                  <td className="text-secondary">{c.country}</td>
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
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}