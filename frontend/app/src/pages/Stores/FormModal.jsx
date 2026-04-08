import Modal from '../../components/ui/Modal'

const STORE_TYPE_OPTIONS = [
  { value: 'physical', label: 'Physical' },
  { value: 'online', label: 'Online' },
  { value: 'subscription', label: 'Subscription' },
  { value: 'service', label: 'Service' },
]

function normalizeError(error) {
  if (!error) return ''

  if (typeof error === 'string') return error

  if (Array.isArray(error)) {
    return error
      .map((item) => {
        if (typeof item === 'string') return item
        if (item?.message) return item.field ? `${item.field}: ${item.message}` : item.message
        if (item?.msg) {
          const field = Array.isArray(item.loc) ? item.loc.filter((part) => part !== 'body').join('.') : ''
          return field ? `${field}: ${item.msg}` : item.msg
        }
        return JSON.stringify(item)
      })
      .join(', ')
  }

  if (typeof error === 'object') {
    if (error.message) return error.message
    if (error.detail) return normalizeError(error.detail)
    return JSON.stringify(error)
  }

  return String(error)
}

export default function FormModal({
  form,
  mode,
  saving,
  error,
  onChange,
  onSave,
  onCancel,
}) {
  const errorMessage = normalizeError(error)

  return (
    <Modal title={mode === 'add' ? 'New store' : 'Edit store'} onClose={onCancel}>
      <form onSubmit={onSave}>
        <div className="mb-3">
          <label className="form-label">Name</label>
          <input
            className="form-control"
            value={form.name}
            onChange={onChange('name')}
            placeholder="Store name"
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Type</label>
          <select
            className="form-select"
            value={form.type}
            onChange={onChange('type')}
            required
          >
            <option value="">Select a type</option>
            {STORE_TYPE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Address</label>
          <input
            className="form-control"
            value={form.address}
            onChange={onChange('address')}
            placeholder="Store address"
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Website</label>
          <input
            type="url"
            className="form-control"
            value={form.website}
            onChange={onChange('website')}
            placeholder="https://example.com"
          />
        </div>

        {errorMessage && <div className="text-danger mb-2">{errorMessage}</div>}

        <div className="d-flex justify-content-end gap-2 mt-3">
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={onCancel}
            disabled={saving}
          >
            Cancel
          </button>

          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </form>
    </Modal>
  )
}