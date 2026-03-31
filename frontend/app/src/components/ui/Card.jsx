export default function Card({ title, children }) {
  return (
    <div className="card card-md">
      <div className="card-body">
        {title && <h2 className="card-title text-center mb-4">{title}</h2>}
        {children}
      </div>
    </div>
  )
}