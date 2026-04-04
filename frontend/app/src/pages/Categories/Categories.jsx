import { useState, useEffect } from 'react'
import { IconPlus } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import SubcategoryModal from './SubcategoryModal'
import ViewModal from './ViewModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = {
  name: '',
  type: 'expense',
}

export default function Categories() {
  const [categories, setCategories] = useState([])
  const [subcategories, setSubcategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [viewCategory, setViewCategory] = useState(null)
  const [subcategoryCategory, setSubcategoryCategory] = useState(null)
  const [deleteCategory, setDeleteCategory] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  async function fetchData() {
    setLoading(true)
    setError('')

    try {
      const [categoriesRes, subcategoriesRes] = await Promise.all([
        client.get('/categories'),
        client.get('/subcategories'),
      ])

      setCategories(categoriesRes.data.categories ?? categoriesRes.data.items ?? categoriesRes.data)
      setSubcategories(
        subcategoriesRes.data.subcategories ??
        subcategoriesRes.data.items ??
        subcategoriesRes.data
      )
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load categories.')
    } finally {
      setLoading(false)
    }
  }

  function getSubcategories(categoryId) {
    return subcategories.filter((s) => s.category_id === categoryId)
  }

  function handleSubcategoriesUpdate(categoryId, updatedSubs) {
    setSubcategories((prev) => {
      const withoutCurrent = prev.filter((item) => item.category_id !== categoryId)
      return [...withoutCurrent, ...updatedSubs]
    })
  }

  function openAdd() {
    setForm({ ...EMPTY_FORM })
    setEditId(null)
    setFormError('')
    setMode('add')
  }

  function openEdit(category) {
    setForm({
      name: category?.name ?? '',
      type: category?.type ?? 'expense',
    })
    setEditId(category?.id ?? null)
    setFormError('')
    setMode('edit')
  }

  function openView(category) {
    setViewCategory(category)
  }

  function openSubcategories(category) {
    setSubcategoryCategory(category)
  }

  function openDeleteModal(category) {
    setDeleteCategory(category)
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
      }

      if (mode === 'edit') {
        await client.put(`/categories/${editId}`, payload)
      } else {
        await client.post('/categories', payload)
      }

      setMode(null)
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      fetchData()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save category.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!deleteCategory) return

    try {
      await client.delete(`/categories/${deleteCategory.id}`)
      setDeleteCategory(null)
      fetchData()
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
          <IconPlus size={16} stroke={1.5} />
          New Category
        </button>
      </div>

      <Alert message={error} />

      <Table
        categories={categories}
        getSubcategories={getSubcategories}
        loading={loading}
        onShow={openView}
        onEdit={openEdit}
        onSubcategory={openSubcategories}
        onDelete={openDeleteModal}
        onAdd={openAdd}
      />

      {mode && (
        <FormModal
          key={mode === 'edit' ? `edit-category-${editId}` : 'add-category'}
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

      {subcategoryCategory && (
        <SubcategoryModal
          category={subcategoryCategory}
          subcategories={getSubcategories(subcategoryCategory.id)}
          onClose={() => setSubcategoryCategory(null)}
          onUpdate={handleSubcategoriesUpdate}
        />
      )}

      {viewCategory && (
        <ViewModal
          category={viewCategory}
          subcategories={getSubcategories(viewCategory.id)}
          onClose={() => setViewCategory(null)}
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