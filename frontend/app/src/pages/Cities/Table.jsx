import { useState } from 'react'
import {
  IconEye,
  IconEdit,
  IconTrash,
  IconDownload,
  IconChevronDown,
} from '@tabler/icons-react'
import * as YAML from 'js-yaml'

export default function Table({
  cities,
  loading,
  onShow,
  onEdit,
  onDelete,
  onAdd,
}) {
  const [exportOpen, setExportOpen] = useState(false)

  function exportRows() {
    return cities.map((city) => ({
      id: city.id,
      name: city.name,
      state: city.state ?? '',
      country: city.country ?? '',
      created_at: city.created_at ?? '',
    }))
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
    const headers = ['id', 'name', 'state', 'country', 'created_at']
    const data = rows.map((row) =>
      headers.map((h) => `"${String(row[h] ?? '').replace(/"/g, '""')}"`).join(',')
    )

    download(
      new Blob([[headers.join(','), ...data].join('\n')], {
        type: 'text/csv;charset=utf-8;',
      }),
      'cities.csv'
    )
  }

  function exportJSON() {
    download(
      new Blob([JSON.stringify(exportRows(), null, 2)], {
        type: 'application/json',
      }),
      'cities.json'
    )
  }

  function exportXLSX() {
    import('xlsx').then((XLSX) => {
      const rows = exportRows()
      const ws = XLSX.utils.json_to_sheet(rows)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Cities')
      XLSX.writeFile(wb, 'cities.xlsx')
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
      'cities.yaml'
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

  return (
    <div className="card">
      <div className="card-header d-flex align-items-center justify-content-between">
        <span className="text-secondary small">{cities.length} records</span>

        <div style={{ position: 'relative' }}>
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

      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <colgroup>
            <col style={{ width: '35%' }} />
            <col style={{ width: '35%' }} />
            <col style={{ width: '20%' }} />
            <col style={{ width: '10%' }} />
          </colgroup>

          <thead>
            <tr>
              <th>Name</th>
              <th>State</th>
              <th>Country</th>
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
            ) : cities.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center py-5 text-secondary">
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
                  <td>{c.state || '—'}</td>
                  <td>{c.country}</td>
                  <td>
                    <div className="d-flex gap-1 justify-content-end">
                      <button
                        type="button"
                        className="btn btn-sm btn-ghost-secondary"
                        title="View"
                        onClick={() => onShow(c)}
                      >
                        <IconEye size={16} stroke={1.5} />
                      </button>

                      <button
                        type="button"
                        className="btn btn-sm btn-ghost-secondary"
                        title="Edit"
                        onClick={() => onEdit(c)}
                      >
                        <IconEdit size={16} stroke={1.5} />
                      </button>

                      <button
                        type="button"
                        className="btn btn-sm btn-ghost-danger"
                        title="Delete"
                        onClick={() => onDelete(c)}
                      >
                        <IconTrash size={16} stroke={1.5} />
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