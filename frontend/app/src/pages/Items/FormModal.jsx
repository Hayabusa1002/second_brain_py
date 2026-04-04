import Modal from '../../components/ui/Modal'

export default function FormModal({
  form,
  categories,
  cities,
  mode,
  saving,
  error,
  onChange,
  onSave,
  onCancel,
}) {
  return (
    <Modal
      title={mode === 'add' ? 'New item' : 'Edit item'}
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
          <label className="form-label">Category</label>
          <select
            className="form-select"
            value={form.category_id ?? ''}
            onChange={onChange('category_id')}
          >
            <option value="">Select category</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">City</label>
          <select
            className="form-select"
            value={form.city_id ?? ''}
            onChange={onChange('city_id')}
          >
            <option value="">Select city</option>
            {cities.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Price</label>
          <input
            type="number"
            className="form-control"
            value={form.price}
            onChange={onChange('price')}
            min="0"
            step="0.01"
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