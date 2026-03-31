import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts'
import { useAuth } from '../../context/AuthContext'
import {
  IconReceipt, IconUser,
  IconArrowUpRight, IconArrowDownRight, IconWallet
} from '@tabler/icons-react'
import client from '../../api/client'

const COLORS = ['#206bc4', '#4299e1', '#74c0fc', '#a5d8ff', '#1c7ed6', '#339af0']

export default function Home() {
  const { user } = useAuth()
  const [summary, setSummary]     = useState({ balance: 0, income: 0, expenses: 0 })
  const [chartData, setChartData] = useState([])
  const [loading, setLoading]     = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const { data } = await client.get('/transactions', { params: { limit: 500 } })
        const txs = data.items ?? data

        const income   = txs.filter(t => t.type === 'income').reduce((s, t) => s + t.amount, 0)
        const expenses = txs.filter(t => t.type === 'expense').reduce((s, t) => s + t.amount, 0)
        setSummary({ balance: income - expenses, income, expenses })

        const byCategory = {}
        txs.filter(t => t.type === 'expense').forEach(t => {
          const cat = t.category ?? 'Other'
          byCategory[cat] = (byCategory[cat] ?? 0) + t.amount
        })
        setChartData(
          Object.entries(byCategory)
            .map(([name, value]) => ({ name, value }))
            .sort((a, b) => b.value - a.value)
        )
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  const fmt = (n) => new Intl.NumberFormat('es-CO', {
    style: 'currency', currency: 'COP', maximumFractionDigits: 0
  }).format(n)

  return (
    <div className="container-xl py-4">

      {/* Header */}
      <div className="mb-4">
        <h2 className="mb-0">Welcome back, {user?.name?.split(' ')[0]}</h2>
        <p className="text-secondary mb-0">Here's your financial overview</p>
      </div>

      {/* Summary cards */}
      <div className="row g-3 mb-4">
        {[
          {
            label: 'Balance',
            value: summary.balance,
            icon: <IconWallet size={20} stroke={1.5} />,
            color: 'blue',
            sub: 'Net total'
          },
          {
            label: 'Income',
            value: summary.income,
            icon: <IconArrowUpRight size={20} stroke={1.5} />,
            color: 'green',
            sub: 'Total received'
          },
          {
            label: 'Expenses',
            value: summary.expenses,
            icon: <IconArrowDownRight size={20} stroke={1.5} />,
            color: 'red',
            sub: 'Total spent'
          },
        ].map(({ label, value, icon, color, sub }) => (
          <div key={label} className="col-12 col-sm-4">
            <div className="card">
              <div className="card-body">
                <div className="d-flex align-items-center mb-2">
                  <span className={`avatar avatar-sm bg-${color}-lt text-${color} me-2`}>
                    {icon}
                  </span>
                  <span className="text-secondary">{label}</span>
                </div>
                <div className="h2 mb-0">
                  {loading ? <span className="placeholder col-6" /> : fmt(value)}
                </div>
                <div className="small text-secondary mt-1">{sub}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="card mb-4">
        <div className="card-header">
          <h3 className="card-title">Quick Actions</h3>
        </div>
        <div className="card-body">
          <div className="d-flex gap-2 flex-wrap">
            <Link to="/transactions" className="btn btn-outline-secondary d-flex align-items-center gap-1">
              <IconReceipt size={16} stroke={1.5} /> View Transactions
            </Link>
            <Link to="/profile" className="btn btn-outline-secondary d-flex align-items-center gap-1">
              <IconUser size={16} stroke={1.5} /> Profile
            </Link>
          </div>
        </div>
      </div>

      {/* Bar chart */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Expenses by Category</h3>
        </div>
        <div className="card-body">
          {loading ? (
            <div className="text-center py-5 text-secondary">Loading chart...</div>
          ) : chartData.length === 0 ? (
            <div className="text-center py-5 text-secondary">No expense data yet</div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 60 }}>
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

    </div>
  )
}