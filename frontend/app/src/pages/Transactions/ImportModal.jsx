import { useState } from 'react'
import { IconUpload, IconDownload } from '@tabler/icons-react'
import client from '../../api/client'

export default function Import({ onClose, onSuccess }) {
  const [file, setFile]           = useState(null)
  const [importing, setImporting] = useState(false)
  const [error, setError]         = useState('')
  const [success, setSuccess]     = useState('')

  function downloadTemplate() {
    const csv = 'date,amount,type,category_id,account_id,description\n2026-01-01,50000,expense,,,'
    const a = document.createElement('a')
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
    a.download = 'transactions_template.csv'
    a.click()
  }

  async function handleImport(e) {
    e.preventDefault()
    if (!file) return
    setImporting(true)
    setError('')
    setSuccess('')
    try {
      const fd = new FormData()
      fd.append('file', file)
      await client.post('/transactions/import', fd, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setSuccess('Transactions imported successfully.')
      setFile(null)
      onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || 'Import failed.')
    } finally {
      setImporting(false)
    }
  }

  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">

          <div className="modal-header">
            <h5 className="modal-title">Import transactions</h5>
            <button className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            <p className="text-secondary mb-3">
              Upload a <code>.csv</code> or <code>.xlsx</code> file with columns:{' '}
              <strong>date, amount, type, category_id, account_id, description</strong>
            </p>
            <button className="btn btn-outline-primary btn-sm mb-4 d-flex align-items-center gap-1"
              onClick={downloadTemplate}>
              <IconDownload size={14} stroke={1.5} /> Download template CSV
            </button>
            {error   && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <form id="import-form" onSubmit={handleImport}>
              <input type="file" className="form-control" accept=".csv,.xlsx"
                onChange={e => setFile(e.target.files[0])} />
            </form>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-outline-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" form="import-form"
              className="btn btn-primary d-flex align-items-center gap-1"
              disabled={!file || importing}>
              <IconUpload size={16} stroke={1.5} />
              {importing ? 'Importing...' : 'Import'}
            </button>
          </div>

        </div>
      </div>
    </div>
  )
}