import { IconBan } from '@tabler/icons-react'

export default function BanModal({ user, onConfirm, onCancel }) {
  const isBanned = user?.status === 'banned'
  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
      <div className="modal-dialog modal-sm modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-body text-center py-4">
            <IconBan size={40} stroke={1.5} className={isBanned ? 'text-success mb-3' : 'text-warning mb-3'} />
            <h5>{isBanned ? 'Unban user?' : 'Ban user?'}</h5>
            <p className="text-secondary mb-0">
              <strong>{user?.name}</strong> will be {isBanned ? 'reactivated' : 'banned and lose access'}.
            </p>
          </div>
          <div className="modal-footer justify-content-center gap-2">
            <button className="btn btn-outline-secondary" onClick={onCancel}>Cancel</button>
            <button className={`btn ${isBanned ? 'btn-success' : 'btn-warning'}`} onClick={onConfirm}>
              {isBanned ? 'Unban' : 'Ban'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}