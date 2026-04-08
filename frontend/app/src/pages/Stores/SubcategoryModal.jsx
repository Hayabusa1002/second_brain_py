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

export default function SubcategoryModal({ store, onClose, onUpdated }) {
  const [items, setItems] = useState([])
  const [selectedIds, setSelectedIds] = useState([])
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!store?.id) return
    fetchData()
  }, [store?.id])

  async function fetchData() {
    setLoading(true)
    setError('')

    try {
      const [allRes, selectedRes] = await Promise.all([
        client.get('/subcategories'),
        client.get(`/stores/${store.id}/subcategories`),
      ])

      const allItems = allRes.data?.subcategories ?? allRes.data?.items ?? allRes.data ?? []
      const selectedItems = selectedRes.data?.subcategories ?? selectedRes.data?.items ?? selectedRes.data ?? []

      setItems(Array.isArray(allItems) ? allItems : [])
      setSelectedIds(
        Array.isArray(selectedItems) ? selectedItems.map((item) => item.id) : []
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to load subcategories.'
      )
    } finally {
      setLoading(false)
    }
  }

  function toggleSubcategory(id) {
    setSelectedIds((prev) =>
      prev.includes(id)
        ? prev.filter((itemId) => itemId !== id)
        : [...prev, id]
    )
  }

  async function handleSave() {
    if (!store?.id) return

    setSaving(true)
    setError('')

    try {
      await client.put(`/stores/${store.id}/subcategories`, {
        subcategory_ids: selectedIds,
      })

      if (onUpdated) {
        await onUpdated()
      }

      onClose()
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to save subcategories.'
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
      <div className="modal-dialog modal-dialog-centered modal-lg">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              Store subcategories — {store?.name ?? ''}
            </h5>
            <button
              type="button"
              className="btn-close"
              onClick={onClose}
            />
          </div>

          <div className="modal-body">
            {errorMessage && (
              <div className="alert alert-danger mb-3">{errorMessage}</div>
            )}

            {loading ? (
              <div className="text-secondary">Loading subcategories...</div>
            ) : items.length === 0 ? (
              <div className="text-secondary">No subcategories available.</div>
            ) : (
              <div className="row">
                {items.map((sub) => (
                  <div className="col-md-6 mb-2" key={sub.id}>
                    <label className="form-check">
                      <input
                        type="checkbox"
                        className="form-check-input"
                        checked={selectedIds.includes(sub.id)}
                        onChange={() => toggleSubcategory(sub.id)}
                        disabled={saving}
                      />
                      <span className="form-check-label">{sub.name}</span>
                    </label>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="modal-footer d-flex justify-content-between">
            <div className="text-secondary small">
              Selected: {selectedIds.length}
            </div>

            <div className="d-flex gap-2">
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={onClose}
                disabled={saving}
              >
                Close
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleSave}
                disabled={saving || loading}
              >
                {saving ? 'Saving...' : 'Save'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}