import { useEffect, useState } from 'react'
import client from '../../api/client'

function normalizeError(error) {
  if (!error) return ''
  if (typeof error === 'string') return error
  if (Array.isArray(error)) {
    return error
      .map((item) => {
        if (typeof item === 'string') return item
        if (item?.message) return item.message
        if (item?.msg) return item.msg
        return JSON.stringify(item)
      })
      .join(', ')
  }
  if (typeof error === 'object') {
    if (error.detail) return normalizeError(error.detail)
    if (error.message) return error.message
    return JSON.stringify(error)
  }
  return String(error)
}

export default function SubcategoryModal({
  store,
  subcategories,
  onClose,
  onUpdated,
}) {
  const [items, setItems] = useState(subcategories ?? [])
  const [selectedId, setSelectedId] = useState(
    store?.category_default?.subcategory?.id ?? ''
  )
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setItems(subcategories ?? [])
    setSelectedId(store?.category_default?.subcategory?.id ?? '')
  }, [subcategories, store?.id])

  async function handleAssign() {
    if (!store?.id || !selectedId) return

    setSaving(true)
    setError('')

    try {
      await client.put(`/stores/${store.id}/category-default`, {
        subcategory_id: selectedId,
      })

      await onUpdated()
      onClose()
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to assign subcategory.'
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleClear() {
    if (!store?.id) return

    setSaving(true)
    setError('')

    try {
      await client.delete(`/stores/${store.id}/category-default`)
      await onUpdated()
      onClose()
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to clear subcategory.'
      )
    } finally {
      setSaving(false)
    }
  }

  const errorMessage = normalizeError(error)

  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              Default subcategory — {store?.name}
            </h5>
            <button className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            {errorMessage && (
              <div className="alert alert-danger mb-3">{errorMessage}</div>
            )}

            <div className="mb-3">
              <div className="text-secondary small">Current default</div>
              <div className="mt-1">
                {store?.category_default?.subcategory?.name ? (
                  <span className="badge bg-blue-lt text-blue">
                    {store.category_default.subcategory.name}
                  </span>
                ) : (
                  <span className="text-secondary">None</span>
                )}
              </div>
            </div>

            <div className="mb-4">
              <label className="form-label fw-medium">Assign subcategory</label>
              <div className="d-flex gap-2">
                <select
                  className="form-select"
                  value={selectedId}
                  onChange={(e) => setSelectedId(e.target.value)}
                  disabled={saving}
                >
                  <option value="">Select a subcategory</option>
                  {items.map((sub) => (
                    <option key={sub.id} value={sub.id}>
                      {sub.category_name
                        ? `${sub.category_name} / ${sub.name}`
                        : sub.name}
                    </option>
                  ))}
                </select>

                <button
                  className="btn btn-primary px-3"
                  onClick={handleAssign}
                  disabled={!selectedId || saving}
                >
                  {saving ? '...' : 'Assign'}
                </button>
              </div>
            </div>

            <div className="mt-2">
              <button
                className="btn btn-outline-danger"
                onClick={handleClear}
                disabled={saving || !store?.category_default}
              >
                Clear default
              </button>
            </div>
          </div>

          <div className="modal-footer">
            <button className="btn btn-outline-secondary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}