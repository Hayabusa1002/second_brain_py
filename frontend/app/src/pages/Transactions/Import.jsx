import { useState } from 'react'
import { IconUpload, IconDownload, IconX } from '@tabler/icons-react'
import client from '../../api/client'

export default function Import({ onClose, onSuccess }) {
  const [file, setFile]       = useState(null)
  const [importing, setImporting] = useState(false)
  const [error, setError]     = useState('')
  const [success, setSuccess] = useState('')

  function downloadTemplate() {
    const csv = 'date,amount,type,category_id,account_id,description\n2026-01-01,50000,expense,,,'
    const blob = new Blob([csv], { type: 'text/csv' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
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
    <div className="card mb-4">
      <div className="card-header d-flex align-items-center justify-content-between">
        <h3 className="card-title mb-0">Import transactions</h3>
        <button className="btn btn-ghost-secondary btn-sm" onClick={onClose}>
          <IconX size={16} stroke={1.5} />
        </button>
      </div>
      <div className="card-body">
        <p className="text-secondary mb-3">
          Upload a <code>.csv</code> or <code>.xlsx</code> file with columns:{' '}
          <strong>date, amount, type, category_id, account_id, description</strong>
        </p>
        <button className="btn btn-outline-secondary btn-sm mb-3 d-flex align-items-center gap-1"
          onClick={downloadTemplate}>
          <IconDownload size={14} stroke={1.5} /> Download template CSV
        </button>
        {error   && <div className="alert alert-danger mb-3">{error}</div>}
        {success && <div className="alert alert-success mb-3">{success}</div>}
        <form onSubmit={handleImport}>
          <input
            type="file" className="form-control mb-3" accept=".csv,.xlsx"
            onChange={e => setFile(e.target.files[0])}
          />
          <div className="d-flex gap-2">
            <button type="submit" className="btn btn-primary d-flex align-items-center gap-1"
              disabled={!file || importing}>
              <IconUpload size={16} stroke={1.5} />
              {importing ? 'Importing...' : 'Import'}
            </button>
            <button type="button" className="btn btn-outline-secondary" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}