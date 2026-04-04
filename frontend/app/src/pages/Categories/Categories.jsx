import { useState, useEffect } from 'react'
import { IconPlus } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = {
  name: '',
  type: 'expense', 
  parent_id: null, 
}

export default function Categories() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null) // 'add' | 'edit'
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [deleteCategory, setDeleteCategory] = useState(null)

  useEffect(() => {
    fetchCategories()
  }, [])

  async function fetchCategories() {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/categories')
      setCategories(data.categories ?? data.items ?? data)
    } catch (err) {
      setError('Failed to load categories.')
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

  function openEdit(c) {
    setForm({
      name: c.name ?? '',
      type: c.type ?? 'expense',
      parent_id: c.parent_id ?? null,
    })
    setEditId(c.id)
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
      const payload = {
        name: form.name,
        type: form.type,
        parent_id: form.parent_id || null,
      }

      if (mode === 'edit') {
        await client.put(`/categories/${editId}`, payload)
      } else {
        await client.post('/categories', payload)
      }

      setMode(null)
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      fetchCategories()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save category.')
    } finally {
      setSaving(false)
    }
  }

  function openDeleteModal(category) {
    setDeleteCategory(category)
  }

  async function handleDelete() {
    if (!deleteCategory) return
    try {
      await client.delete(`/categories/${deleteCategory.id}`)
      setDeleteCategory(null)
      fetchCategories()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete category.')
      setDeleteCategory(null)
    }
  }

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h2 className="mb-0">Categories</h2>

        <button
          className="btn btn-primary d-flex align-items-center gap-1"
          onClick={openAdd}
        >
          <IconPlus size={16} stroke={1.5} /> New category
        </button>
      </div>

      <Alert message={error} />

      <Table
        categories={categories}
        loading={loading}
        onEdit={openEdit}
        onDelete={openDeleteModal}
        onAdd={openAdd}
      />

      {mode && (
        <FormModal
          key={mode === 'add' ? 'add-category' : `edit-category-${editId}`}
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

      {deleteCategory && (
        <DeleteModal
          category={deleteCategory}
          onConfirm={handleDelete}
          onCancel={() => setDeleteCategory(null)}
        />
      )}
    </div>
  )
}