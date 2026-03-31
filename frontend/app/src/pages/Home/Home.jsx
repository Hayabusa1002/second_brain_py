import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'

export default function Home() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [summary, setSummary] = useState({ income: 0, expenses: 0, balance: 0 })
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const { data } = await client.get('/transactions?limit=5&order=desc')
        const txList = data.items ?? data

        const income   = txList.filter(t => t.type === 'income') .reduce((a, t) => a + t.amount, 0)
        const expenses = txList.filter(t => t.type === 'expense').reduce((a, t) => a + t.amount, 0)

        setTransactions(txList)
        setSummary({ income, expenses, balance: income - expenses })
      } catch (err) {
        console.error('Error cargando home:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="container-xl d-flex justify-content-center py-5">
        <div className="spinner-border text-primary" role="status" />
      </div>
    )
  }

  return (
    <div className="container-xl">

      {/* Page header */}
      <div className="page-header mb-4">
        <div className="row align-items-center">
          <div className="col">
            <h2 className="page-title">
              Hello, {user?.full_name ?? user?.username}
            </h2>
            <div className="text-secondary mt-1">Transactions summary</div>
          </div>
          <div className="col-auto ms-auto">
            <button
              className="btn btn-primary"
              onClick={() => navigate('/transactions/new')}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                fill="currentColor" className="me-2" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
              </svg>
              New transaction
            </button>
          </div>
        </div>
      </div>

      {/* Summary cards */}
      <div className="row row-deck row-cards mb-4">
        <SummaryCard label="Balance"  amount={summary.balance}  color="blue"  />
        <SummaryCard label="Ingresos" amount={summary.income}   color="green" />
        <SummaryCard label="Gastos"   amount={summary.expenses} color="red"   />
      </div>

      {/* Recent transactions */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Recent transactions</h3>
          <div className="card-options">
            <button
              className="btn btn-link text-secondary"
              onClick={() => navigate('/transactions')}
            >
              Ver todas →
            </button>
          </div>
        </div>

        <div className="card-body p-0">
          {transactions.length === 0 ? (
            <p className="text-center text-secondary py-4 mb-0">
              No transactions yet.
            </p>
          ) : (
            <div className="table-responsive">
              <table className="table table-vcenter card-table">
                <thead>
                  <tr>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Date</th>
                    <th className="text-end">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map(tx => (
                    <TransactionRow key={tx.id} tx={tx} />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Quick actions */}
      <div className="row mt-4">
        <div className="col-auto">
          <button className="btn" onClick={() => navigate('/categories')}>
            Categories
          </button>
        </div>
        <div className="col-auto">
          <button className="btn" onClick={() => navigate('/reports')}>
            Reports
          </button>
        </div>
      </div>

    </div>
  )
}

// ─── Sub-componentes ─────────────────────────────────────────────────────────

const colorClass = {
  blue:  'bg-blue-lt  text-blue',
  green: 'bg-green-lt text-green',
  red:   'bg-red-lt   text-red',
}

function SummaryCard({ label, amount, color }) {
  return (
    <div className="col-sm-6 col-lg-4">
      <div className="card">
        <div className="card-body">
          <div className="d-flex align-items-center mb-3">
            <span className={`badge ${colorClass[color]} me-2`}>{label}</span>
          </div>
          <div className="h1 mb-0">
            ${amount.toLocaleString('es-CO', { minimumFractionDigits: 0 })}
          </div>
        </div>
      </div>
    </div>
  )
}

function TransactionRow({ tx }) {
  const isIncome = tx.type === 'income'
  return (
    <tr>
      <td>{tx.description ?? '—'}</td>
      <td className="text-secondary">{tx.category?.name ?? '—'}</td>
      <td className="text-secondary">
        {new Date(tx.date).toLocaleDateString('es-CO')}
      </td>
      <td className={`text-end fw-semibold ${isIncome ? 'text-green' : 'text-red'}`}>
        {isIncome ? '+' : '-'}${tx.amount.toLocaleString('es-CO')}
      </td>
    </tr>
  )
}