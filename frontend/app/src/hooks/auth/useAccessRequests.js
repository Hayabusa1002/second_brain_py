import { useEffect, useState } from 'react'
import client from '../../api/client'
import parseAuthErrors from '../../utils/auth/accessRequests/parseErrors'

export default function useAccessRequests() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [actionError, setActionError] = useState('')
  const [processingId, setProcessingId] = useState(null)

  useEffect(() => {
    fetchRequests()
  }, [])

  async function fetchRequests() {
    setLoading(true)
    setError('')

    try {
      const { data } = await client.get('/users/pending')
      setRequests(data.users ?? data.items ?? data)
    } catch (err) {
      if (err.response?.status === 403) {
        setError('You do not have permission to view access requests.')
      } else {
        setError(parseAuthErrors(err, 'Failed to load access requests.'))
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleApprove(user) {
    setProcessingId(user.id)
    setActionError('')

    try {
      await client.post(`/users/${user.id}/approve`)
      setRequests((prev) => prev.filter((u) => u.id !== user.id))
    } catch (err) {
      setActionError(parseAuthErrors(err, 'Failed to approve request.'))
    } finally {
      setProcessingId(null)
    }
  }

  async function handleReject(user) {
    setProcessingId(user.id)
    setActionError('')

    try {
      await client.post(`/users/${user.id}/reject`)
      setRequests((prev) => prev.filter((u) => u.id !== user.id))
    } catch (err) {
      setActionError(parseAuthErrors(err, 'Failed to reject request.'))
    } finally {
      setProcessingId(null)
    }
  }

  return {
    requests,
    loading,
    error,
    actionError,
    processingId,
    isForbidden: error === 'You do not have permission to view access requests.',
    handleApprove,
    handleReject,
    refetch: fetchRequests,
  }
}