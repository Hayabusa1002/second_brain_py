import { useEffect, useState } from 'react'
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
  const [deletingAll, setDeletingAll] = useState(false)
  const [error, setError] = useState('')

  const [renamingId, setRenamingId] = useState(null)
  const [renameValue, setRenameValue] = useState('')
  const [renaming, setRenaming] = useState(false)

  useEffect(() => {
    setItems(subcategories ?? [])
  }, [subcategories, category?.id])

  async function refreshSubcategories() {
    const { data } = await client.get(
      `/categories/${category.id}/subcategories/`
    )
    const updated = data.subcategories ?? data.items ?? data ?? []
    const normalized = Array.isArray(updated) ? updated : []

    setItems(normalized)
    onUpdate(category.id, normalized)
    return normalized
  }

  async function handleAdd() {
    if (!name.trim()) return

    setSaving(true)
    setError('')

    try {
      await client.post(`/categories/${category.id}/subcategories/`, {
        name: name.trim(),
      })

      await refreshSubcategories()
      setName('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create subcategory.')
    } finally {
      setSaving(false)
    }
  }

  async function handleRemove(subcategoryId) {
    setError('')

    try {
      await client.delete(
        `/categories/${category.id}/subcategories/${subcategoryId}`
      )

      await refreshSubcategories()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to remove subcategory.')
    }
  }

  async function handleRemoveAll() {
    if (!items.length) return

    if (
      !window.confirm(
        'This will delete all subcategories in this category. Are you sure?'
      )
    ) return

    setDeletingAll(true)
    setError('')

    try {
      await Promise.all(
        items.map((item) =>
          client.delete(`/categories/${category.id}/subcategories/${item.id}`)
        )
      )

      await refreshSubcategories()
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Failed to remove all subcategories.'
      )
    } finally {
      setDeletingAll(false)
    }
  }

  function startRename(item) {
    setRenamingId(item.id)
    setRenameValue(item.name)
    setError('')
  }

  function cancelRename() {
    setRenamingId(null)
    setRenameValue('')
  }

  async function handleRename(subcategoryId) {
    if (!renameValue.trim()) return
    setRenaming(true)
    setError('')
    try {
      await client.patch(
        `/categories/${category.id}/subcategories/${subcategoryId}`,
        { name: renameValue.trim() }
      )
      await refreshSubcategories()
      cancelRename()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to rename subcategory.')
    } finally {
      setRenaming(false)
    }
  }

  const isBusy = saving || deletingAll || renaming

  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              Subcategories — {category.name}
            </h5>
            <button className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            {error && (
              <div className="alert alert-danger mb-3">{error}</div>
            )}

            {/* Add subcategory */}
            <div className="mb-4">
              <label className="form-label fw-medium">Add subcategory</label>
              <div className="d-flex gap-2">
                <input
                  className="form-control"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Subcategory name..."
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && name.trim() && !saving) handleAdd()
                  }}
                  disabled={isBusy}
                />
                <button
                  className="btn btn-primary px-3"
                  onClick={handleAdd}
                  disabled={!name.trim() || isBusy}
                >
                  {saving ? '...' : 'Add'}
                </button>
              </div>
            </div>

            {/* List */}
            <div className="mt-2">
              {items.length === 0 ? (
                <div className="text-secondary">No subcategories yet.</div>
              ) : (
                <>
                  {items.map((item) => (
                    <div
                      key={item.id}
                      className="py-2 border-bottom"
                    >
                      {renamingId === item.id ? (
                        /* ── Rename row ── */
                        <div className="d-flex gap-2 align-items-center">
                          <input
                            className="form-control form-control-sm"
                            value={renameValue}
                            autoFocus
                            onChange={(e) => setRenameValue(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter' && renameValue.trim() && !renaming)
                                handleRename(item.id)
                              if (e.key === 'Escape') cancelRename()
                            }}
                            disabled={renaming}
                          />
                          <button
                            className="btn btn-sm btn-success"
                            onClick={() => handleRename(item.id)}
                            disabled={!renameValue.trim() || renaming}
                          >
                            {renaming ? '...' : 'Save'}
                          </button>
                          <button
                            className="btn btn-sm btn-outline-secondary"
                            onClick={cancelRename}
                            disabled={renaming}
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        /* ── Normal row ── */
                        <div className="d-flex align-items-center justify-content-between">
                          <span>{item.name}</span>
                          <div className="d-flex gap-2">
                            <button
                              className="btn btn-sm btn-outline-secondary"
                              onClick={() => startRename(item)}
                              disabled={isBusy}
                            >
                              Rename
                            </button>
                            <button
                              className="btn btn-sm btn-danger"
                              onClick={() => handleRemove(item.id)}
                              disabled={isBusy}
                            >
                              Remove
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}

                  <div className="mt-3 d-flex justify-content-end">
                    <button
                      type="button"
                      className="btn btn-outline-danger"
                      onClick={handleRemoveAll}
                      disabled={isBusy || !items.length}
                    >
                      {deletingAll ? 'Removing...' : 'Remove all'}
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="modal-footer">
            <button
              className="btn btn-outline-secondary"
              onClick={onClose}
              disabled={isBusy}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}