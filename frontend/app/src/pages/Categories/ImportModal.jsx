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
          row.subcategory ??
          row.subcategory_names ??
          row.Subcategory_names ??
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
          type: String(row.type ?? row.Type ?? '')
            .trim()
            .toLowerCase(),
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

  async function getCategories() {
    const { data } = await client.get('/categories')
    return data.categories ?? data.items ?? data ?? []
  }

  async function findCategory(name, type) {
    const categories = await getCategories()

    return (
      categories.find(
        (c) =>
          c.name?.trim().toLowerCase() === name.trim().toLowerCase() &&
          c.type === type
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
    a.download = `categories-import-log-${new Date().toISOString().replace(/[:.]/g, '-')}.json`
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  function openTemplate(format) {
    const url = new URL(`/api/categories/import/template/${format}`, API_URL)
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

      let createdCategories = 0
      let createdSubcategories = 0

      const log = {
        file_name: file.name,
        imported_at: new Date().toISOString(),
        totals: {
          rows_detected: parsedRows.length,
          rows_normalized: items.length,
          categories_created: 0,
          subcategories_created: 0,
          category_existing: 0,
          subcategory_existing_or_skipped: 0,
          failed_categories: 0,
          failed_subcategories: 0,
        },
        details: [],
      }

      for (const item of items) {
        let categoryId = null
        let categoryStatus = 'unknown'
        let categoryMessage = ''
        const subcategoryLogs = []

        try {
          const { data } = await client.post('/categories', {
            name: item.name,
            type: item.type,
          })

          categoryId = data.id
          createdCategories += 1
          categoryStatus = 'created'
          categoryMessage = 'Category created successfully.'
        } catch (err) {
          const existing = await findCategory(item.name, item.type)

          if (existing?.id) {
            categoryId = existing.id
            categoryStatus = 'existing'
            categoryMessage = 'Category already existed.'
          } else {
            categoryStatus = 'failed'
            categoryMessage =
              err.response?.data?.detail || 'Failed to create or locate category.'
            log.totals.failed_categories += 1
          }
        }

        if (categoryStatus === 'existing') {
          log.totals.category_existing += 1
        }

        if (categoryId && item.subcategories.length > 0) {
          for (const subName of item.subcategories) {
            try {
              await client.post(`/categories/${categoryId}/subcategories/`, {
                name: subName,
              })

              createdSubcategories += 1
              subcategoryLogs.push({
                name: subName,
                status: 'created',
                message: 'Subcategory created successfully.',
              })
            } catch (err) {
              log.totals.subcategory_existing_or_skipped += 1
              const message =
                err.response?.data?.detail || 'Skipped or already exists.'

              subcategoryLogs.push({
                name: subName,
                status: 'skipped',
                message,
              })
            }
          }
        } else if (categoryId && item.subcategories.length === 0) {
          categoryMessage =
            categoryMessage || 'Category processed with no subcategories.'
        }

        log.details.push({
          category: {
            name: item.name,
            type: item.type,
            id: categoryId,
            status: categoryStatus,
            message: categoryMessage,
          },
          subcategories: subcategoryLogs,
        })
      }

      log.totals.categories_created = createdCategories
      log.totals.subcategories_created = createdSubcategories

      setSummary({
        categories: createdCategories,
        subcategories: createdSubcategories,
      })

      setImportLog(log)

      if (onSuccess) await onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to import file.')
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
            <h5 className="modal-title">Import Categories</h5>
            <button type="button" className="btn-close" onClick={onClose} />
          </div>

          <div className="modal-body">
            {error && <div className="alert alert-danger">{error}</div>}

            {summary && (
              <div className="alert alert-success d-flex justify-content-between align-items-center gap-3">
                <span>
                  Imported {summary.categories} categories and {summary.subcategories} subcategories.
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
                CSV/XLSX use <strong>subcategory_names</strong>.
                <br />
                JSON/YAML use <strong>subcategories</strong> as objects.
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