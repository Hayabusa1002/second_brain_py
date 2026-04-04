import { useState } from 'react'
import client from '../../api/client'

export default function SubcategoryModal({
  category,
  subcategories,
  onClose,
  onUpdate,
}) {
  const [items, setItems] = useState(subcategories ?? [])
  const [name, setName] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  async function handleAdd() {
    if (!name.trim()) return

    setSaving(true)
    setError('')

    try {
      const payload = {
        name: name.trim(),
        category_id: category.id,
      }

      const { data } = await client.post('/subcategories', payload)
      const created = data.subcategory ?? data.item ?? data
      const updated = [...items, created]

      setItems(updated)
      setName('')
      onUpdate(category.id, updated)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create subcategory.')
    } finally {
      setSaving(false)
    }
  }

  async function handleRemove(subcategoryId) {
    setError('')

    try {
      await client.delete(`/subcategories/${subcategoryId}`)
      const updated = items.filter((item) => item.id !== subcategoryId)
      setItems(updated)
      onUpdate(category.id, updated)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to remove subcategory.')
    }
  }

  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Subcategories — {category.name}</h5>
            <button className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger mb-3">{error}</div>}

            <div className="mb-4">
              <label className="form-label fw-medium">Add subcategory</label>
              <div className="d-flex gap-2">
                <input
                  className="form-control"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Subcategory name..."
                />
                <button
                  className="btn btn-primary px-3"
                  onClick={handleAdd}
                  disabled={!name.trim() || saving}
                >
                  {saving ? '...' : 'Add'}
                </button>
              </div>
            </div>

            <div className="mt-2">
              {items.length === 0 ? (
                <div className="text-secondary">No subcategories yet.</div>
              ) : (
                items.map((item) => (
                  <div
                    key={item.id}
                    className="d-flex align-items-center justify-content-between py-2 border-bottom"
                  >
                    <span>{item.name}</span>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleRemove(item.id)}
                    >
                      Remove
                    </button>
                  </div>
                ))
              )}
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