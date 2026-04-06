import { useState, useEffect } from 'react'
import { IconPlus, IconUpload } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import ViewModal from './ViewModal'
import ImportModal from './ImportModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = {
  name: '',
  state: '',
  country: '',
}

export default function Cities() {
  const [cities, setCities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState('table')
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

  const [viewCity, setViewCity] = useState(null)
  const [deleteCity, setDeleteCity] = useState(null)

  useEffect(() => {
    fetchCities()
  }, [])

  async function fetchCities() {
    setLoading(true)
    setError('')
    try {
      const { data } = await client.get('/cities')
      setCities(data.cities ?? data.items ?? data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load cities.')
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
      state: c.state ?? '',
      country: c.country ?? '',
    })
    setEditId(c.id)
    setFormError('')
    setMode('edit')
  }

  function openView(city) {
    setViewCity(city)
  }

  function openDeleteModal(city) {
    setDeleteCity(city)
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
        state: form.state,
        country: form.country,
      }

      if (mode === 'edit') {
        await client.put(`/cities/${editId}`, payload)
      } else {
        await client.post('/cities', payload)
      }

      setMode('table')
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      await fetchCities()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save city.')
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete() {
    if (!deleteCity) return
    try {
      await client.delete(`/cities/${deleteCity.id}`)
      setDeleteCity(null)
      await fetchCities()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete city.')
      setDeleteCity(null)
    }
  }

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <h2 className="mb-0">Cities</h2>
        </div>

        <div className="d-flex gap-2">
          <button
            className="btn btn-outline-primary d-flex align-items-center gap-1"
            onClick={openAdd}
          >
            <IconPlus size={16} stroke={1.5} />
            New City
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
          onSuccess={fetchCities}
        />
      )}

      <Table
        cities={cities}
        loading={loading}
        onShow={openView}
        onEdit={openEdit}
        onDelete={openDeleteModal}
        onAdd={openAdd}
      />

      {viewCity && (
        <ViewModal
          city={viewCity}
          onClose={() => setViewCity(null)}
        />
      )}

      {deleteCity && (
        <DeleteModal
          city={deleteCity}
          onConfirm={handleDelete}
          onCancel={() => setDeleteCity(null)}
        />
      )}
    </div>
  )
}