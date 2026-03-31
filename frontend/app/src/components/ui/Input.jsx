export default function Input({ label, ...props }) {
  return (
    <div className="mb-3">
      {label && <label className="form-label">{label}</label>}
      <input className="form-control" {...props} />
    </div>
  )
}