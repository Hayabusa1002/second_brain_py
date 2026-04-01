import { useState, useEffect } from 'react'
import { IconPlus } from '@tabler/icons-react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import BanModal from './BanModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = { name: '', email: '', password: '', role: 'partner' }

export default function Users() {
  const { user: currentUser } = useAuth()

  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null) // 'add' | 'edit'
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [banUser, setBanUser] = useState(null)
  const [deleteUser, setDeleteUser] = useState(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  async function fetchUsers() {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/users')
      setUsers(data.users ?? data.items ?? data)
    } catch (err) {
      if (err.response?.status === 403) {
        setError('You do not have permission to view users.')
      } else {
        setError('Failed to load users.')
      }
    } finally {
      setLoading(false)
    }
  }

  function openAdd() {
    setForm({ ...EMPTY_FORM })
    setEditId(null)
    setFormError('')
    setMode('add')
  }

  function openEdit(u) {
    setForm({
      name: u.name ?? '',
      email: u.email ?? '',
      password: '',
      role: u.role ?? 'partner',
    })
    setEditId(u.id)
    setFormError('')
    setMode('edit')
  }

  const setField =
    (field) =>
      (e) =>
        setForm((prev) => ({ ...prev, [field]: e.target.value }))

  async function handleSave(e) {
    e.preventDefault()
    setSaving(true)
    setFormError('')
    try {
      if (mode === 'edit') {
        await client.put(`/users/${editId}`, {
          name: form.name,
          email: form.email,
          role: form.role,
        })
      } else {
        await client.post('/auth/register', {
          name: form.name,
          email: form.email,
          password: form.password,
          role: form.role,
        })
      }
      setMode(null)
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      fetchUsers()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save user.')
    } finally {
      setSaving(false)
    }
  }

  // ---- Status transitions ----

  async function handleApprove(user) {
    try {
      await client.post(`/users/${user.id}/approve`)
      fetchUsers()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to approve user.')
    }
  }

  async function handleReject(user) {
    try {
      await client.post(`/users/${user.id}/reject`)
      fetchUsers()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reject user.')
    }
  }

  function openBanModal(user) {
    setBanUser(user)
  }

  async function handleBan() {
    if (!banUser) return
    try {
      const endpoint =
        banUser.status === 'banned'
          ? `/users/${banUser.id}/unban`
          : `/users/${banUser.id}/ban`
      await client.post(endpoint)
      setBanUser(null)
      fetchUsers()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update user status.')
      setBanUser(null)
    }
  }

  async function handleReopen(user) {
    try {
      await client.post(`/users/${user.id}/reopen`)
      fetchUsers()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reopen user request.')
    }
  }

  // ---- Delete ----

  function openDeleteModal(user) {
    setDeleteUser(user)
  }

  async function handleDelete() {
    if (!deleteUser) return
    try {
      await client.delete(`/users/${deleteUser.id}`)
      setDeleteUser(null)
      fetchUsers()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete user.')
      setDeleteUser(null)
    }
  }

  const isForbidden = error === 'You do not have permission to view users.'

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h2 className="mb-0">Users</h2>

        {/* If no permission, do not show add button */}
        {!isForbidden && (
          <button
            className="btn btn-primary d-flex align-items-center gap-1"
            onClick={openAdd}
          >
            <IconPlus size={16} stroke={1.5} /> New user
          </button>
        )}
      </div>

      <Alert message={error} />

      {/* If 403, do not show anything else */}
      {isForbidden ? null : (
        <>
          <Table
            users={users}
            currentUserId={currentUser?.id}
            loading={loading}
            onEdit={openEdit}
            onApprove={handleApprove}
            onReject={handleReject}
            onBan={openBanModal}
            onUnban={(u) => openBanModal(u)} // reuses same modal
            onReopen={handleReopen}
            onDelete={openDeleteModal}
            onAdd={openAdd}
          />

          {mode && (
            <FormModal
              key={mode === 'add' ? 'add-user' : `edit-user-${editId}`}
              form={form}
              mode={mode}
              saving={saving}
              error={formError}
              onChange={setField}
              onSave={handleSave}
              onCancel={() => {
                setMode(null)
                setForm({ ...EMPTY_FORM })
                setEditId(null)
                setFormError('')
              }}
            />
          )}

          {banUser && (
            <BanModal
              user={banUser}
              onConfirm={handleBan}
              onCancel={() => setBanUser(null)}
            />
          )}

          {deleteUser && (
            <DeleteModal
              user={deleteUser}
              onConfirm={handleDelete}
              onCancel={() => setDeleteUser(null)}
            />
          )}
        </>
      )}
    </div>
  )
}