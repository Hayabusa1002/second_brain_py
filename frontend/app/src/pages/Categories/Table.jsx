import { useState } from 'react'
import {
  IconEye,
  IconEdit,
  IconTrash,
  IconListDetails,
  IconDownload,
  IconChevronDown,
} from '@tabler/icons-react'
import * as YAML from 'js-yaml'

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
  const [exportOpen, setExportOpen] = useState(false)

  // Global text search and type filter
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [searchFocused, setSearchFocused] = useState(false)

  // Build full nested export rows
  function exportRows() {
    return categories.map((category) => ({
      id: category.id,
      name: category.name,
      type: category.type,
      created_at: category.created_at ?? '',
      subcategories: getSubcategories(category.id).map((s) => ({
        id: s.id,
        name: s.name,
        created_at: s.created_at ?? '',
      })),
    }))
  }

  // Flatten subcategories for tabular formats (CSV / XLSX)
  function exportFlatRows() {
    return exportRows().map((row) => ({
      id: row.id,
      name: row.name,
      type: row.type,
      subcategory_names: row.subcategories.map((s) => s.name).join(' | '),
      created_at: row.created_at,
    }))
  }

  // Export dispatcher
  function exportData(format) {
    setExportOpen(false)
    if (format === 'csv') return exportCSV()
    if (format === 'json') return exportJSON()
    if (format === 'xlsx') return exportXLSX()
    if (format === 'yaml') return exportYAML()
  }

  function exportCSV() {
    const rows = exportFlatRows()
    const headers = ['id', 'name', 'type', 'subcategory_names', 'created_at']
    const data = rows.map((row) =>
      headers.map((h) => `"${String(row[h] ?? '').replace(/"/g, '""')}"`).join(',')
    )

    download(
      new Blob([[headers.join(','), ...data].join('\n')], {
        type: 'text/csv;charset=utf-8;',
      }),
      'categories.csv'
    )
  }

  function exportJSON() {
    download(
      new Blob([JSON.stringify(exportRows(), null, 2)], {
        type: 'application/json',
      }),
      'categories.json'
    )
  }

  function exportXLSX() {
    import('xlsx').then((XLSX) => {
      const rows = exportFlatRows()
      const ws = XLSX.utils.json_to_sheet(rows)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Categories')
      XLSX.writeFile(wb, 'categories.xlsx')
    })
  }

  function exportYAML() {
    const yaml = YAML.dump(exportRows(), {
      noRefs: true,
      lineWidth: 120,
    })

    download(
      new Blob([yaml], {
        type: 'application/x-yaml;charset=utf-8;',
      }),
      'categories.yaml'
    )
  }

  // Generic file download helper
  function download(blob, filename) {
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  // In‑memory filtering for search + type
  const filteredCategories = categories.filter((category) => {
    const matchesType = typeFilter ? category.type === typeFilter : true

    const haystack = [
      category.name ?? '',
      ...getSubcategories(category.id).map((s) => s.name ?? ''),
    ]
      .join(' ')
      .toLowerCase()

    const matchesSearch = search
      ? haystack.includes(search.toLowerCase())
      : true

    return matchesType && matchesSearch
  })

  // We keep this state only for future tweaks; it no longer changes width
  const searchExpanded = Boolean(search || typeFilter || searchFocused)

  return (
    <div className="card">
      {/* Fixed-height header, filters + Export on the right */}
      <div
        className="card-header d-flex align-items-center"
        style={{
          minHeight: 72,
          paddingTop: 12,
          paddingBottom: 12,
        }}
      >
        {/* Records counter on the left */}
        <div className="text-secondary small">
          {filteredCategories.length} records
          {filteredCategories.length !== categories.length && (
            <span className="text-muted ms-1">
              (de {categories.length})
            </span>
          )}
        </div>

        {/* Filters + Export aligned to the right, single row */}
        <div
          className="d-flex align-items-center ms-auto"
          style={{
            gap: 8,
            width: '100%',
            maxWidth: 800,
            whiteSpace: 'nowrap', // prevent wrapping to next line
          }}
        >
          {/* Search input (fixed horizontal behavior) */}
          <div
            className="input-group input-group-flat search-stable"
            style={{
              flex: '1 1 auto',
            }}
          >
            <input
              type="text"
              className="form-control"
              placeholder="Search categories or subcategories"
              value={search}
              onFocus={() => setSearchFocused(true)}
              onBlur={() => setSearchFocused(false)}
              onChange={(e) => setSearch(e.target.value)}
            />
            <span className="input-group-text">
              {search && (
                <button
                  type="button"
                  className="btn btn-link p-0 text-secondary"
                  onClick={() => setSearch('')}
                  title="Clear"
                >
                  ✕
                </button>
              )}
            </span>
          </div>

          {/* Type filter select */}
          <select
            className="form-select"
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            style={{ width: 160, flex: '0 0 auto' }}
          >
            <option value="">All types</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>

          {/* Export dropdown button */}
          <div style={{ position: 'relative', flex: '0 0 auto' }}>
            <button
              className="btn btn-primary d-flex align-items-center gap-1"
              onClick={() => setExportOpen((o) => !o)}
            >
              <IconDownload size={16} stroke={1.5} />
              Export
              <IconChevronDown size={14} stroke={1.5} />
            </button>

            {exportOpen && (
              <>
                {/* Backdrop to close dropdown when clicking outside */}
                <div
                  style={{ position: 'fixed', inset: 0, zIndex: 999 }}
                  onClick={() => setExportOpen(false)}
                />

                <div
                  className="dropdown-menu show"
                  style={{
                    position: 'absolute',
                    right: 0,
                    top: '100%',
                    zIndex: 1000,
                    minWidth: 180,
                  }}
                >
                  {[
                    ['CSV', 'csv'],
                    ['Excel (XLSX)', 'xlsx'],
                    ['JSON', 'json'],
                    ['YAML', 'yaml'],
                  ].map(([label, fmt]) => (
                    <button
                      key={fmt}
                      className="dropdown-item"
                      onClick={() => exportData(fmt)}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Table body */}
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
            ) : filteredCategories.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center py-5 text-secondary">
                  No categories yet.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>
                    Create one
                  </button>
                </td>
              </tr>
            ) : (
              filteredCategories.map((category) => {
                const subcategories = getSubcategories(category.id)

                return (
                  <tr key={category.id}>
                    <td>
                      <span
                        className={`badge ${
                          TYPE_BADGE[category.type] ?? 'bg-secondary-lt'
                        }`}
                      >
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