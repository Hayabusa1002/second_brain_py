import Modal from '../../components/ui/Modal'

export default function ViewModal({ store, onClose }) {
  if (!store) return null

  return (
    <Modal title="Store details" onClose={onClose}>
      <div className="row g-3">
        <div className="col-12">
          <div className="text-secondary small">Name</div>
          <div className="fw-medium">{store.name || '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">Type</div>
          <div>{store.type || '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">ID</div>
          <div>{store.id ?? '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">Address</div>
          <div>{store.address || '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">Website</div>
          <div>
            {store.website ? (
              <a href={store.website} target="_blank" rel="noopener noreferrer">
                {store.website}
              </a>
            ) : (
              '—'
            )}
          </div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">Created at</div>
          <div>{store.created_at || '—'}</div>
        </div>
      </div>

      <div className="d-flex justify-content-end mt-4">
        <button type="button" className="btn btn-primary" onClick={onClose}>
          Close
        </button>
      </div>
    </Modal>
  )
}