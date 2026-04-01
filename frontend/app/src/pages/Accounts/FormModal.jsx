export default function Form({ form, mode, saving, error, onChange, onSave, onCancel }) {
  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">

          <div className="modal-header">
            <h5 className="modal-title">
              {mode === 'edit' ? 'Edit account' : 'New account'}
            </h5>
            <button className="btn-close" onClick={onCancel} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger mb-3">{error}</div>}
            <form id="account-form" onSubmit={onSave}>
              <div className="mb-3">
                <label className="form-label">Name</label>
                <input
                  type="text" className="form-control" placeholder="Account name"
                  value={form.name} onChange={onChange('name')} required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Type</label>
                <select className="form-select" value={form.type}
                  onChange={onChange('type')} required>
                  <option value="individual">Individual</option>
                  <option value="shared">Shared</option>
                </select>
              </div>
            </form>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" form="account-form" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>

        </div>
      </div>
    </div>
  )
}