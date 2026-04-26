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
      .map((row) => {
        const subRaw =
          row.subcategories ??
          row.Subcategories ??
          row.subcategory_names ??
          row.Subcategory_names ??
          row.subcategory ??
          row.Subcategory ??
          ''

        let subcategories = []

        if (Array.isArray(subRaw)) {
          subcategories = subRaw
            .map((s) => {
              if (typeof s === 'object' && s !== null) {
                return String(s.name ?? '').trim()
              }
              return String(s).trim()
            })
            .filter(Boolean)
        } else {
          subcategories = String(subRaw)
            .split('|')
            .map((s) => s.trim())
            .filter(Boolean)
        }

        return {
          name: String(row.name ?? row.Name ?? '').trim(),
          type: String(row.type ?? row.Type ?? '').trim().toLowerCase(),
          address: String(row.address ?? row.Address ?? '').trim(),
          website: String(row.website ?? row.Website ?? '').trim(),
          subcategories,
        }
      })
      .filter((row) => row.name && row.type)
  }

  async function parseFile(inputFile) {
    const ext = inputFile.name.split('.').pop()?.toLowerCase()

    if (ext === 'csv' || ext === 'xlsx' || ext === 'xls') {
      const buffer = await inputFile.arrayBuffer()
      const workbook = XLSX.read(buffer, { type: 'array' })
      const sheet = workbook.Sheets[workbook.SheetNames[0]]
      return XLSX.utils.sheet_to_json(sheet, { defval: '' })
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

  async function getAllSubcategories() {
    const { data } = await client.get('/subcategories')
    return data.subcategories ?? data.items ?? data ?? []
  }

  async function getStoreSubcategories(storeId) {
    const { data } = await client.get(`/stores/${storeId}/subcategories`)
    return data.subcategories ?? data.items ?? data ?? []
  }

  async function findStore(name, type, address, website) {
    const stores = await getStores()

    return (
      stores.find(
        (s) =>
          s.name?.trim().toLowerCase() === name.trim().toLowerCase() &&
          String(s.type ?? '').trim().toLowerCase() === String(type ?? '').trim().toLowerCase() &&
          String(s.address ?? '').trim().toLowerCase() === String(address ?? '').trim().toLowerCase() &&
          String(s.website ?? '').trim().toLowerCase() === String(website ?? '').trim().toLowerCase()
      ) ?? null
    )
  }

  function matchSubcategoriesByName(allSubcategories, names) {
    return names.map((name) => {
      const found =
        allSubcategories.find(
          (s) =>
            s.name?.trim().toLowerCase() === name.trim().toLowerCase()
        ) ?? null

      return {
        name,
        id: found?.id ?? null,
      }
    })
  }

  function extractAssignedSubcategoryIds(items) {
    if (!Array.isArray(items)) return []

    return items
      .map((item) => item.subcategory_id ?? item.subcategory?.id ?? item.id)
      .filter(Boolean)
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

  function openTemplate(format) {
    const url = new URL(`/api/stores/import/template/${format}`, API_URL)
    window.open(url.toString(), '_blank', 'noopener,noreferrer')
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
      const allSubcategories = await getAllSubcategories()

      let createdStores = 0
      let assignedSubcategories = 0

      const log = {
        file_name: file.name,
        imported_at: new Date().toISOString(),
        totals: {
          rows_detected: parsedRows.length,
          rows_normalized: items.length,
          stores_created: 0,
          subcategories_created: 0,
          store_existing: 0,
          subcategory_existing_or_skipped: 0,
          failed_stores: 0,
          failed_subcategories: 0,
        },
        details: [],
      }

      for (const item of items) {
        let storeId = null
        let storeStatus = 'unknown'
        let storeMessage = ''
        let subcategoryLogs = []

        try {
          const { data } = await client.post('/stores', {
            name: item.name,
            type: item.type,
            address: item.address || null,
            website: item.website || null,
          })

          storeId = data.id
          createdStores += 1
          storeStatus = 'created'
          storeMessage = 'Store created successfully.'
        } catch (err) {
          const existing = await findStore(
            item.name,
            item.type,
            item.address,
            item.website
          )

          if (existing?.id) {
            storeId = existing.id
            storeStatus = 'existing'
            storeMessage = 'Store already existed.'
            log.totals.store_existing += 1
          } else {
            storeStatus = 'failed'
            storeMessage =
              err.response?.data?.detail ||
              'Failed to create or locate store.'
            log.totals.failed_stores += 1
          }
        }

        if (storeId && item.subcategories.length > 0) {
          const matched = matchSubcategoriesByName(
            allSubcategories,
            item.subcategories
          )

          const missing = matched.filter((m) => !m.id)
          const validIds = matched.filter((m) => m.id).map((m) => m.id)

          if (missing.length > 0) {
            log.totals.subcategory_existing_or_skipped += missing.length

            subcategoryLogs.push(
              ...missing.map((m) => ({
                name: m.name,
                status: 'skipped',
                message: 'Subcategory name not found in catalog.',
              }))
            )
          }

          if (validIds.length > 0) {
            try {
              const currentAssignments = await getStoreSubcategories(storeId)
              const currentIds = extractAssignedSubcategoryIds(currentAssignments)

              const mergedIds = [...new Set([...currentIds, ...validIds])]

              await client.put(`/stores/${storeId}/subcategories`, {
                subcategory_ids: mergedIds,
              })

              assignedSubcategories += validIds.length

              subcategoryLogs.push(
                ...matched
                  .filter((m) => m.id)
                  .map((m) => ({
                    name: m.name,
                    status: 'assigned',
                    message: 'Subcategory assigned successfully.',
                  }))
              )
            } catch (err) {
              log.totals.failed_subcategories += validIds.length

              subcategoryLogs.push(
                ...matched
                  .filter((m) => m.id)
                  .map((m) => ({
                    name: m.name,
                    status: 'failed',
                    message:
                      err.response?.data?.detail ||
                      'Failed to assign subcategory.',
                  }))
              )
            }
          }
        }

        log.details.push({
          store: {
            name: item.name,
            type: item.type,
            address: item.address,
            website: item.website,
            id: storeId,
            status: storeStatus,
            message: storeMessage,
          },
          subcategories: subcategoryLogs,
        })
      }

      log.totals.stores_created = createdStores
      log.totals.subcategories_created = assignedSubcategories

      setSummary({
        stores: createdStores,
        subcategories: assignedSubcategories,
      })

      setImportLog(log)

      if (onSuccess) await onSuccess()
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Failed to import file.'
      )
    } finally {
      setImporting(false)
    }
  }

  return (
    <div
      className="modal modal-blur fade show d-block"
      style={{ backgroundColor: 'rgba(0, 0, 0, 0.4)' }}
    >
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
                <span>
                  Imported {summary.stores} stores and assigned {summary.subcategories} subcategories.
                </span>

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
                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm"
                  onClick={() => openTemplate('csv')}
                >
                  CSV
                </button>
                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm"
                  onClick={() => openTemplate('json')}
                >
                  JSON
                </button>
                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm"
                  onClick={() => openTemplate('yaml')}
                >
                  YAML
                </button>
              </div>
            </div>

            <div className="mb-3">
              <div className="text-secondary small">
                Supported formats: CSV, XLSX, JSON, YAML.
                <br />
                Fields: <strong>name</strong>, <strong>type</strong>, <strong>address</strong>, <strong>website</strong>.
                <br />
                Valid store types: <strong>physical</strong>, <strong>online</strong>, <strong>subscription</strong>, <strong>service</strong>.
                <br />
                CSV/XLSX use <strong>subcategory_names</strong> separated by <strong>|</strong>.
                <br />
                JSON/YAML can use <strong>subcategories</strong> as strings or objects.
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
            <button
              type="button"
              className="btn btn-outline-secondary"
              onClick={onClose}
            >
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