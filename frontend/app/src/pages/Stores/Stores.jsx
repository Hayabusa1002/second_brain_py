import { useState, useEffect } from 'react'
import { IconPlus, IconUpload } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import ViewModal from './ViewModal'
import ImportModal from './ImportModal'
import DeleteModal from './DeleteModal'
import SubcategoryModal from './SubcategoryModal'

const EMPTY_FORM = {
  name: '',
  type: '',
  address: '',
  website: '',
}

export default function Stores() {
  const [stores, setStores] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState('table')
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [viewStore, setViewStore] = useState(null)
  const [deleteStore, setDeleteStore] = useState(null)
  const [subcategoryStore, setSubcategoryStore] = useState(null)

  useEffect(() => {
    fetchStores()
  }, [])

  async function fetchStores() {
    setLoading(true)
    setError('')

    try {
      const { data } = await client.get('/stores')
      setStores(data.stores ?? data.items ?? data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load stores.')
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

  function openEdit(store) {
    setForm({
      name: store.name ?? '',
      type: store.type ?? '',
      address: store.address ?? '',
      website: store.website ?? '',
    })
    setEditId(store.id)
    setFormError('')
    setMode('edit')
  }

  function openView(store) {
    setViewStore(store)
  }

  function openDeleteModal(store) {
    setDeleteStore(store)
  }

  function openAssignSubcategory(store) {
    setSubcategoryStore(store)
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
        name: form.name.trim(),
        type: form.type,
        address: form.address.trim() || null,
        website: form.website.trim() || null,
      }

      if (mode === 'edit') {
        await client.patch(`/stores/${editId}`, payload)
      } else {
        await client.post('/stores', payload)
      }

      setMode('table')
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      await fetchStores()
    } catch (err) {
      setFormError(
        err.response?.data?.detail ??
          err.response?.data ??
          err.message ??
          'Failed to save store.'
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!deleteStore) return

    try {
      await client.delete(`/stores/${deleteStore.id}`)
      setDeleteStore(null)
      await fetchStores()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete store.')
      setDeleteStore(null)
    }
  }

  async function handleStoreSubcategoriesUpdate() {
    setSubcategoryStore(null)
    await fetchStores()
  }

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h2 className="mb-0">Stores</h2>
        </div>

        <div className="d-flex gap-2">
          <button
            className="btn btn-outline-primary d-flex align-items-center gap-1"
            onClick={openAdd}
          >
            <IconPlus size={16} stroke={1.5} />
            New Store
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
          onCancel={() => {
            setMode('table')
            setForm({ ...EMPTY_FORM })
            setEditId(null)
            setFormError('')
          }}
        />
      )}

      {mode === 'import' && (
        <ImportModal
          onClose={() => setMode('table')}
          onSuccess={fetchStores}
        />
      )}

      <Table
        stores={stores}
        loading={loading}
        onShow={openView}
        onEdit={openEdit}
        onDelete={openDeleteModal}
        onAdd={openAdd}
        onAssignSubcategory={openAssignSubcategory}
      />

      {viewStore && (
        <ViewModal
          store={viewStore}
          onClose={() => setViewStore(null)}
        />
      )}

      {deleteStore && (
        <DeleteModal
          store={deleteStore}
          onConfirm={handleDelete}
          onCancel={() => setDeleteStore(null)}
        />
      )}

      {subcategoryStore && (
        <SubcategoryModal
          store={subcategoryStore}
          onClose={() => setSubcategoryStore(null)}
          onUpdate={handleStoreSubcategoriesUpdate}
        />
      )}
    </div>
  )
}