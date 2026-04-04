export default function Modal({ title, children, onClose }) {
  return (
    <>
      <div className="modal modal-blur fade show d-block" tabIndex="-1" role="dialog">
        <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h5 className="modal-title">{title}</h5>
              <button
                type="button"
                className="btn-close"
                aria-label="Close"
                onClick={onClose}
              />
            </div>

            <div className="modal-body">
              {children}
            </div>
          </div>
        </div>
      </div>

      <div className="modal-backdrop fade show" />
    </>
  )
}