import { IconX } from '@tabler/icons-react'

export default function Form({ form, accounts, categories, mode, saving, error, onChange, onSave, onCancel }) {
  return (
    <div className="card mb-4">
      <div className="card-header d-flex align-items-center justify-content-between">
        <h3 className="card-title mb-0">
          {mode === 'edit' ? 'Edit transaction' : 'Add transaction'}
        </h3>
        <button className="btn btn-ghost-secondary btn-sm" onClick={onCancel}>
          <IconX size={16} stroke={1.5} />
        </button>
      </div>
      <div className="card-body">
        {error && <div className="alert alert-danger mb-3">{error}</div>}
        <form onSubmit={onSave}>
          <div className="row g-3">
            <div className="col-12 col-md-6">
              <label className="form-label">Account</label>
              <select className="form-select" value={form.account_id} onChange={onChange('account_id')} required>
                <option value="">Select account...</option>
                {accounts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
              </select>
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Amount</label>
              <input
                type="number" step="0.01" min="0"
                className="form-control" placeholder="0.00"
                value={form.amount} onChange={onChange('amount')} required
              />
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Type</label>
              <select className="form-select" value={form.type} onChange={onChange('type')} required>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Category</label>
              <select className="form-select" value={form.category_id} onChange={onChange('category_id')} required>
                <option value="">Select category...</option>
                {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Date</label>
              <input
                type="date" className="form-control"
                value={form.date} onChange={onChange('date')} required
              />
            </div>
            <div className="col-12 col-md-6">
              <label className="form-label">Description</label>
              <input
                type="text" className="form-control" placeholder="Optional"
                value={form.description} onChange={onChange('description')}
              />
            </div>
          </div>
          <div className="d-flex gap-2 mt-4">
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save'}
            </button>
            <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}