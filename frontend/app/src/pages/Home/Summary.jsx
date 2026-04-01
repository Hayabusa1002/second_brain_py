import {
  IconArrowUpRight, IconArrowDownRight, IconWallet
} from '@tabler/icons-react'

const fmt = (n) => new Intl.NumberFormat('es-CO', {
  style: 'currency', currency: 'COP', maximumFractionDigits: 0
}).format(n)

const CARDS = [
  { key: 'balance',  label: 'Balance',  icon: <IconWallet size={20} stroke={1.5} />,         color: 'blue',  sub: 'Net total' },
  { key: 'income',   label: 'Income',   icon: <IconArrowUpRight size={20} stroke={1.5} />,   color: 'green', sub: 'Total received' },
  { key: 'expenses', label: 'Expenses', icon: <IconArrowDownRight size={20} stroke={1.5} />, color: 'red',   sub: 'Total spent' },
]

export default function Summary({ summary, loading }) {
  return (
    <div className="row g-3 mb-4">
      {CARDS.map(({ key, label, icon, color, sub }) => (
        <div key={key} className="col-12 col-sm-4">
          <div className="card">
            <div className="card-body">
              <div className="d-flex align-items-center mb-2">
                <span className={`avatar avatar-sm bg-${color}-lt text-${color} me-2`}>
                  {icon}
                </span>
                <span className="text-secondary">{label}</span>
              </div>
              <div className="h2 mb-0">
                {loading ? <span className="placeholder col-6" /> : fmt(summary[key])}
              </div>
              <div className="small text-secondary mt-1">{sub}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}