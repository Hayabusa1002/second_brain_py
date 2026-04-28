import { useState } from 'react'
import client from '../../api/client'
import parseErrors from '../../utils/forms/parseErrors'
import validateForm from '../../utils/profile/changePassword/validateForm'

const initialForm = {
  current_password: '',
  new_password: '',
  confirm_password: '',
}

const initialShow = {
  current: false,
  new: false,
  confirm: false,
}

export default function useChangePassword() {
  const [form, setForm] = useState(initialForm)
  const [show, setShow] = useState(initialShow)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [loading, setLoading] = useState(false)

  const handleChange = (field) => (e) => {
    const value = e.target.value

    setForm((prev) => ({ ...prev, [field]: value }))

    if (fieldErrors[field]) {
      setFieldErrors((prev) => ({ ...prev, [field]: '' }))
    }

    if (error) setError('')
    if (success) setSuccess('')
  }

  const toggleShow = (field) => {
    setShow((prev) => ({ ...prev, [field]: !prev[field] }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')
    setFieldErrors({})

    const localErrors = validateForm(form)

    if (Object.keys(localErrors).length > 0) {
      setFieldErrors(localErrors)
      setError('Please review the highlighted fields.')
      return
    }

    setLoading(true)

    try {
      await client.put('/auth/password', {
        current_password: form.current_password,
        new_password: form.new_password,
      })

      setSuccess('Password updated successfully.')
      setForm(initialForm)
      setShow(initialShow)
    } catch (err) {
      const parsed = parseErrors(err, 'Failed to update password.')
      setError(parsed.error)
      setFieldErrors(parsed.fieldErrors)
    } finally {
      setLoading(false)
    }
  }

  return {
    form,
    show,
    error,
    success,
    fieldErrors,
    loading,
    handleChange,
    toggleShow,
    handleSubmit,
  }
}