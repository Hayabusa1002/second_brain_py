import { useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import validateForm from '../../utils/auth/login/validateForm'
import parseErrors from '../../utils/forms/parseErrors'

export default function useLoginForm() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [form, setForm] = useState({ email: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const handleChange = (field) => (e) => {
    const value = e.target.value

    setForm((prev) => ({ ...prev, [field]: value }))

    if (fieldErrors[field]) {
      setFieldErrors((prev) => ({ ...prev, [field]: '' }))
    }

    if (error) {
      setError('')
    }
  }

  const togglePassword = () => {
    setShowPassword((prev) => !prev)
  }

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const oauthError = params.get('error') || params.get('detail')

    if (oauthError) {
      setError(oauthError)
      navigate('/login', { replace: true })
    }
  }, [location.search, navigate])

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setFieldErrors({})

    const localErrors = validateForm(form)

    if (Object.keys(localErrors).length > 0) {
      setFieldErrors(localErrors)
      setError('Please review the highlighted fields.')
      return
    }

    setLoading(true)

    try {
      const { data } = await client.post('/auth/login', {
        email: form.email.trim(),
        password: form.password,
      })

      login(data.user)
      navigate('/')
    } catch (err) {
      const parsed = parseErrors(err)
      setError(parsed.error)
      setFieldErrors(parsed.fieldErrors)
    } finally {
      setLoading(false)
    }
  }

  return {
    form,
    showPassword,
    error,
    fieldErrors,
    loading,
    handleChange,
    handleSubmit,
    togglePassword,
  }
}