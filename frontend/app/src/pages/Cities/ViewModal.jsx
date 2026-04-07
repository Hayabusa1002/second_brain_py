import Modal from '../../components/ui/Modal'

export default function ViewModal({ city, onClose }) {
  if (!city) return null

  return (
    <Modal title="City details" onClose={onClose}>
      <div className="row g-3">
        <div className="col-12">
          <div className="text-secondary small">Name</div>
          <div className="fw-medium">{city.name || '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">State</div>
          <div>{city.state || '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">Country</div>
          <div>{city.country || '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">ID</div>
          <div>{city.id ?? '—'}</div>
        </div>

        <div className="col-12">
          <div className="text-secondary small">Created at</div>
          <div>{city.created_at || '—'}</div>
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