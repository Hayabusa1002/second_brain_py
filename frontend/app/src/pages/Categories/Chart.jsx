import { IconEdit, IconTrash } from '@tabler/icons-react'

function CategoryItem({ category, tone, onEditCategory, onDeleteCategory }) {
  const badgeClass =
    tone === 'income' ? 'bg-green-lt text-green' : 'bg-red-lt text-red'

  return (
    <div className="d-inline-flex align-items-center gap-2">
      <span className={`badge ${badgeClass} fw-medium`}>{category.name}</span>

      <div className="d-flex gap-1">
        <button
          type="button"
          className="btn btn-sm btn-ghost-secondary"
          title="Edit category"
          onClick={() => onEditCategory(category)}
        >
          <IconEdit size={16} stroke={1.5} />
        </button>

        <button
          type="button"
          className="btn btn-sm btn-ghost-danger"
          title="Delete category"
          onClick={() => onDeleteCategory(category)}
        >
          <IconTrash size={16} stroke={1.5} />
        </button>
      </div>
    </div>
  )
}

export default function Chart({
  categories,
  loading,
  onEditCategory,
  onDeleteCategory,
}) {
  const incomeCategories = categories.filter((c) => c.type === 'income')
  const expenseCategories = categories.filter((c) => c.type === 'expense')

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title mb-0">Categories by type</h3>
      </div>

      <div className="card-body">
        {loading ? (
          <div className="text-secondary">Loading...</div>
        ) : (
          <div className="row g-4">
            <div className="col-md-6">
              <div className="card card-sm border-0 bg-green-lt">
                <div className="card-body">
                  <div className="d-flex align-items-center justify-content-between mb-3">
                    <h4 className="mb-0 text-green">Income</h4>
                    <span className="badge bg-green text-white">
                      {incomeCategories.length}
                    </span>
                  </div>

                  {incomeCategories.length === 0 ? (
                    <div className="text-secondary">No income categories.</div>
                  ) : (
                    <div className="d-flex flex-wrap gap-2">
                      {incomeCategories.map((category) => (
                        <CategoryItem
                          key={category.id}
                          category={category}
                          tone="income"
                          onEditCategory={onEditCategory}
                          onDeleteCategory={onDeleteCategory}
                        />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="col-md-6">
              <div className="card card-sm border-0 bg-red-lt">
                <div className="card-body">
                  <div className="d-flex align-items-center justify-content-between mb-3">
                    <h4 className="mb-0 text-red">Expenses</h4>
                    <span className="badge bg-red text-white">
                      {expenseCategories.length}
                    </span>
                  </div>

                  {expenseCategories.length === 0 ? (
                    <div className="text-secondary">No expense categories.</div>
                  ) : (
                    <div className="d-flex flex-wrap gap-2">
                      {expenseCategories.map((category) => (
                        <CategoryItem
                          key={category.id}
                          category={category}
                          tone="expense"
                          onEditCategory={onEditCategory}
                          onDeleteCategory={onDeleteCategory}
                        />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}