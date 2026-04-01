import { useState } from 'react'
import { IconX } from '@tabler/icons-react'
import client from '../../api/client'

export default function OwnersModal({ account, currentUser, allUsers, onClose, onUpdate }) {
  const [owners, setOwners]       = useState(account.owners ?? [])
  const [selectedUser, setSelectedUser] = useState('')
  const [assigning, setAssigning] = useState(false)
  const [error, setError]         = useState('')

  const isIndividual = account.type === 'individual'
  const availableUsers = allUsers.filter(u => !owners.find(o => o.id === u.id))

  async function handleAssign() {
    if (!selectedUser) return
    setAssigning(true)
    setError('')
    try {
      await client.post(`/accounts/${account.id}/owners/${selectedUser}`)
      const user = allUsers.find(u => u.id === selectedUser)
      const updated = [...owners, user]
      setOwners(updated)
      setSelectedUser('')
      onUpdate(account.id, updated)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to assign user.')
    } finally {
      setAssigning(false)
    }
  }

  async function handleRemove(userId) {
    if (owners.length <= 1) return  // account always with at least one owner
    setError('')
    try {
      await client.delete(`/accounts/${account.id}/owners/${userId}`)
      const updated = owners.filter(o => o.id !== userId)
      setOwners(updated)
      onUpdate(account.id, updated, userId === currentUser.id)
      // Si se elimina a sí mismo, cerrar modal (el padre lo quita de la lista)
      if (userId === currentUser.id) onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to remove user.')
    }
  }

  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">

          <div className="modal-header">
            <h5 className="modal-title">Owners — {account.name}</h5>
            <button className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger mb-3">{error}</div>}

            {isIndividual ? (
              <div className="text-secondary">
                Individual accounts can only have one owner.
              </div>
            ) : (
              <>
                <div className="mb-4">
                  <label className="form-label fw-medium">Assign user</label>
                  <div className="d-flex gap-2">
                    <select className="form-select" value={selectedUser}
                      onChange={e => setSelectedUser(e.target.value)}>
                      <option value="">Select a user...</option>
                      {availableUsers.map(u => (
                        <option key={u.id} value={u.id}>{u.name}</option>
                      ))}
                    </select>
                    <button className="btn btn-primary px-3"
                      onClick={handleAssign}
                      disabled={!selectedUser || assigning}>
                      {assigning ? '...' : 'Assign'}
                    </button>
                  </div>
                </div>
              </>
            )}

            {/* Lista de owners */}
            <div className="mt-2">
              {owners.map(owner => {
                const isMe   = owner.id === currentUser?.id
                const isLast = owners.length <= 1
                return (
                  <div key={owner.id}
                    className="d-flex align-items-center justify-content-between py-2 border-bottom">
                    <span>
                      {owner.name}
                      {isMe && <span className="badge bg-blue-lt text-blue ms-2">you</span>}
                    </span>
                    {!isIndividual && (
                      <button
                        className="btn btn-sm btn-danger"
                        onClick={() => handleRemove(owner.id)}
                        disabled={isLast}
                        title={isLast ? 'Account must have at least one owner' : isMe ? 'Remove yourself' : 'Remove'}>
                        Remove
                      </button>
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          <div className="modal-footer">
            <button className="btn btn-outline-secondary" onClick={onClose}>Close</button>
          </div>

        </div>
      </div>
    </div>
  )
}