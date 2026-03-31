export default function Card({ children }) {
  return (
    <div className="card card-md">
      <div className="card-body">
        {children}
      </div>
    </div>
  )
}