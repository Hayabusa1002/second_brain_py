import { IconEdit } from '@tabler/icons-react'

const TYPE_BADGE = {
  income:  'bg-green-lt text-green',
  expense: 'bg-red-lt text-red',
}

const fmt = (n) => new Intl.NumberFormat('es-CO', {
  style: 'currency', currency: 'COP', maximumFractionDigits: 0
}).format(n)

const fmtDate = (d) => d
  ? new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' })
  : '—'

export default function ViewModal({ tx, accountMap, categoryMap, onClose, onEdit }) {
  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Transaction detail</h5>
            <button className="btn-close" onClick={onClose} />
          </div>
          <div className="modal-body">
            <div className="row g-3">
              {[
                { label: 'Date',
                  value: fmtDate(tx.date ?? tx.created_at) },
                { label: 'Amount',
                  value: <span className={tx.type === 'income' ? 'text-green fw-bold' : 'text-red fw-bold'}>
                    {tx.type === 'expense' ? '−' : '+'}{fmt(tx.amount)}
                  </span> },
                { label: 'Type',
                  value: <span className={`badge ${TYPE_BADGE[tx.type] ?? 'bg-secondary-lt'}`}>{tx.type}</span> },
                { label: 'Account',
                  value: <span className="badge bg-blue-lt text-blue">{accountMap[tx.account_id] ?? '—'}</span> },
                { label: 'Category',
                  value: <span className="badge bg-purple-lt text-purple">{categoryMap[tx.category_id] ?? '—'}</span> },
                { label: 'Description',
                  value: tx.description || '—' },
                { label: 'ID',
                  value: <code className="small">{tx.id}</code> },
              ].map(({ label, value }) => (
                <div key={label} className="col-6">
                  <div className="text-secondary small mb-1">{label}</div>
                  <div>{value}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="modal-footer">
            <button className="btn btn-outline-secondary" onClick={onClose}>Close</button>
            <button className="btn btn-primary" onClick={() => { onEdit(tx); onClose() }}>
              <IconEdit size={14} stroke={1.5} className="me-1" /> Edit
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}