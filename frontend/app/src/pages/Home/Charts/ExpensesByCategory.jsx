import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts'

const COLORS = ['#206bc4', '#4299e1', '#74c0fc', '#a5d8ff', '#1c7ed6', '#339af0']

const fmt = (n) => new Intl.NumberFormat('es-CO', {
  style: 'currency', currency: 'COP', maximumFractionDigits: 0
}).format(n)

export default function ExpensesByCategoryChart({ data, loading }) {
  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Expenses by Category</h3>
      </div>
      <div className="card-body">
        {loading ? (
          <div className="text-center py-5 text-secondary">Loading chart...</div>
        ) : data.length === 0 ? (
          <div className="text-center py-5 text-secondary">No expense data yet</div>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 60 }}>
              <XAxis
                dataKey="name"
                angle={-35}
                textAnchor="end"
                tick={{ fontSize: 12 }}
              />
              <YAxis
                tickFormatter={(v) => new Intl.NumberFormat('es-CO', {
                  notation: 'compact', maximumFractionDigits: 1
                }).format(v)}
                tick={{ fontSize: 12 }}
              />
              <Tooltip formatter={(v) => [fmt(v), 'Expenses']} />
              <Bar
                dataKey="value"
                radius={[4, 4, 0, 0]}
                shape={(props) => {
                  const { x, y, width, height, index } = props
                  return (
                    <rect
                      x={x} y={y}
                      width={width} height={height}
                      fill={COLORS[index % COLORS.length]}
                      rx={4} ry={4}
                    />
                  )
                }}
              />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}