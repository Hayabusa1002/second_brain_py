import { IconTrash } from '@tabler/icons-react'

export default function DeleteModal({ store, onConfirm, onCancel }) {
  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}
    >
      <div className="modal-dialog modal-sm modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-body text-center py-4">
            <IconTrash size={40} stroke={1.5} className="text-danger mb-3" />
            <h5>Delete store?</h5>
            <p className="text-secondary mb-0">
              <strong>{store?.name}</strong> will be permanently deleted.
            </p>
          </div>
          <div className="modal-footer justify-content-center gap-2">
            <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="button" className="btn btn-danger" onClick={onConfirm}>
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}