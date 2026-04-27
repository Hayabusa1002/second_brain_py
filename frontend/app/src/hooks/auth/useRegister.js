import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import client from '../../api/client'
import validateForm from '../../utils/auth/register/validateForm'
import parseErrors from '../../utils/forms/parseErrors'

export default function useRegisterForm() {
  const navigate = useNavigate()

  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
  })
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
      await client.post('/auth/register', {
        name: form.name.trim(),
        email: form.email.trim(),
        password: form.password,
      })

      navigate('/login')
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