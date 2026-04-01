import { Link } from 'react-router-dom'
import { IconReceipt, IconUser } from '@tabler/icons-react'

export default function QuickActions() {
  return (
    <div className="card mb-4">
      <div className="card-header">
        <h3 className="card-title">Quick Actions</h3>
      </div>
      <div className="card-body">
        <div className="d-flex gap-2 flex-wrap">
          <Link to="/transactions" className="btn btn-outline-secondary d-flex align-items-center gap-1">
            <IconReceipt size={16} stroke={1.5} /> View Transactions
          </Link>
          <Link to="/profile" className="btn btn-outline-secondary d-flex align-items-center gap-1">
            <IconUser size={16} stroke={1.5} /> Profile
          </Link>
        </div>
      </div>
    </div>
  )
}