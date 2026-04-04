import Modal from '../../components/ui/Modal'

export default function ViewModal({ category, subcategories, onClose }) {
  return (
    <Modal title="Category detail" onClose={onClose}>
      <div className="row g-3">
        <div className="col-12">
          <div className="form-label mb-1">ID</div>
          <div>{category?.id ?? '—'}</div>
        </div>

        <div className="col-12">
          <div className="form-label mb-1">Name</div>
          <div>{category?.name ?? '—'}</div>
        </div>

        <div className="col-12">
          <div className="form-label mb-1">Type</div>
          <div>{category?.type ?? '—'}</div>
        </div>

        <div className="col-12">
          <div className="form-label mb-1">Subcategories</div>
          {subcategories?.length ? (
            <div className="d-flex flex-wrap gap-1">
              {subcategories.map((sub) => (
                <span key={sub.id} className="badge bg-secondary-lt text-secondary">
                  {sub.name}
                </span>
              ))}
            </div>
          ) : (
            <div>—</div>
          )}
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