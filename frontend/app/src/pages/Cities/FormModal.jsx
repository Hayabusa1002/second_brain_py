import Modal from '../../components/ui/Modal'

export default function FormModal({
  form,
  mode,
  saving,
  error,
  onChange,
  onSave,
  onCancel,
}) {
  return (
    <Modal
      title={mode === 'add' ? 'New city' : 'Edit city'}
      onClose={onCancel}
    >
      <form onSubmit={onSave}>
        <div className="mb-3">
          <label className="form-label">Name</label>
          <input
            className="form-control"
            value={form.name}
            onChange={onChange('name')}
            placeholder="City name"
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">State</label>
          <input
            className="form-control"
            value={form.state}
            onChange={onChange('state')}
            placeholder="State or province"
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Country</label>
          <input
            className="form-control"
            value={form.country}
            onChange={onChange('country')}
            placeholder="Country"
            required
          />
        </div>

        {error && <div className="text-danger mb-2">{error}</div>}

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