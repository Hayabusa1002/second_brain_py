import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import parseErrors from '../../utils/forms/parseErrors'
import validateForm from '../../utils/users/validateForm'

const EMPTY_FORM = { name: '', email: '', password: '', role: 'partner' }

export default function useUsers() {
  const { user: currentUser } = useAuth()

  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null) // 'add' | 'edit'
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})

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
    setFieldErrors({})
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
    setFieldErrors({})
    setMode('edit')
  }

  const setField = (field) => (e) => {
    const value = e.target.value

    setForm((prev) => ({ ...prev, [field]: value }))

    if (fieldErrors[field]) {
      setFieldErrors((prev) => ({ ...prev, [field]: '' }))
    }

    if (formError) setFormError('')
  }

  async function handleSave(e) {
    e.preventDefault()
    if (!mode) return

    setSaving(true)
    setFormError('')
    setFieldErrors({})

    const localErrors = validateForm(form, mode)

    if (Object.keys(localErrors).length > 0) {
      setFieldErrors(localErrors)
      setFormError('Please review the highlighted fields.')
      setSaving(false)
      return
    }

    try {
      if (mode === 'edit') {
        await client.put(`/users/${editId}`, {
          name: form.name.trim(),
          email: form.email.trim(),
          role: form.role,
        })
      } else {
        await client.post('/users', {
          name: form.name.trim(),
          email: form.email.trim(),
          password: form.password,
          role: form.role,
        })
      }

      resetFormState()
      fetchUsers()
    } catch (err) {
      const parsed = parseErrors(err, 'Failed to save user.')
      setFormError(parsed.error)
      setFieldErrors(parsed.fieldErrors)
    } finally {
      setSaving(false)
    }
  }

  function resetFormState() {
    setMode(null)
    setForm({ ...EMPTY_FORM })
    setEditId(null)
    setFormError('')
    setFieldErrors({})
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

  return {
    currentUser,
    users,
    loading,
    error,
    isForbidden,

    mode,
    form,
    editId,
    saving,
    formError,
    fieldErrors,

    banUser,
    deleteUser,

    openAdd,
    openEdit,
    setField,
    handleSave,
    resetFormState,

    openBanModal,
    handleBan,
    openDeleteModal,
    handleDelete,
    handleApprove,
    handleReject,
    handleReopen,

    setBanUser,
    setDeleteUser,
  }
}