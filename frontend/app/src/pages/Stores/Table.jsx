import { useState } from 'react'
import {
  IconEye,
  IconEdit,
  IconTrash,
  IconDownload,
  IconChevronDown,
  IconTags,
} from '@tabler/icons-react'
import * as YAML from 'js-yaml'

export default function Table({
  stores,
  loading,
  onShow,
  onEdit,
  onDelete,
  onAdd,
  onAssignSubcategory,
}) {
  const [exportOpen, setExportOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [searchFocused, setSearchFocused] = useState(false)

  function getStoreSubcategories(store) {
    if (!Array.isArray(store.store_subcategories)) return []

    return store.store_subcategories
      .map((item) => item?.subcategory)
      .filter(Boolean)
  }

  function exportRows() {
    return stores.map((store) => {
      const subcategories = getStoreSubcategories(store)

      return {
        id: store.id,
        name: store.name,
        type: store.type ?? '',
        address: store.address ?? '',
        website: store.website ?? '',
        subcategories: subcategories.map((s) => s.name).join(', '),
        created_at: store.created_at ?? '',
      }
    })
  }

  function exportData(format) {
    setExportOpen(false)
    if (format === 'csv') return exportCSV()
    if (format === 'json') return exportJSON()
    if (format === 'xlsx') return exportXLSX()
    if (format === 'yaml') return exportYAML()
  }

  function exportCSV() {
    const rows = exportRows()
    const headers = [
      'id',
      'name',
      'type',
      'address',
      'website',
      'subcategories',
      'created_at',
    ]

    const data = rows.map((row) =>
      headers.map((h) => `"${String(row[h] ?? '').replace(/"/g, '""')}"`).join(',')
    )

    download(
      new Blob([[headers.join(','), ...data].join('\n')], {
        type: 'text/csv;charset=utf-8;',
      }),
      'stores.csv'
    )
  }

  function exportJSON() {
    download(
      new Blob([JSON.stringify(exportRows(), null, 2)], {
        type: 'application/json',
      }),
      'stores.json'
    )
  }

  function exportXLSX() {
    import('xlsx').then((XLSX) => {
      const rows = exportRows()
      const ws = XLSX.utils.json_to_sheet(rows)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Stores')
      XLSX.writeFile(wb, 'stores.xlsx')
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
      'stores.yaml'
    )
  }

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

  const types = [...new Set(stores.map((s) => s.type).filter(Boolean))].sort()

  const filteredStores = stores.filter((store) => {
    const matchesType = typeFilter ? store.type === typeFilter : true

    const subcategoryNames = getStoreSubcategories(store)
      .map((sub) => sub.name ?? '')
      .join(' ')

    const haystack = [
      store.name ?? '',
      store.type ?? '',
      store.address ?? '',
      store.website ?? '',
      subcategoryNames,
    ]
      .join(' ')
      .toLowerCase()

    const matchesSearch = search ? haystack.includes(search.toLowerCase()) : true

    return matchesType && matchesSearch
  })

  const searchExpanded = Boolean(search || typeFilter || searchFocused)

  return (
    <div className="card">
      <div
        className="card-header d-flex align-items-center"
        style={{
          minHeight: 72,
          paddingTop: 12,
          paddingBottom: 12,
        }}
      >
        <div className="text-secondary small">
          {filteredStores.length} records
          {filteredStores.length !== stores.length && (
            <span className="text-muted ms-1">
              (de {stores.length})
            </span>
          )}
        </div>

        <div
          className="d-flex align-items-center ms-auto"
          style={{
            gap: 8,
            width: '100%',
            maxWidth: 1000,
            whiteSpace: 'nowrap',
          }}
        >
          <div
            className="input-group input-group-flat search-stable"
            style={{
              flex: '1 1 auto',
            }}
          >
            <input
              type="text"
              className="form-control"
              placeholder="Search stores, type or subcategory"
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

          <select
            className="form-select"
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            style={{ width: 180, flex: '0 0 auto' }}
          >
            <option value="">All types</option>
            {types.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>

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

      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '28%' }} />
            <col style={{ width: '18%' }} />
            <col style={{ width: '34%' }} />
            <col style={{ width: '20%' }} />
          </colgroup>

          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
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
            ) : filteredStores.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center py-5 text-secondary">
                  No stores found{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>
                    Create one
                  </button>
                </td>
              </tr>
            ) : (
              filteredStores.map((s) => {
                const subcategories = getStoreSubcategories(s)

                return (
                  <tr key={s.id}>
                    <td className="fw-medium">{s.name}</td>

                    <td>{s.type || '—'}</td>

                    <td>
                      {subcategories.length > 0 ? (
                        <div className="d-flex flex-wrap gap-1">
                          {subcategories.map((sub, index) => (
                            <span
                              key={sub.id ?? `${s.id}-${index}`}
                              className="badge bg-secondary-lt text-secondary"
                            >
                              {sub.name}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-secondary">None</span>
                      )}
                    </td>

                    <td>
                      <div className="d-flex gap-1 justify-content-end flex-wrap">
                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-secondary"
                          title="View"
                          onClick={() => onShow(s)}
                        >
                          <IconEye size={16} stroke={1.5} />
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-secondary"
                          title="Edit"
                          onClick={() => onEdit(s)}
                        >
                          <IconEdit size={16} stroke={1.5} />
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-secondary"
                          title="Manage subcategories"
                          onClick={() => onAssignSubcategory?.(s)}
                        >
                          <IconTags size={16} stroke={1.5} />
                        </button>

                        <button
                          type="button"
                          className="btn btn-sm btn-ghost-danger"
                          title="Delete"
                          onClick={() => onDelete(s)}
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