import { useState, useEffect } from 'react'
import { IconPlus } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = {
  name: '',
  category_id: '',
  city_id: '',
  price: '',
}

export default function Items() {
  const [items, setItems] = useState([])
  const [categories, setCategories] = useState([])
  const [cities, setCities] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [deleteItem, setDeleteItem] = useState(null)

  useEffect(() => {
    fetchAll()
  }, [])

  async function fetchAll() {
    setLoading(true)
    setError('')
    try {
      const [itemsRes, catsRes, citiesRes] = await Promise.all([
        client.get('/items'),
        client.get('/categories'),
        client.get('/cities'),
      ])

      setItems(itemsRes.data.items ?? itemsRes.data)
      setCategories(catsRes.data.categories ?? catsRes.data)
      setCities(citiesRes.data.cities ?? citiesRes.data)
    } catch (err) {
      setError('Failed to load items.')
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

  function openEdit(i) {
    setForm({
      name: i.name ?? '',
      category_id: i.category_id ?? '',
      city_id: i.city_id ?? '',
      price: i.price ?? '',
    })
    setEditId(i.id)
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
        category_id: form.category_id || null,
        city_id: form.city_id || null,
        price: form.price ? Number(form.price) : null,
      }

      if (mode === 'edit') {
        await client.put(`/items/${editId}`, payload)
      } else {
        await client.post('/items', payload)
      }

      setMode(null)
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      fetchAll()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save item.')
    } finally {
      setSaving(false)
    }
  }

  function openDeleteModal(item) {
    setDeleteItem(item)
  }

  async function handleDelete() {
    if (!deleteItem) return
    try {
      await client.delete(`/items/${deleteItem.id}`)
      setDeleteItem(null)
      fetchAll()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete item.')
      setDeleteItem(null)
    }
  }

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h2 className="mb-0">Items</h2>

        <button
          className="btn btn-primary d-flex align-items-center gap-1"
          onClick={openAdd}
        >
          <IconPlus size={16} stroke={1.5} /> New item
        </button>
      </div>

      <Alert message={error} />

      <Table
        items={items}
        categories={categories}
        cities={cities}
        loading={loading}
        onEdit={openEdit}
        onDelete={openDeleteModal}
        onAdd={openAdd}
      />

      {mode && (
        <FormModal
          key={mode === 'add' ? 'add-item' : `edit-item-${editId}`}
          form={form}
          categories={categories}
          cities={cities}
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

      {deleteItem && (
        <DeleteModal
          item={deleteItem}
          onConfirm={handleDelete}
          onCancel={() => setDeleteItem(null)}
        />
      )}
    </div>
  )
}