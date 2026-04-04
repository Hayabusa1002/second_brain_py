import { useState, useEffect } from 'react'
import { IconPlus } from '@tabler/icons-react'
import client from '../../api/client'
import Alert from '../../components/ui/Alert'
import Table from './Table'
import FormModal from './FormModal'
import DeleteModal from './DeleteModal'

const EMPTY_FORM = {
  name: '',
  country: '',
}

export default function Cities() {
  const [cities, setCities] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [mode, setMode] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [editId, setEditId] = useState(null)
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')

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
      setError('Failed to load cities.')
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
      country: c.country ?? '',
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
        country: form.country,
      }

      if (mode === 'edit') {
        await client.put(`/cities/${editId}`, payload)
      } else {
        await client.post('/cities', payload)
      }

      setMode(null)
      setForm({ ...EMPTY_FORM })
      setEditId(null)
      fetchCities()
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to save city.')
    } finally {
      setSaving(false)
    }
  }

  function openDeleteModal(city) {
    setDeleteCity(city)
  }

  async function handleDelete() {
    if (!deleteCity) return
    try {
      await client.delete(`/cities/${deleteCity.id}`)
      setDeleteCity(null)
      fetchCities()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete city.')
      setDeleteCity(null)
    }
  }

  return (
    <div className="container-xl py-4">
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h2 className="mb-0">Cities</h2>

        <button
          className="btn btn-primary d-flex align-items-center gap-1"
          onClick={openAdd}
        >
          <IconPlus size={16} stroke={1.5} /> New city
        </button>
      </div>

      <Alert message={error} />

      <Table
        cities={cities}
        loading={loading}
        onEdit={openEdit}
        onDelete={openDeleteModal}
        onAdd={openAdd}
      />

      {mode && (
        <FormModal
          key={mode === 'add' ? 'add-city' : `edit-city-${editId}`}
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