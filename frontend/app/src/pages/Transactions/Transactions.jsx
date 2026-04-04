import { useState, useEffect, useCallback } from 'react'
import { IconPlus, IconUpload } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import Filters from './Filters'
import FormModal from './FormModal'
import ImportModal from './ImportModal'
import ViewModal from './ViewModal'
import DeleteModal from './DeleteModal'

const PAGE_SIZE = 10
const EMPTY_FORM = {
  account_id: '',
  category_id: '',
  amount: '',
  type: 'expense',
  date: '',
  description: '',
}
const EMPTY_FILTERS = {
  account_id: '',
  type: '',
  category_id: '',
  date_from: '',
  date_to: '',
}

export default function Transactions() {
  const [transactions, setTransactions] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selected, setSelected] = useState([])
  const [accounts, setAccounts] = useState([])
  const [categories, setCategories] = useState([])
  const [accountMap, setAccountMap] = useState({})
  const [categoryMap, setCategoryMap] = useState({})

  const [filters, setFilters] = useState(EMPTY_FILTERS)
  const [activeFilters, setActiveFilters] = useState(EMPTY_FILTERS)

  const [mode, setMode] = useState('table')
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')
  const [viewTx, setViewTx] = useState(null)
  const [deleteId, setDeleteId] = useState(null)

  const totalPages = Math.ceil(total / PAGE_SIZE) || 1

  const fetchTransactions = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/transactions', {
        params: {
          page,
          limit: PAGE_SIZE,
          account_id: activeFilters.account_id || undefined,
          type: activeFilters.type || undefined,
          category_id: activeFilters.category_id || undefined,
          date_from: activeFilters.date_from || undefined,
          date_to: activeFilters.date_to || undefined,
        },
      })

      // backend ahora siempre responde { items, total, page, limit }
      setTransactions(data.items || [])
      setTotal(typeof data.total === 'number' ? data.total : (data.items || []).length)
    } catch {
      setError('Failed to load transactions.')
    } finally {
      setLoading(false)
    }
  }, [page, activeFilters])

  useEffect(() => {
    fetchTransactions()
  }, [fetchTransactions])

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
        const accMap = {}
        accs.forEach((a) => {
          accMap[a.id] = a.name
        })
        const catMap = {}
        cats.forEach((c) => {
          catMap[c.id] = c.name
        })
        setAccountMap(accMap)
        setCategoryMap(catMap)
      } catch (e) {
        console.error(e)
      }
    }
    fetchMeta()
  }, [])

  function handleFilterChange(key, value) {
    setFilters((f) => ({ ...f, [key]: value }))
  }

  function applyFilters() {
    setPage(1)
    setActiveFilters(filters)
  }

  function clearFilters() {
    setFilters(EMPTY_FILTERS)
    setActiveFilters(EMPTY_FILTERS)
    setPage(1)
  }

  function toggleAll() {
    const allIds = transactions.map((t) => t.id)
    const allSelected = allIds.every((id) => selected.includes(id))
    setSelected(allSelected ? [] : allIds)
  }

  function toggleOne(id) {
    setSelected((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]))
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
      account_id: tx.account_id ?? '',
      category_id: tx.category_id ?? '',
      amount: tx.amount ?? '',
      type: tx.type ?? 'expense',
      date: tx.date ?? '',
      description: tx.description ?? '',
    })
    setEditId(tx.id)
    setFormError('')
    setMode('edit')
  }

  const setField =
    (f) =>
    (e) =>
      setForm((prev) => ({ ...prev, [f]: e.target.value }))

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
          <button
            className="btn btn-outline-primary d-flex align-items-center gap-1"
            onClick={() => setMode('import')}
          >
            <IconUpload size={16} stroke={1.5} /> Import CSV / Excel
          </button>
        </div>
      </div>

      <Alert message={error} />

      {(mode === 'add' || mode === 'edit') && (
        <FormModal
          form={form}
          accounts={accounts}
          categories={categories}
          mode={mode}
          saving={saving}
          error={formError}
          onChange={setField}
          onSave={handleSave}
          onCancel={() => setMode('table')}
        />
      )}

      {mode === 'import' && (
        <ImportModal onClose={() => setMode('table')} onSuccess={fetchTransactions} />
      )}

      <Filters
        accounts={accounts}
        categories={categories}
        filters={filters}
        onChange={handleFilterChange}
        onFilter={applyFilters}
        onClear={clearFilters}
        transactions={transactions}
      />

      <Table
        transactions={transactions}
        accountMap={accountMap}
        categoryMap={categoryMap}
        selected={selected}
        loading={loading}
        page={page}
        totalPages={totalPages}
        total={total}
        onToggleAll={toggleAll}
        onToggleOne={toggleOne}
        onView={setViewTx}
        onEdit={openEdit}
        onDelete={setDeleteId}
        onPageChange={setPage}
        onAdd={openAdd}
      />

      {viewTx && (
        <ViewModal
          tx={viewTx}
          accountMap={accountMap}
          categoryMap={categoryMap}
          onClose={() => setViewTx(null)}
          onEdit={openEdit}
        />
      )}

      {deleteId && (
        <DeleteModal
          onConfirm={() => handleDelete(deleteId)}
          onCancel={() => setDeleteId(null)}
        />
      )}
    </div>
  )
}