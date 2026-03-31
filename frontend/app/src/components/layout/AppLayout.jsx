import Navbar from './Navbar'

export default function AppLayout({ children }) {
  return (
    <div className="wrapper">
      <Navbar />
      <div className="page-wrapper">
        <div className="page-body">
          <div className="container-xl">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}