export default function Alert({ message, type = 'danger' }) {
  if (!message) return null
  return <div className={`alert alert-${type} mb-3`}>{message}</div>
}