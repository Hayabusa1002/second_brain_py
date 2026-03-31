import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Cell, ReferenceLine
} from 'recharts'

const fmt = (n) => new Intl.NumberFormat('es-CO', {
  style: 'currency', currency: 'COP', maximumFractionDigits: 0
}).format(n)

const fmtCompact = (v) => new Intl.NumberFormat('es-CO', {
  notation: 'compact', maximumFractionDigits: 1
}).format(v)

function buildWaterfall(txs, catMap) {
  // Group by Category and sum income and expenses
  const map = {}
  txs.forEach(t => {
    const cat = catMap[t.category_id] ?? 'Other'
    if (!map[cat]) map[cat] = { income: 0, expense: 0 }
    if (t.type === 'income') map[cat].income += parseFloat(t.amount)
    else                     map[cat].expense += parseFloat(t.amount)
  })

  // Net by category, sorted by abs value desc
  const sorted = Object.entries(map)
    .map(([name, { income, expense }]) => ({
      name,
      net: income - expense,
      type: income >= expense ? 'income' : 'expense'
    }))
    .sort((a, b) => Math.abs(b.net) - Math.abs(a.net))

  // Build waterfall: invisible base + visible value
  let running = 0
  const items = sorted.map(({ name, net, type }) => {
    const base  = net >= 0 ? running : running + net
    const value = Math.abs(net)
    running += net
    return { name, base, value, net, type, running, isTotal: false }
  })

  // Net balance bar — starts in 0, end with the acumulated value
  items.push({
    name:    'Net Balance',
    base:    running >= 0 ? 0 : running,
    value:   Math.abs(running),
    net:     running,
    type:    running >= 0 ? 'income' : 'expense',
    running,
    isTotal: true,
  })

  return items
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  const d = payload[0]?.payload
  if (!d) return null
  return (
    <div className="card p-2 shadow" style={{ minWidth: 160 }}>
      <div className="fw-medium mb-1">{label}</div>
      <div className={d.type === 'income' ? 'text-green' : 'text-red'}>
        {d.type === 'income' ? '+' : '−'}{fmt(Math.abs(d.net))}
      </div>
      <div className="text-secondary small">Running: {fmt(d.running)}</div>
    </div>
  )
}

export default function ExpensesByCategoryChart({ txs, catMap, loading }) {
  const data = buildWaterfall(txs, catMap)

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Balance by Category</h3>
      </div>
      <div className="card-body">
        {loading ? (
          <div className="text-center py-5 text-secondary">Loading chart...</div>
        ) : data.length === 0 ? (
          <div className="text-center py-5 text-secondary">No data yet</div>
        ) : (
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={data} margin={{ top: 10, right: 20, left: 10, bottom: 60 }}>
              <XAxis
                dataKey="name"
                angle={-35}
                textAnchor="end"
                tick={{ fontSize: 12 }}
              />
              <YAxis
                tickFormatter={fmtCompact}
                tick={{ fontSize: 12 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0} stroke="#444" strokeDasharray="3 3" />

              {/* Offset invisible bar */}
              <Bar dataKey="base" stackId="waterfall" fill="transparent" />

              {/* Colored visible bar */}
              <Bar dataKey="value" stackId="waterfall" radius={[4, 4, 0, 0]}>
                {data.map((entry, i) => (
                  <Cell
                    key={i}
                    fill={entry.type === 'income' ? '#2fb344' : '#d63939'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}