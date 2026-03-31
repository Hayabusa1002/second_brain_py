import { useState } from 'react'
import {
  IconEdit, IconTrash, IconEye,
  IconArrowUpRight, IconArrowDownRight,
  IconChevronLeft, IconChevronRight,
  IconDownload, IconChevronDown
} from '@tabler/icons-react'

const PAGE_SIZE = 10

const TYPE_BADGE = {
  income:  { cls: 'bg-green-lt text-green',  icon: <IconArrowUpRight size={12} /> },
  expense: { cls: 'bg-red-lt text-red',      icon: <IconArrowDownRight size={12} /> },
}

const fmt = (n) => new Intl.NumberFormat('es-CO', {
  style: 'currency', currency: 'COP', maximumFractionDigits: 0
}).format(n)

const fmtDate = (d) => d
  ? new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

export default function Table({
  transactions, accountMap, categoryMap,
  selected, loading, page, totalPages, total,
  onToggleAll, onToggleOne,
  onView, onEdit, onDelete, onPageChange,
  onAdd,
}) {
  const [exportOpen, setExportOpen] = useState(false)
  const allIds = transactions.map(t => t.id)
  const allSelected = allIds.length > 0 && allIds.every(id => selected.includes(id))

  function exportData(format) {
    setExportOpen(false)
    if (format === 'csv')  return exportCSV()
    if (format === 'json') return exportJSON()
    if (format === 'xlsx') return exportXLSX()
  }

  function exportCSV() {
    const headers = ['date', 'account_id', 'type', 'category_id', 'amount', 'description']
    const rows = transactions.map(t => headers.map(h => `"${t[h] ?? ''}"`).join(','))
    download(new Blob([[headers.join(','), ...rows].join('\n')], { type: 'text/csv' }), 'transactions.csv')
  }

  function exportJSON() {
    download(
      new Blob([JSON.stringify(transactions, null, 2)], { type: 'application/json' }),
      'transactions.json'
    )
  }

  function exportXLSX() {
    import('xlsx').then(XLSX => {
      const ws = XLSX.utils.json_to_sheet(transactions)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, ws, 'Transactions')
      XLSX.writeFile(wb, 'transactions.xlsx')
    })
  }

  function download(blob, filename) {
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = filename
    a.click()
  }

  return (
    <div className="card">

      {/* Header */}
      <div className="card-header d-flex align-items-center justify-content-between">
        <span className="text-secondary small">
          {selected.length > 0 ? `${selected.length} selected` : `${total} records`}
        </span>
        <div className="d-flex align-items-center gap-2">
          {selected.length > 0 && (
            <button className="btn btn-sm btn-danger d-flex align-items-center gap-1"
              onClick={() => selected.forEach(onDelete)}>
              <IconTrash size={14} stroke={1.5} /> Delete selected
            </button>
          )}
          <div style={{ position: 'relative' }}>
            <button
              className="btn btn-primary d-flex align-items-center gap-1"
              onClick={() => setExportOpen(o => !o)}>
              <IconDownload size={16} stroke={1.5} />
              Export <IconChevronDown size={14} stroke={1.5} />
            </button>
            {exportOpen && (
              <>
                <div style={{ position: 'fixed', inset: 0, zIndex: 999 }}
                  onClick={() => setExportOpen(false)} />
                <div className="dropdown-menu show"
                  style={{ position: 'absolute', right: 0, top: '100%', zIndex: 1000, minWidth: 160 }}>
                  {[['CSV', 'csv'], ['JSON', 'json'], ['Excel (XLSX)', 'xlsx']].map(([label, fmt]) => (
                    <button key={fmt} className="dropdown-item" onClick={() => exportData(fmt)}>
                      {label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="table-responsive">
        <table className="table table-vcenter table-hover card-table">
          <thead>
            <tr>
              <th style={{ width: 40 }}>
                <input type="checkbox" className="form-check-input m-0"
                  checked={allSelected} onChange={onToggleAll} />
              </th>
              <th style={{ width: '20%' }}>Date</th>
              <th style={{ width: '15%' }}>Account</th>
              <th style={{ width: '15%' }}>Type</th>
              <th style={{ width: '15%' }}>Category</th>
              <th style={{ width: '15%' }}>Amount</th>
              <th style={{ width: '10%' }} />
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={7} className="text-center py-5 text-secondary">Loading...</td></tr>
            ) : transactions.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-5 text-secondary">
                  No transactions found.{' '}
                  <button className="btn btn-link p-0" onClick={onAdd}>Create one</button>
                </td>
              </tr>
            ) : transactions.map(tx => {
              const badge = TYPE_BADGE[tx.type] ?? { cls: 'bg-secondary-lt', icon: null }
              return (
                <tr key={tx.id}>
                  <td>
                    <input type="checkbox" className="form-check-input m-0"
                      checked={selected.includes(tx.id)} onChange={() => onToggleOne(tx.id)} />
                  </td>
                  <td className="text-secondary">{fmtDate(tx.date ?? tx.created_at)}</td>
                  <td>
                    <span className="badge bg-blue-lt text-blue">
                      {accountMap[tx.account_id] ?? '—'}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${badge.cls} d-inline-flex align-items-center gap-1`}>
                      {badge.icon}{tx.type}
                    </span>
                  </td>
                  <td>
                    <span className="badge bg-purple-lt text-purple">
                      {categoryMap[tx.category_id] ?? '—'}
                    </span>
                  </td>
                  <td className="fw-medium">
                    <span className={tx.type === 'income' ? 'text-green' : 'text-red'}>
                      {tx.type === 'expense' ? '−' : '+'}{fmt(tx.amount)}
                    </span>
                  </td>
                  <td>
                    <div className="d-flex gap-1 justify-content-end">
                      <button className="btn btn-sm btn-ghost-secondary" title="View"
                        onClick={() => onView(tx)}>
                        <IconEye size={16} stroke={1.5} />
                      </button>
                      <button className="btn btn-sm btn-ghost-secondary" title="Edit"
                        onClick={() => onEdit(tx)}>
                        <IconEdit size={16} stroke={1.5} />
                      </button>
                      <button className="btn btn-sm btn-ghost-danger" title="Delete"
                        onClick={() => onDelete(tx.id)}>
                        <IconTrash size={16} stroke={1.5} />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="card-footer d-flex align-items-center justify-content-between">
          <p className="m-0 text-secondary small">
            Showing <strong>{(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, total)}</strong> of <strong>{total}</strong>
          </p>
          <ul className="pagination m-0">
            <li className={`page-item ${page === 1 ? 'disabled' : ''}`}>
              <button className="page-link" onClick={() => onPageChange(p => p - 1)}>
                <IconChevronLeft size={14} stroke={1.5} />
              </button>
            </li>
            {Array.from({ length: totalPages }, (_, i) => i + 1)
              .filter(p => p === 1 || p === totalPages || Math.abs(p - page) <= 1)
              .reduce((acc, p, i, arr) => {
                if (i > 0 && p - arr[i - 1] > 1) acc.push('...')
                acc.push(p)
                return acc
              }, [])
              .map((p, i) =>
                p === '...' ? (
                  <li key={`ellipsis-${i}`} className="page-item disabled">
                    <span className="page-link">…</span>
                  </li>
                ) : (
                  <li key={p} className={`page-item ${p === page ? 'active' : ''}`}>
                    <button className="page-link" onClick={() => onPageChange(p)}>{p}</button>
                  </li>
                )
              )}
            <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
              <button className="page-link" onClick={() => onPageChange(p => p + 1)}>
                <IconChevronRight size={14} stroke={1.5} />
              </button>
            </li>
          </ul>
        </div>
      )}

    </div>
  )
}