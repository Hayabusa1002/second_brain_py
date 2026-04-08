import { useEffect, useMemo, useRef, useState } from 'react'
import client from '../../api/client'

export default function SubcategoryModal({
  store,
  onClose,
  onUpdate,
}) {
  const [options, setOptions] = useState([])
  const [selectedIds, setSelectedIds] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [search, setSearch] = useState('')
  const [menuOpen, setMenuOpen] = useState(false)
  const [error, setError] = useState('')
  const dropdownRef = useRef(null)

  useEffect(() => {
    if (!store?.id) return
    fetchData()
  }, [store?.id])

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setMenuOpen(false)
      }
    }

    function handleEscape(event) {
      if (event.key === 'Escape') {
        setMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    document.addEventListener('keydown', handleEscape)

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
      document.removeEventListener('keydown', handleEscape)
    }
  }, [])

  async function fetchData() {
    setLoading(true)
    setError('')

    try {
      const [allRes, assignedRes] = await Promise.all([
        client.get('/subcategories'),
        client.get(`/stores/${store.id}/subcategories`),
      ])

      const allItems =
        allRes.data?.subcategories ??
        allRes.data?.items ??
        allRes.data ??
        []

      const assignedItems =
        assignedRes.data?.subcategories ??
        assignedRes.data?.items ??
        assignedRes.data ??
        []

      const normalizedOptions = Array.isArray(allItems) ? allItems : []
      const normalizedAssigned = Array.isArray(assignedItems) ? assignedItems : []

      setOptions(normalizedOptions)
      setSelectedIds(
        normalizedAssigned.map((item) =>
          String(item.subcategory_id ?? item.subcategory?.id ?? item.id)
        )
      )
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load subcategories.')
    } finally {
      setLoading(false)
    }
  }

  function toggleSubcategory(id) {
    const stringId = String(id)

    setSelectedIds((prev) =>
      prev.includes(stringId)
        ? prev.filter((itemId) => itemId !== stringId)
        : [...prev, stringId]
    )
  }

  function removeSubcategory(id) {
    const stringId = String(id)
    setSelectedIds((prev) => prev.filter((itemId) => itemId !== stringId))
  }

  function clearSelection() {
    setSelectedIds([])
  }

  async function handleSave() {
    if (!store?.id) return

    setSaving(true)
    setError('')

    try {
      await client.put(`/stores/${store.id}/subcategories`, {
        subcategory_ids: selectedIds,
      })

      const selectedItems = options.filter((item) =>
        selectedIds.includes(String(item.id))
      )

      onUpdate?.(store.id, selectedItems)
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save subcategories.')
    } finally {
      setSaving(false)
    }
  }

  const filteredOptions = useMemo(() => {
    const term = search.trim().toLowerCase()
    if (!term) return options

    return options.filter((item) =>
      item.name?.toLowerCase().includes(term)
    )
  }, [options, search])

  const selectedItems = useMemo(() => {
    return options.filter((item) => selectedIds.includes(String(item.id)))
  }, [options, selectedIds])

  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0,0,0,0.45)' }}
      role="dialog"
      aria-modal="true"
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
              disabled={saving}
            />
          </div>

          <div className="modal-body">
            {error && (
              <div className="alert alert-danger mb-3">{error}</div>
            )}

            {loading ? (
              <div className="text-secondary">Loading subcategories...</div>
            ) : (
              <>
                <div className="mb-4">
                  <div className="d-flex align-items-center justify-content-between mb-2">
                    <label className="form-label mb-0">
                      Selected subcategories
                    </label>

                    <button
                      type="button"
                      className="btn btn-sm btn-outline-secondary"
                      onClick={clearSelection}
                      disabled={saving || selectedIds.length === 0}
                    >
                      Clear
                    </button>
                  </div>

                  {selectedItems.length === 0 ? (
                    <div className="text-secondary">
                      No subcategories selected.
                    </div>
                  ) : (
                    <div className="d-flex flex-wrap gap-2">
                      {selectedItems.map((item) => (
                        <span
                          key={item.id}
                          className="badge bg-azure-lt text-azure d-inline-flex align-items-center gap-1 ps-2 pe-1 py-2"
                        >
                          <span>{item.name}</span>
                          <button
                            type="button"
                            className="btn btn-sm btn-ghost-secondary border-0 shadow-none p-0 ms-1"
                            onClick={() => removeSubcategory(item.id)}
                            disabled={saving}
                            style={{
                              minWidth: '18px',
                              minHeight: '18px',
                              lineHeight: 1,
                            }}
                            aria-label={`Remove ${item.name}`}
                          >
                            ×
                          </button>
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="mb-3">
                  <label className="form-label">Search subcategories</label>
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Type to filter..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    disabled={saving}
                  />
                </div>

                <div className="mb-2" ref={dropdownRef}>
                  <label className="form-label">Add subcategories</label>

                  <div className={`dropdown ${menuOpen ? 'show' : ''}`}>
                    <button
                      type="button"
                      className="btn btn-outline-secondary w-100 d-flex align-items-center justify-content-between"
                      onClick={() => setMenuOpen((prev) => !prev)}
                      disabled={saving}
                      aria-expanded={menuOpen}
                    >
                      <span>
                        {selectedIds.length > 0
                          ? `${selectedIds.length} subcategories selected`
                          : 'Select subcategories'}
                      </span>
                      <span className="ms-2">{menuOpen ? '▴' : '▾'}</span>
                    </button>

                    <div
                      className={`dropdown-menu w-100 p-2 ${menuOpen ? 'show' : ''}`}
                      style={{
                        maxHeight: '320px',
                        overflowY: 'auto',
                      }}
                    >
                      {filteredOptions.length === 0 ? (
                        <div className="dropdown-item-text text-secondary">
                          No matching subcategories.
                        </div>
                      ) : (
                        filteredOptions.map((item) => {
                          const checked = selectedIds.includes(String(item.id))

                          return (
                            <label
                              key={item.id}
                              className="dropdown-item d-flex align-items-center gap-2 rounded cursor-pointer mb-1"
                              style={{ cursor: 'pointer' }}
                            >
                              <input
                                type="checkbox"
                                className="form-check-input m-0"
                                checked={checked}
                                onChange={() => toggleSubcategory(item.id)}
                              />
                              <span className="flex-fill">{item.name}</span>
                              {checked && (
                                <span className="badge bg-green-lt text-green">
                                  Added
                                </span>
                              )}
                            </label>
                          )
                        })
                      )}
                    </div>
                  </div>

                  <div className="form-hint mt-2">
                    Click the button to open the selector and choose multiple subcategories.
                  </div>
                </div>
              </>
            )}
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn btn-outline-secondary"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSave}
              disabled={loading || saving}
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}