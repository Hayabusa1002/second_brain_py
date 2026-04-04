import Modal from '../../components/ui/Modal'

export default function DeleteModal({ category, onConfirm, onCancel }) {
  return (
    <Modal title="Delete category" onClose={onCancel}>
      <p className="text-secondary mb-3">
        Are you sure you want to delete <strong>{category?.name ?? 'this category'}</strong>?
      </p>

      <div className="d-flex justify-content-end gap-2">
        <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>
          Cancel
        </button>
        <button type="button" className="btn btn-danger" onClick={onConfirm}>
          Delete
        </button>
      </div>
    </Modal>
  )
}