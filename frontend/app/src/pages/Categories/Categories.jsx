import { useState, useEffect, useCallback } from 'react'
import { IconPlus, IconUpload } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import ImportModal from './ImportModal'
import SubcategoryModal from './SubcategoryModal'
import ViewModal from './ViewModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = {
  name: '',
  type: 'expense',
}

export default function Categories() {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState('table')
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [viewCategory, setViewCategory] = useState(null)
  const [subcategoryCategory, setSubcategoryCategory] = useState(null)
  const [deleteCategory, setDeleteCategory] = useState(null)

  const normalizeCategories = (data) => {
    if (Array.isArray(data?.categories)) return data.categories
    if (Array.isArray(data?.items)) return data.items
    if (Array.isArray(data)) return data
    return []
  }

  const fetchData = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const res = await client.get('/categories')
      const items = normalizeCategories(res.data)
      setCategories(items)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load categories.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  function getSubcategories(categoryId) {
    const category = categories.find((item) => item.id === categoryId)
    return category?.subcategories ?? []
  }

  function handleSubcategoriesUpdate(categoryId, updatedSubs) {
    setCategories((prev) =>
      prev.map((category) =>
        category.id === categoryId
          ? {
              ...category,
              subcategories: Array.isArray(updatedSubs) ? updatedSubs : [],
            }
          : category
      )
    )
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
        await client.patch(`/categories/${editId}`, payload)
      } else {
        await client.post('/categories', payload)
      }

      setMode('table')
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      await fetchData()
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
      await fetchData()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete category.')
      setDeleteCategory(null)
    }
  }

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h2 className="mb-0">Categories</h2>
        </div>

        <div className="d-flex gap-2">
          <button
            className="btn btn-outline-primary d-flex align-items-center gap-1"
            onClick={openAdd}
          >
            <IconPlus size={16} stroke={1.5} />
            New Category
          </button>

          <button
            className="btn btn-outline-primary d-flex align-items-center gap-1"
            onClick={() => setMode('import')}
          >
            <IconUpload size={16} stroke={1.5} />
            Import
          </button>
        </div>
      </div>

      <Alert message={error} />

      {(mode === 'add' || mode === 'edit') && (
        <FormModal
          form={form}
          mode={mode}
          saving={saving}
          error={formError}
          onChange={setField}
          onSave={handleSave}
          onCancel={() => setMode('table')}
        />
      )}

      {mode === 'import' && (
        <ImportModal
          onClose={() => setMode('table')}
          onSuccess={fetchData}
        />
      )}

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