export default function Button({ children, loading, ...props }) {
  return (
    <button className="btn btn-primary w-100" disabled={loading} {...props}>
      {loading ? 'Loading...' : children}
    </button>
  )
}