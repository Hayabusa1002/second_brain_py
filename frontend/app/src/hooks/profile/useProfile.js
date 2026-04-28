import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import client from '../../api/client'
import parseErrors from '../../utils/forms/parseErrors'
import validateForm from '../../utils/profile/profile/validateForm'

const EMPTY_PROFILE = {
  id: '',
  name: '',
  email: '',
  role: '',
  status: '',
  created_at: '',
  last_login: '',
}

function mapProfile(user) {
  return {
    id: user.id ?? '',
    name: user.name ?? '',
    email: user.email ?? '',
    role: user.role ?? '',
    status: user.status ?? '',
    created_at: user.created_at ?? '',
    last_login: user.last_login ?? user.last_seen ?? '',
  }
}

export default function useProfile() {
  const { user: currentUser, setUser } = useAuth?.() ?? { user: null, setUser: () => {} }

  const [profile, setProfile] = useState(EMPTY_PROFILE)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [success, setSuccess] = useState('')
  const [isEditing, setIsEditing] = useState(false)

  useEffect(() => {
    fetchProfile()
  }, [])

  async function fetchProfile() {
    setLoading(true)
    setError('')

    try {
      const { data } = await client.get('/auth/me')
      const user = data.user ?? data
      setProfile(mapProfile(user))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load profile.')
    } finally {
      setLoading(false)
    }
  }

  const setField = (field) => (e) => {
    const value = e.target.value

    setProfile((prev) => ({ ...prev, [field]: value }))

    if (fieldErrors[field]) {
      setFieldErrors((prev) => ({ ...prev, [field]: '' }))
    }

    if (formError) setFormError('')
    if (success) setSuccess('')
  }

  async function handleSave(e) {
    e.preventDefault()
    setSaving(true)
    setFormError('')
    setFieldErrors({})
    setSuccess('')

    const localErrors = validateForm(profile)

    if (Object.keys(localErrors).length > 0) {
      setFieldErrors(localErrors)
      setFormError('Please review the highlighted fields.')
      setSaving(false)
      return
    }

    try {
      const userId = currentUser?.id ?? profile.id

      const payload = {
        name: profile.name.trim(),
        email: profile.email.trim(),
      }

      const { data } = await client.put(`/users/${userId}`, payload)
      const updatedUser = data.user ?? data

      if (setUser) {
        setUser((prev) => ({
          ...prev,
          ...updatedUser,
          name: updatedUser.name ?? payload.name,
          email: updatedUser.email ?? payload.email,
        }))
      }

      setProfile((prev) => ({
        ...prev,
        name: updatedUser.name ?? payload.name,
        email: updatedUser.email ?? payload.email,
      }))

      setSuccess('Profile updated successfully.')
      setIsEditing(false)
      fetchProfile()
    } catch (err) {
      const parsed = parseErrors(err, 'Failed to update profile.')
      setFormError(parsed.error)
      setFieldErrors(parsed.fieldErrors)
    } finally {
      setSaving(false)
    }
  }

  function handleCancel() {
    setIsEditing(false)
    setFormError('')
    setFieldErrors({})
    setSuccess('')
    fetchProfile()
  }

  return {
    profile,
    loading,
    error,
    saving,
    formError,
    fieldErrors,
    success,
    isEditing,
    setIsEditing,
    setField,
    handleSave,
    handleCancel,
  }
}