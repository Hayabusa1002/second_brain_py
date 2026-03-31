export default function PageCenter({ children }) {
  return (
    <div className="page page-center">
      <div className="container container-tight py-4">
        {children}
      </div>
    </div>
  )
}