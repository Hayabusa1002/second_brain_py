import { useState, useEffect, useMemo } from 'react'
import { IconPlus } from '@tabler/icons-react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import DeleteModal from './DeleteModal'
import OwnersModal from './OwnersModal'

const EMPTY_FORM = { name: '', type: 'individual' }

export default function Accounts() {
  const { user } = useAuth()

  const [accounts, setAccounts] = useState([])
  const [allUsers, setAllUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null) // 'add' | 'edit'
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [deleteAccount, setDeleteAccount] = useState(null)
  const [ownersAccount, setOwnersAccount] = useState(null)

  const canManageSharedAccounts =
    user?.role === 'admin' || user?.role === 'owner'

  const individualAccountsCount = useMemo(() => {
    return accounts.filter(acc => acc.type === 'individual').length
  }, [accounts])

  useEffect(() => {
    fetchAccounts()
  }, [])

  useEffect(() => {
    if (!canManageSharedAccounts) {
      setAllUsers([])
      return
    }
    fetchUsers()
  }, [canManageSharedAccounts])

  async function fetchAccounts() {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/accounts')
      setAccounts(data.items ?? data)
    } catch {
      setError('Failed to load accounts.')
    } finally {
      setLoading(false)
    }
  }

  async function fetchUsers() {
    try {
      const { data } = await client.get('/accounts/users/active')
      setAllUsers(data.users)
    } catch (err) {
      if (err.response?.status !== 403) {
        console.error('users error:', err)
      }
    }
  }

  function openAdd() {
    setForm({ ...EMPTY_FORM })
    setEditId(null)
    setFormError('')
    setMode('add')
  }

  function openEdit(acc) {
    setForm({ name: acc.name, type: acc.type })
    setEditId(acc.id)
    setFormError('')
    setMode('edit')
  }

  function openDelete(acc) {
    const isLastIndividual =
      acc.type === 'individual' && individualAccountsCount <= 1

    if (isLastIndividual) {
      setError('You must keep at least one individual account.')
      return
    }

    setError('')
    setDeleteAccount(acc)
  }

  const setField = (field) => (e) =>
    setForm(prev => ({ ...prev, [field]: e.target.value }))

  async function handleSave(e) {
    e.preventDefault()
    setSaving(true)
    setFormError('')
    try {
      if (mode === 'edit') {
        await client.put(`/accounts/${editId}`, form)
      } else {
        await client.post('/accounts', form)
      }
      setMode(null)
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      fetchAccounts()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save account.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    try {
      setError('')

      await client.delete(`/accounts/${deleteAccount.id}`)

      setDeleteAccount(null)
      fetchAccounts()
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        (err.response?.status === 403
          ? 'You do not have permission to delete this account.'
          : 'Failed to delete account.')

      setError(message)
      setDeleteAccount(null)
    }
  }

  function handleOwnersUpdate(accountId, updatedOwners, selfRemoved = false) {
    if (selfRemoved) {
      setAccounts(prev => prev.filter(a => a.id !== accountId))
      setOwnersAccount(null)
    } else {
      setAccounts(prev =>
        prev.map(a => (a.id === accountId ? { ...a, owners: updatedOwners } : a))
      )
      setOwnersAccount(prev => (prev ? { ...prev, owners: updatedOwners } : null))
    }
  }

  return (
    <div className="container-xl py-4">

      {/* Header */}
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h2 className="mb-0">Accounts</h2>
        <button
          className="btn btn-primary d-flex align-items-center gap-1"
          onClick={openAdd}
        >
          <IconPlus size={16} stroke={1.5} /> New account
        </button>
      </div>

      <Alert message={error} />

      <Table
        accounts={accounts}
        loading={loading}
        onEdit={openEdit}
        onDelete={openDelete}
        onOwners={setOwnersAccount}
        onAdd={openAdd}
        individualAccountsCount={individualAccountsCount}
        currentUser={user}
      />

      {mode && (
        <FormModal
          form={form}
          mode={mode}
          saving={saving}
          error={formError}
          onChange={setField}
          onSave={handleSave}
          onCancel={() => setMode(null)}
        />
      )}

      {deleteAccount && (
        <DeleteModal
          account={deleteAccount}
          onConfirm={handleDelete}
          onCancel={() => setDeleteAccount(null)}
        />
      )}

      {ownersAccount && (
        <OwnersModal
          account={ownersAccount}
          currentUser={user}
          allUsers={allUsers}
          onClose={() => setOwnersAccount(null)}
          onUpdate={handleOwnersUpdate}
        />
      )}

    </div>
  )
}