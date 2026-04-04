export default function Table({
  items,
  categories,
  cities,
  loading,
  onEdit,
  onDelete,
  onAdd,
}) {
  const getCategory = (id) => categories.find((c) => c.id === id)
  const getCity = (id) => cities.find((c) => c.id === id)

  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '30%' }} />
            <col style={{ width: '25%' }} />
            <col style={{ width: '25%' }} />
            <col style={{ width: '10%' }} />
            <col style={{ width: '10%' }} />
          </colgroup>
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>City</th>
              <th>Price</th>
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
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center py-5 text-secondary">
                  No items yet.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>
                    Create one
                  </button>
                </td>
              </tr>
            ) : (
              items.map((i) => {
                const cat = getCategory(i.category_id)
                const city = getCity(i.city_id)
                return (
                  <tr key={i.id}>
                    <td className="fw-medium">{i.name}</td>
                    <td className="text-secondary">
                      {cat ? cat.name : '—'}
                    </td>
                    <td className="text-secondary">
                      {city ? city.name : '—'}
                    </td>
                    <td className="text-secondary">
                      {i.price != null ? i.price : '—'}
                    </td>
                    <td className="text-end">
                      <div className="d-flex gap-1 justify-content-end flex-wrap">
                        <button
                          className="btn btn-sm btn-outline-secondary"
                          onClick={() => onEdit(i)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => onDelete(i)}
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