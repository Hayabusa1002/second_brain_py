export default function Form({ form, accounts, categories, mode, saving, error, onChange, onSave, onCancel }) {
  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">

          <div className="modal-header">
            <h5 className="modal-title">
              {mode === 'edit' ? 'Edit transaction' : 'Add transaction'}
            </h5>
            <button className="btn-close" onClick={onCancel} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger mb-3">{error}</div>}
            <form id="transaction-form" onSubmit={onSave}>
              <div className="row g-3">
                <div className="col-12 col-md-6">
                  <label className="form-label">Account</label>
                  <select className="form-select" value={form.account_id}
                    onChange={onChange('account_id')} required>
                    <option value="">Select account...</option>
                    {accounts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                  </select>
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label">Amount</label>
                  <input type="number" step="0.01" min="0" className="form-control"
                    placeholder="0.00" value={form.amount}
                    onChange={onChange('amount')} required />
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label">Type</label>
                  <select className="form-select" value={form.type}
                    onChange={onChange('type')} required>
                    <option value="expense">Expense</option>
                    <option value="income">Income</option>
                  </select>
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label">Category</label>
                  <select className="form-select" value={form.category_id}
                    onChange={onChange('category_id')} required>
                    <option value="">Select category...</option>
                    {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                  </select>
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label">Date</label>
                  <input type="date" className="form-control"
                    value={form.date} onChange={onChange('date')} required />
                </div>
                <div className="col-12 col-md-6">
                  <label className="form-label">Description</label>
                  <input type="text" className="form-control" placeholder="Optional"
                    value={form.description} onChange={onChange('description')} />
                </div>
              </div>
            </form>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" form="transaction-form" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>

        </div>
      </div>
    </div>
  )
}