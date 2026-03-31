import { useState, useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import Summary                  from './Summary'
import QuickActions             from './QuickActions'
import ExpensesByCategoryChart  from './Charts/ExpensesByCategory'

export default function Home() {
  const { user } = useAuth()
  const [summary, setSummary]         = useState({ balance: 0, income: 0, expenses: 0 })
  const [chartData, setChartData]     = useState([])
  const [loading, setLoading]         = useState(true)
  const [categoryMap, setCategoryMap] = useState({})

  useEffect(() => {
    async function fetchData() {
      try {
        const [txRes, catRes] = await Promise.all([
          client.get('/transactions', { params: { limit: 500 } }),
          client.get('/categories'),
        ])
        const txs  = txRes.data.items ?? txRes.data
        const cats = catRes.data.items ?? catRes.data

        // Construir mapa id → name
        const catMap = {}
        cats.forEach(c => { catMap[c.id] = c.name })
        setCategoryMap(catMap)

        const income   = txs.filter(t => t.type === 'income').reduce((s, t) => s + parseFloat(t.amount), 0)
        const expenses = txs.filter(t => t.type === 'expense').reduce((s, t) => s + parseFloat(t.amount), 0)
        setSummary({ balance: income - expenses, income, expenses })

        const byCategory = {}
        txs.filter(t => t.type === 'expense').forEach(t => {
          const cat = catMap[t.category_id] ?? 'Other'  // ← fix
          byCategory[cat] = (byCategory[cat] ?? 0) + parseFloat(t.amount)
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

  return (
    <div className="container-xl py-4">

      <div className="mb-4">
        <h2 className="mb-0">Welcome back, {user?.name?.split(' ')[0]}</h2>
        <p className="text-secondary mb-0">Here's your financial overview</p>
      </div>

      <Summary summary={summary} loading={loading} />
      <QuickActions />
      <ExpensesByCategoryChart data={chartData} loading={loading} />

    </div>
  )
}