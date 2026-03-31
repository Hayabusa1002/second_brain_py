import { useState, useEffect, useCallback } from 'react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import {
  IconPlus, IconEdit, IconTrash, IconEye,
  IconArrowUpRight, IconArrowDownRight,
  IconSearch, IconChevronLeft, IconChevronRight,
  IconUpload, IconDownload, IconX
} from '@tabler/icons-react'

const PAGE_SIZE = 10

const TYPE_BADGE = {
  income:  { cls: 'bg-green-lt text-green',  icon: <IconArrowUpRight size={12} /> },
  expense: { cls: 'bg-red-lt text-red',      icon: <IconArrowDownRight size={12} /> },
}

const EMPTY_FORM = { account_id: '', category_id: '', amount: '', type: 'expense', date: '', description: '' }

const fmt = (n) => new Intl.NumberFormat('es-CO', {
  style: 'currency', currency: 'COP', maximumFractionDigits: 0
}).format(n)

const fmtDate = (d) => d
  ? new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

export default function Transactions() {
  const [transactions, setTransactions] = useState([])
  const [total, setTotal]               = useState(0)
  const [page, setPage]                 = useState(1)
  const [search, setSearch]             = useState('')
  const [searchInput, setSearchInput]   = useState('')
  const [loading, setLoading]           = useState(true)
  const [error, setError]               = useState('')
  const [selected, setSelected]         = useState([])
  const [deleteId, setDeleteId]         = useState(null)
  const [viewTx, setViewTx]             = useState(null)
  const [accounts, setAccounts]         = useState([])
  const [categories, setCategories]     = useState([])
  const [accountMap, setAccountMap]     = useState({})
  const [categoryMap, setCategoryMap]   = useState({})

  const [mode, setMode]           = useState('table')
  const [form, setForm]           = useState(EMPTY_FORM)
  const [editId, setEditId]       = useState(null)
  const [saving, setSaving]       = useState(false)
  const [formError, setFormError] = useState('')

  const [importFile, setImportFile]       = useState(null)
  const [importing, setImporting]         = useState(false)
  const [importError, setImportError]     = useState('')
  const [importSuccess, setImportSuccess] = useState('')

  const totalPages = Math.ceil(total / PAGE_SIZE)

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

  useEffect(() => {
    async function fetchMeta() {
      try {
        const [accRes, catRes] = await Promise.all([
          client.get('/accounts'),
          client.get('/categories'),
        ])
        const accs = accRes.data.items ?? accRes.data
        const cats = catRes.data.items ?? catRes.data
        setAccounts(accs)
        setCategories(cats)
        const accMap = {}; accs.forEach(a => { accMap[a.id] = a.name })
        const catMap = {}; cats.forEach(c => { catMap[c.id] = c.name })
        setAccountMap(accMap)
        setCategoryMap(catMap)
      } catch (e) { console.error(e) }
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
  function toggleAll() { setSelected(allSelected ? [] : allIds) }
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

  function openAdd() {
    setForm(EMPTY_FORM)
    setEditId(null)
    setFormError('')
    setMode('add')
  }

  function openEdit(tx) {
    setForm({
      account_id:  tx.account_id  ?? '',
      category_id: tx.category_id ?? '',
      amount:      tx.amount      ?? '',
      type:        tx.type        ?? 'expense',
      date:        tx.date        ?? '',
      description: tx.description ?? '',
    })
    setEditId(tx.id)
    setFormError('')
    setMode('edit')
  }

  function cancelForm() {
    setMode('table')
    setFormError('')
  }

  const setField = (f) => (e) => setForm(prev => ({ ...prev, [f]: e.target.value }))

  async function handleSave(e) {
    e.preventDefault()
    setSaving(true)
    setFormError('')
    try {
      const payload = { ...form, amount: parseFloat(form.amount) }
      if (mode === 'edit') {
        await client.put(`/transactions/${editId}`, payload)
      } else {
        await client.post('/transactions', payload)
      }
      setMode('table')
      fetchTransactions()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save transaction.')
    } finally {
      setSaving(false)
    }
  }

  function downloadTemplate() {
    const csv = 'date,amount,type,category_id,account_id,description\n2026-01-01,50000,expense,,,'
    const blob = new Blob([csv], { type: 'text/csv' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = 'transactions_template.csv'
    a.click()
  }

  async function handleImport(e) {
    e.preventDefault()
    if (!importFile) return
    setImporting(true)
    setImportError('')
    setImportSuccess('')
    try {
      const fd = new FormData()
      fd.append('file', importFile)
      await client.post('/transactions/import', fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setImportSuccess('Transactions imported successfully.')
      setImportFile(null)
      fetchTransactions()
    } catch (err) {
      setImportError(err.response?.data?.detail || 'Import failed.')
    } finally {
      setImporting(false)
    }
  }

  const TransactionForm = (
    <div className="card mb-4">
      <div className="card-header d-flex align-items-center justify-content-between">
        <h3 className="card-title mb-0">
          {mode === 'edit' ? 'Edit transaction' : 'Add transaction'}
        </h3>
        <button className="btn btn-ghost-secondary btn-sm" onClick={cancelForm}>
          <IconX size={16} stroke={1.5} />
        </button>
      </div>
      <div className="card-body">
        {formError && <div className="alert alert-danger mb-3">{formError}</div>}
        <form onSubmit={handleSave}>
          <div className="row g-3">
            <div className="col-12 col-md-6">
              <label className="form-label">Account</label>
              <select className="form-select" value={form.account_id} onChange={setField('account_id')} required>
                <option value="">Select account...</option>
                {accounts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
              </select>
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Amount</label>
              <input
                type="number" step="0.01" min="0"
                className="form-control" placeholder="0.00"
                value={form.amount} onChange={setField('amount')} required
              />
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Type</label>
              <select className="form-select" value={form.type} onChange={setField('type')} required>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Category</label>
              <select className="form-select" value={form.category_id} onChange={setField('category_id')} required>
                <option value="">Select category...</option>
                {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Date</label>
              <input
                type="date" className="form-control"
                value={form.date} onChange={setField('date')} required
              />
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Description</label>
              <input
                type="text" className="form-control" placeholder="Optional"
                value={form.description} onChange={setField('description')}
              />
            </div>
          </div>
          <div className="d-flex gap-2 mt-4">
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save'}
            </button>
            <button type="button" className="btn btn-outline-secondary" onClick={cancelForm}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )

  const ImportForm = (
    <div className="card mb-4">
      <div className="card-header d-flex align-items-center justify-content-between">
        <h3 className="card-title mb-0">Import transactions</h3>
        <button className="btn btn-ghost-secondary btn-sm" onClick={() => setMode('table')}>
          <IconX size={16} stroke={1.5} />
        </button>
      </div>
      <div className="card-body">
        <p className="text-secondary mb-3">
          Upload a <code>.csv</code> or <code>.xlsx</code> file with columns:{' '}
          <strong>date, amount, type, category_id, account_id, description</strong>
        </p>
        <button className="btn btn-outline-secondary btn-sm mb-3 d-flex align-items-center gap-1"
          onClick={downloadTemplate}>
          <IconDownload size={14} stroke={1.5} /> Download template CSV
        </button>
        {importError   && <div className="alert alert-danger mb-3">{importError}</div>}
        {importSuccess && <div className="alert alert-success mb-3">{importSuccess}</div>}
        <form onSubmit={handleImport}>
          <input
            type="file" className="form-control mb-3" accept=".csv,.xlsx"
            onChange={e => setImportFile(e.target.files[0])}
          />
          <div className="d-flex gap-2">
            <button type="submit" className="btn btn-primary d-flex align-items-center gap-1"
              disabled={!importFile || importing}>
              <IconUpload size={16} stroke={1.5} />
              {importing ? 'Importing...' : 'Import'}
            </button>
            <button type="button" className="btn btn-outline-secondary"
              onClick={() => setMode('table')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )

  return (
    <div className="container-xl py-4">

      {/* Header */}
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h2 className="mb-0">Transactions</h2>
          <p className="text-secondary mb-0">{total} records found</p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-primary d-flex align-items-center gap-1" onClick={openAdd}>
            <IconPlus size={16} stroke={1.5} /> Add
          </button>
          <button className="btn btn-outline-secondary d-flex align-items-center gap-1"
            onClick={() => { setMode('import'); setImportError(''); setImportSuccess('') }}>
            <IconUpload size={16} stroke={1.5} /> Import CSV / Excel
          </button>
        </div>
      </div>

      <Alert message={error} />

      {(mode === 'add' || mode === 'edit') && TransactionForm}
      {mode === 'import' && ImportForm}

      {/* Table */}
      <div className="card">
        <div className="card-header d-flex align-items-center justify-content-between gap-2 flex-wrap">
          <form className="d-flex gap-2" onSubmit={handleSearch}>
            <div className="input-group">
              <input
                type="text" className="form-control form-control-sm"
                placeholder="Search transactions..."
                value={searchInput} onChange={e => setSearchInput(e.target.value)}
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
              <button className="btn btn-sm btn-danger ms-2"
                onClick={() => selected.forEach(handleDelete)}>
                <IconTrash size={14} stroke={1.5} /> Delete selected
              </button>
            </span>
          )}
        </div>

        <div className="table-responsive">
          <table className="table table-vcenter table-hover card-table">
            <thead>
              <tr>
                <th style={{ width: 40 }}>
                  <input type="checkbox" className="form-check-input m-0"
                    checked={allSelected} onChange={toggleAll} />
                </th>
                <th>Date</th>
                <th>Account</th>
                <th>Type</th>
                <th>Category</th>
                <th className="text-end">Amount</th>
                <th style={{ width: 100 }} />
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan={7} className="text-center py-5 text-secondary">Loading...</td></tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-5 text-secondary">
                    No transactions found.{' '}
                    <button className="btn btn-link p-0" onClick={openAdd}>Create one</button>
                  </td>
                </tr>
              ) : transactions.map(tx => {
                const badge = TYPE_BADGE[tx.type] ?? { cls: 'bg-secondary-lt', icon: null }
                return (
                  <tr key={tx.id}>
                    <td>
                      <input type="checkbox" className="form-check-input m-0"
                        checked={selected.includes(tx.id)} onChange={() => toggleOne(tx.id)} />
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
                    <td className="text-end fw-medium">
                      <span className={tx.type === 'income' ? 'text-green' : 'text-red'}>
                        {tx.type === 'expense' ? '−' : '+'}{fmt(tx.amount)}
                      </span>
                    </td>
                    <td>
                      <div className="d-flex gap-1 justify-content-end">
                        <button className="btn btn-sm btn-ghost-secondary" title="View"
                          onClick={() => setViewTx(tx)}>
                          <IconEye size={16} stroke={1.5} />
                        </button>
                        <button className="btn btn-sm btn-ghost-secondary" title="Edit"
                          onClick={() => openEdit(tx)}>
                          <IconEdit size={16} stroke={1.5} />
                        </button>
                        <button className="btn btn-sm btn-ghost-danger" title="Delete"
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

      {/* View modal */}
      {viewTx && (
        <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Transaction detail</h5>
                <button className="btn-close" onClick={() => setViewTx(null)} />
              </div>
              <div className="modal-body">
                <div className="row g-3">
                  {[
                    { label: 'Date',    value: fmtDate(viewTx.date ?? viewTx.created_at) },
                    { label: 'Amount',  value: <span className={viewTx.type === 'income' ? 'text-green fw-bold' : 'text-red fw-bold'}>{viewTx.type === 'expense' ? '−' : '+'}{fmt(viewTx.amount)}</span> },
                    { label: 'Type',    value: <span className={`badge ${TYPE_BADGE[viewTx.type]?.cls ?? 'bg-secondary-lt'} d-inline-flex align-items-center gap-1`}>{TYPE_BADGE[viewTx.type]?.icon}{viewTx.type}</span> },
                    { label: 'Account', value: <span className="badge bg-blue-lt text-blue">{accountMap[viewTx.account_id] ?? '—'}</span> },
                    { label: 'Category',value: <span className="badge bg-purple-lt text-purple">{categoryMap[viewTx.category_id] ?? '—'}</span> },
                    { label: 'Description', value: viewTx.description || '—' },
                    { label: 'ID',      value: <code className="small">{viewTx.id}</code> },
                  ].map(({ label, value }) => (
                    <div key={label} className="col-6">
                      <div className="text-secondary small mb-1">{label}</div>
                      <div>{value}</div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="modal-footer">
                <button className="btn btn-outline-secondary" onClick={() => setViewTx(null)}>Close</button>
                <button className="btn btn-primary" onClick={() => { openEdit(viewTx); setViewTx(null) }}>
                  <IconEdit size={14} stroke={1.5} className="me-1" /> Edit
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete modal */}
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
                <button className="btn btn-outline-secondary" onClick={() => setDeleteId(null)}>Cancel</button>
                <button className="btn btn-danger" onClick={() => handleDelete(deleteId)}>Delete</button>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}