import {
  IconEye,
  IconEdit,
  IconTrash,
  IconListDetails,
} from '@tabler/icons-react'

const TYPE_BADGE = {
  income: 'bg-green-lt text-green',
  expense: 'bg-red-lt text-red',
}

export default function Table({
  categories,
  getSubcategories,
  loading,
  onShow,
  onEdit,
  onSubcategory,
  onDelete,
  onAdd,
}) {
  return (
    <div className="card">
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '15%' }} />
            <col style={{ width: '25%' }} />
            <col style={{ width: '40%' }} />
            <col style={{ width: '20%' }} />
          </colgroup>

          <thead>
            <tr>
              <th>Type</th>
              <th>Category</th>
              <th>Subcategories</th>
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
              categories.map((category) => {
                const subcategories = getSubcategories(category.id)

                return (
                  <tr key={category.id}>
                    <td>
                      <span className={`badge ${TYPE_BADGE[category.type] ?? 'bg-secondary-lt'}`}>
                        {category.type}
                      </span>
                    </td>

                    <td className="fw-medium">{category.name}</td>

                    <td>
                      {subcategories.length === 0 ? (
                        <span className="text-secondary">—</span>
                      ) : (
                        <div className="d-flex flex-wrap gap-1">
                          {subcategories.map((sub) => (
                            <span
                              key={sub.id}
                              className="badge bg-secondary-lt text-secondary"
                            >
                              {sub.name}
                            </span>
                          ))}
                        </div>
                      )}
                    </td>

                    <td>
                      <div className="d-flex gap-1 justify-content-end">
                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-secondary"
                          title="View"
                          onClick={() => onShow(category)}
                        >
                          <IconEye size={16} stroke={1.5} />
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-secondary"
                          title="Edit"
                          onClick={() => onEdit(category)}
                        >
                          <IconEdit size={16} stroke={1.5} />
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-secondary"
                          title="Subcategories"
                          onClick={() => onSubcategory(category)}
                        >
                          <IconListDetails size={16} stroke={1.5} />
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-danger"
                          title="Delete"
                          onClick={() => onDelete(category)}
                        >
                          <IconTrash size={16} stroke={1.5} />
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