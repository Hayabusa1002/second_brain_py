import { useState } from 'react'
import * as XLSX from 'xlsx'
import * as YAML from 'js-yaml'
import client from '../../api/client'

const API_URL = import.meta.env.VITE_API_URL

export default function ImportModal({ onClose, onSuccess }) {
  const [file, setFile] = useState(null)
  const [importing, setImporting] = useState(false)
  const [error, setError] = useState('')
  const [summary, setSummary] = useState(null)
  const [importLog, setImportLog] = useState(null)

  function normalizeRows(rows) {
    return rows
      .map((row) => ({
        name: String(row.name ?? row.Name ?? '').trim(),
        address: String(row.address ?? row.Address ?? '').trim(),
        city: String(row.city ?? row.City ?? '').trim(),
        country: String(row.country ?? row.Country ?? '').trim(),
      }))
      .filter((row) => row.name && row.country)
  }

  async function parseFile(inputFile) {
    const ext = inputFile.name.split('.').pop()?.toLowerCase()

    if (ext === 'csv' || ext === 'xlsx' || ext === 'xls') {
      const buffer = await inputFile.arrayBuffer()
      const workbook = XLSX.read(buffer, { type: 'array' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]
      return XLSX.utils.sheet_to_json(sheet)
    }

    if (ext === 'json') {
      const text = await inputFile.text()
      const parsed = JSON.parse(text)
      return Array.isArray(parsed) ? parsed : []
    }

    if (ext === 'yaml' || ext === 'yml') {
      const text = await inputFile.text()
      const parsed = YAML.load(text)
      return Array.isArray(parsed) ? parsed : []
    }

    throw new Error('Unsupported file format.')
  }

  async function getStores() {
    const { data } = await client.get('/stores')
    return data.stores ?? data.items ?? data ?? []
  }

  async function findStore(name, address, city, country) {
    const stores = await getStores()
    return (
      stores.find(
        (s) =>
          s.name?.trim().toLowerCase() === name.trim().toLowerCase() &&
          String(s.address ?? '').trim().toLowerCase() === String(address ?? '').trim().toLowerCase() &&
          String(s.city ?? '').trim().toLowerCase() === String(city ?? '').trim().toLowerCase() &&
          s.country?.trim().toLowerCase() === country.trim().toLowerCase()
      ) ?? null
    )
  }

  function downloadLog() {
    if (!importLog) return

    const blob = new Blob([JSON.stringify(importLog, null, 2)], {
      type: 'application/json;charset=utf-8;',
    })

    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `stores-import-log-${new Date().toISOString().replace(/[:.]/g, '-')}.json`
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  async function handleImport() {
    if (!file) return

    setImporting(true)
    setError('')
    setSummary(null)
    setImportLog(null)

    try {
      const parsedRows = await parseFile(file)
      const items = normalizeRows(parsedRows)

      let createdStores = 0

      const log = {
        file_name: file.name,
        imported_at: new Date().toISOString(),
        totals: {
          rows_detected: parsedRows.length,
          rows_normalized: items.length,
          stores_created: 0,
          store_existing: 0,
          failed_stores: 0,
        },
        details: [],
      }

      for (const item of items) {
        let storeId = null
        let storeStatus = 'unknown'
        let storeMessage = ''

        try {
          const { data } = await client.post('/stores', {
            name: item.name,
            address: item.address,
            city: item.city,
            country: item.country,
          })

          storeId = data.id
          createdStores += 1
          storeStatus = 'created'
          storeMessage = 'Store created successfully.'
        } catch (err) {
          const existing = await findStore(item.name, item.address, item.city, item.country)

          if (existing?.id) {
            storeId = existing.id
            storeStatus = 'existing'
            storeMessage = 'Store already existed.'
          } else {
            storeStatus = 'failed'
            storeMessage = err.response?.data?.detail || 'Failed to create or locate store.'
            log.totals.failed_stores += 1
          }
        }

        if (storeStatus === 'existing') {
          log.totals.store_existing += 1
        }

        log.details.push({
          store: {
            id: storeId,
            name: item.name,
            address: item.address,
            city: item.city,
            country: item.country,
            status: storeStatus,
            message: storeMessage,
          },
        })
      }

      log.totals.stores_created = createdStores

      setSummary({ stores: createdStores })
      setImportLog(log)

      if (onSuccess) await onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to import file.')
    } finally {
      setImporting(false)
    }
  }

  function openTemplate(format) {
    const url = new URL(`/api/stores/import/template/${format}`, API_URL)
    window.open(url.toString(), '_blank', 'noopener,noreferrer')
  }

  return (
    <div className="modal modal-blur fade show d-block" style={{ backgroundColor: 'rgba(0, 0, 0, 0.4)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Import Stores</h5>
            <button type="button" className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger">{error}</div>}

            {summary && (
              <div className="alert alert-success d-flex justify-content-between align-items-center gap-3">
                <span>Imported {summary.stores} stores.</span>
                {importLog && (
                  <button
                    type="button"
                    className="btn btn-sm btn-outline-success"
                    onClick={downloadLog}
                  >
                    Download log
                  </button>
                )}
              </div>
            )}

            <div className="mb-3">
              <label className="form-label">Download examples</label>
              <div className="d-flex flex-wrap gap-2">
                <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => openTemplate('csv')}>
                  CSV
                </button>
                <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => openTemplate('json')}>
                  JSON
                </button>
                <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => openTemplate('yaml')}>
                  YAML
                </button>
              </div>
            </div>

            <div className="mb-3">
              <div className="text-secondary small">
                Supported formats: CSV, XLSX, JSON, YAML.
                <br />
                Fields: <strong>name</strong>, <strong>address</strong>, <strong>city</strong>, <strong>country</strong>.
              </div>
            </div>

            <div className="mb-3">
              <label className="form-label">File</label>
              <input
                type="file"
                className="form-control"
                accept=".csv,.xlsx,.xls,.json,.yaml,.yml"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              />
            </div>
          </div>

          <div className="modal-footer">
            <button type="button" className="btn btn-outline-secondary" onClick={onClose}>
              Close
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleImport}
              disabled={!file || importing}
            >
              {importing ? 'Importing...' : 'Import'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}