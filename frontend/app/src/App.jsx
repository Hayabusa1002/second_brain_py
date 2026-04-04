import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/auth/ProtectedRoute'

import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import AccessRequests from './pages/Auth/AccessRequests'
import Home from './pages/Home/Home'
import Profile from './pages/Profile/Profile'
import ChangePassword from './pages/Profile/ChangePassword'
import Transactions from './pages/Transactions/Transactions'
import Accounts from './pages/Accounts/Accounts'
import Users from './pages/Users/Users'
import Categories from './pages/Categories/Categories'
import Cities from './pages/Cities/Cities'
import Items from './pages/Items/Items'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/access-requests" element={<AccessRequests />} />
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/profile/change-password" element={<ProtectedRoute><ChangePassword /></ProtectedRoute>} />
        <Route path="/transactions" element={<ProtectedRoute><Transactions /></ProtectedRoute>} />
        <Route path="/accounts" element={<ProtectedRoute><Accounts /></ProtectedRoute>} />
        <Route path="/users" element={<ProtectedRoute><Users /></ProtectedRoute>} />
        <Route path="/categories" element={<ProtectedRoute><Categories /></ProtectedRoute>} />
        <Route path="/cities" element={<ProtectedRoute><Cities /></ProtectedRoute>} />
        <Route path="/items" element={<ProtectedRoute><Items /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}