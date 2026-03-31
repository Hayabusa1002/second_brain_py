import { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'

// Icons
import {
  IconPlus, IconEdit, IconTrash, IconEye,
  IconArrowUpRight, IconArrowDownRight,
  IconSearch, IconChevronLeft, IconChevronRight
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

export default function Transactions() {
  const navigate = useNavigate()
  const [transactions, setTransactions] = useState([])
  const [total, setTotal]               = useState(0)
  const [page, setPage]                 = useState(1)
  const [search, setSearch]             = useState('')
  const [searchInput, setSearchInput]   = useState('')
  const [loading, setLoading]           = useState(true)
  const [error, setError]               = useState('')
  const [selected, setSelected]         = useState([])
  const [deleteId, setDeleteId]         = useState(null)
  const [accounts, setAccounts]         = useState({})
  const [categories, setCategories]     = useState({})

  const totalPages = Math.ceil(total / PAGE_SIZE)

  // Fetch transactions
  const fetchTransactions = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/transactions', {
        params: { page, limit: PAGE_SIZE, search: search || undefined }
      })
      setTransactions(data.items ?? data)
      setTotal(data.total ?? (data.items ?? data).length)
    } catch {
      setError('Failed to load transactions.')
    } finally {
      setLoading(false)
    }
  }, [page, search])

  useEffect(() => { fetchTransactions() }, [fetchTransactions])

  // Fetch accounts & categories maps
  useEffect(() => {
    async function fetchMeta() {
      try {
        const [accRes, catRes] = await Promise.all([
          client.get('/accounts'),
          client.get('/categories'),
        ])
        const accMap = {}
        ;(accRes.data.items ?? accRes.data).forEach(a => { accMap[a.id] = a.name })
        const catMap = {}
        ;(catRes.data.items ?? catRes.data).forEach(c => { catMap[c.id] = c.name })
        setAccounts(accMap)
        setCategories(catMap)
      } catch (e) {
        console.error(e)
      }
    }
    fetchMeta()
  }, [])

  function handleSearch(e) {
    e.preventDefault()
    setPage(1)
    setSearch(searchInput)
  }

  const allIds = transactions.map(t => t.id)
  const allSelected = allIds.length > 0 && allIds.every(id => selected.includes(id))
  function toggleAll() {
    setSelected(allSelected ? [] : allIds)
  }
  function toggleOne(id) {
    setSelected(s => s.includes(id) ? s.filter(x => x !== id) : [...s, id])
  }

  async function handleDelete(id) {
    try {
      await client.delete(`/transactions/${id}`)
      setDeleteId(null)
      fetchTransactions()
    } catch {
      setError('Failed to delete transaction.')
    }
  }

  return (
    <div className="container-xl py-4">

      {/* Header */}
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h2 className="mb-0">Transactions</h2>
          <p className="text-secondary mb-0">{total} records found</p>
        </div>
        <Link to="/transactions/new" className="btn btn-primary d-flex align-items-center gap-1">
          <IconPlus size={16} stroke={1.5} /> New Transaction
        </Link>
      </div>

      <Alert message={error} />

      {/* Card */}
      <div className="card">

        {/* Toolbar */}
        <div className="card-header d-flex align-items-center justify-content-between gap-2 flex-wrap">
          <form className="d-flex gap-2" onSubmit={handleSearch}>
            <div className="input-group">
              <input
                type="text"
                className="form-control form-control-sm"
                placeholder="Search transactions..."
                value={searchInput}
                onChange={e => setSearchInput(e.target.value)}
                style={{ minWidth: 220 }}
              />
              <button type="submit" className="btn btn-sm btn-outline-secondary">
                <IconSearch size={14} stroke={1.5} />
              </button>
            </div>
          </form>

          {selected.length > 0 && (
            <span className="text-secondary small">
              {selected.length} selected
              <button
                className="btn btn-sm btn-danger ms-2"
                onClick={() => selected.forEach(handleDelete)}>
                <IconTrash size={14} stroke={1.5} /> Delete selected
              </button>
            </span>
          )}
        </div>

        {/* Table */}
        <div className="table-responsive">
          <table className="table table-vcenter table-hover card-table">
            <thead>
              <tr>
                <th style={{ width: 40 }}>
                  <input
                    type="checkbox"
                    className="form-check-input m-0"
                    checked={allSelected}
                    onChange={toggleAll}
                  />
                </th>
                <th>Date</th>
                <th>Account</th>
                <th>Type</th>
                <th>Category</th>
                <th className="text-end">Amount</th>
                <th>Description</th>
                <th style={{ width: 100 }} />
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={8} className="text-center py-5 text-secondary">
                    Loading...
                  </td>
                </tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={8} className="text-center py-5 text-secondary">
                    No transactions found.{' '}
                    <Link to="/transactions/new">Create one</Link>
                  </td>
                </tr>
              ) : transactions.map(tx => {
                const badge = TYPE_BADGE[tx.type] ?? { cls: 'bg-secondary-lt', icon: null }
                return (
                  <tr key={tx.id}>
                    <td>
                      <input
                        type="checkbox"
                        className="form-check-input m-0"
                        checked={selected.includes(tx.id)}
                        onChange={() => toggleOne(tx.id)}
                      />
                    </td>
                    <td className="text-secondary">{fmtDate(tx.date ?? tx.created_at)}</td>
                    <td className="text-secondary">{accounts[tx.account_id] ?? '—'}</td>
                    <td>
                      <span className={`badge ${badge.cls} d-inline-flex align-items-center gap-1`}>
                        {badge.icon}
                        {tx.type}
                      </span>
                    </td>
                    <td className="text-secondary">{categories[tx.category_id] ?? '—'}</td>
                    <td className="text-end fw-medium">
                      <span className={tx.type === 'income' ? 'text-green' : 'text-red'}>
                        {tx.type === 'expense' ? '−' : '+'}{fmt(tx.amount)}
                      </span>
                    </td>
                    <td>
                      <div className="fw-medium">{tx.description || '—'}</div>
                    </td>
                    <td>
                      <div className="d-flex gap-1 justify-content-end">
                        <button
                          className="btn btn-sm btn-ghost-secondary"
                          title="View"
                          onClick={() => navigate(`/transactions/${tx.id}`)}>
                          <IconEye size={16} stroke={1.5} />
                        </button>
                        <button
                          className="btn btn-sm btn-ghost-secondary"
                          title="Edit"
                          onClick={() => navigate(`/transactions/${tx.id}/edit`)}>
                          <IconEdit size={16} stroke={1.5} />
                        </button>
                        <button
                          className="btn btn-sm btn-ghost-danger"
                          title="Delete"
                          onClick={() => setDeleteId(tx.id)}>
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
                <button className="page-link" onClick={() => setPage(p => p - 1)}>
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
                      <button className="page-link" onClick={() => setPage(p)}>{p}</button>
                    </li>
                  )
                )}
              <li className={`page-item ${page === totalPages ? 'disabled' : ''}`}>
                <button className="page-link" onClick={() => setPage(p => p + 1)}>
                  <IconChevronRight size={14} stroke={1.5} />
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>

      {/* Delete confirmation modal */}
      {deleteId && (
        <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
          <div className="modal-dialog modal-sm modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-body text-center py-4">
                <IconTrash size={40} stroke={1.5} className="text-danger mb-3" />
                <h5>Delete transaction?</h5>
                <p className="text-secondary">This action cannot be undone.</p>
              </div>
              <div className="modal-footer justify-content-center gap-2">
                <button className="btn btn-outline-secondary" onClick={() => setDeleteId(null)}>
                  Cancel
                </button>
                <button className="btn btn-danger" onClick={() => handleDelete(deleteId)}>
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}