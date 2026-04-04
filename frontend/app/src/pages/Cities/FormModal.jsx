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
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Type</label>
          <select
            className="form-select"
            value={form.type}
            onChange={onChange('type')}
          >
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Parent city (optional)</label>
          <input
            className="form-control"
            value={form.parent_id ?? ''}
            onChange={onChange('parent_id')}
            placeholder="Parent city id"
          />
        </div>

        {error && <div className="text-danger mb-2">{error}</div>}

        <div className="d-flex justify-content-end gap-2 mt-3">
          <button
            type="button"
            className="btn btn-link"
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