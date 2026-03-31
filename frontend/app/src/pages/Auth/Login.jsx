import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import PageCenter from '../../components/ui/PageCenter'
import Card from '../../components/ui/Card'
import Input from '../../components/ui/Input'
import Button from '../../components/ui/Button'
import Alert from '../../components/ui/Alert'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const { data } = await client.post('/auth/login', form)
      login(data)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageCenter>
      <div className="text-center mb-4">
        <h2 className="h1">Second Brain</h2>
        <p className="text-secondary">Personal finance management</p>
      </div>
      <Card title="Sign in">
        <form onSubmit={handleSubmit}>
          <Alert message={error} />
          <Input label="Email" type="email" placeholder="your@email.com" value={form.email} onChange={set('email')} required />
          <Input label="Password" type="password" placeholder="Your password" value={form.password} onChange={set('password')} required />
          <div className="form-footer">
            <Button loading={loading}>Sign in</Button>
          </div>
        </form>
      </Card>
      <div className="text-center text-secondary mt-3">
        Don&apos;t have an account? <Link to="/register">Sign up</Link>
      </div>
    </PageCenter>
  )
}