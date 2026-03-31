export default function Filters({ accounts, categories, filters, onChange, onFilter, onClear }) {
  return (
    <div className="card mb-4">
      <div className="card-header">
        <h3 className="card-title">Filters</h3>
      </div>
      <div className="card-body">
        <div className="row g-3">

          <div className="col-12 col-md-4">
            <label className="form-label">Account</label>
            <select className="form-select" value={filters.account_id}
              onChange={e => onChange('account_id', e.target.value)}>
              <option value="">All accounts</option>
              {accounts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
            </select>
          </div>

          <div className="col-12 col-md-4">
            <label className="form-label">Type</label>
            <select className="form-select" value={filters.type}
              onChange={e => onChange('type', e.target.value)}>
              <option value="">All</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>

          <div className="col-12 col-md-4">
            <label className="form-label">Category</label>
            <select className="form-select" value={filters.category_id}
              onChange={e => onChange('category_id', e.target.value)}>
              <option value="">All</option>
              {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>

          <div className="col-12 col-md-4">
            <label className="form-label">From</label>
            <input type="date" className="form-control" value={filters.date_from}
              onChange={e => onChange('date_from', e.target.value)} />
          </div>

          <div className="col-12 col-md-4">
            <label className="form-label">To</label>
            <input type="date" className="form-control" value={filters.date_to}
              onChange={e => onChange('date_to', e.target.value)} />
          </div>

          <div className="col-12 col-md-4 d-flex align-items-end gap-2">
            <button className="btn btn-primary flex-fill" onClick={onFilter}>Filter</button>
            <button className="btn btn-outline-secondary flex-fill" onClick={onClear}>Clear</button>
          </div>

        </div>
      </div>
    </div>
  )
}