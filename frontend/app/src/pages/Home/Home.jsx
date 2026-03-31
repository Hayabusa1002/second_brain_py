import { useState, useEffect } from 'react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import Summary                from './Summary'
import QuickActions           from './QuickActions'
import WaterfallCategory      from './Charts/WaterfallCategory'

export default function Home() {
  const { user } = useAuth()
  const [summary, setSummary] = useState({ balance: 0, income: 0, expenses: 0 })
  const [txs, setTxs]         = useState([])
  const [catMap, setCatMap]   = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [txRes, catRes] = await Promise.all([
          client.get('/transactions', { params: { limit: 500 } }),
          client.get('/categories'),
        ])

        const transactions = txRes.data.items ?? txRes.data
        const cats         = catRes.data.items ?? catRes.data

        // Category map
        const map = {}
        cats.forEach(c => { map[c.id] = c.name })
        setCatMap(map)

        // Summary
        const income   = transactions.filter(t => t.type === 'income').reduce((s, t) => s + parseFloat(t.amount), 0)
        const expenses = transactions.filter(t => t.type === 'expense').reduce((s, t) => s + parseFloat(t.amount), 0)
        setSummary({ balance: income - expenses, income, expenses })

        setTxs(transactions)
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
      <WaterfallCategory txs={txs} catMap={catMap} loading={loading} />

    </div>
  )
}