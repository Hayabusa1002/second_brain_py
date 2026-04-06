import { useState } from 'react'
import * as XLSX from 'xlsx'
import * as YAML from 'js-yaml'
import client from '../../api/client'

export default function ImportModal({ onClose, onSuccess }) {
  const [file, setFile] = useState(null)
  const [importing, setImporting] = useState(false)
  const [error, setError] = useState('')
  const [summary, setSummary] = useState(null)

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

  async function findCategoryId(name, type) {
    const { data } = await client.get('/categories')
    const categories = data.categories ?? data.items ?? data

    const existing = categories.find(
      (c) =>
        c.name?.trim().toLowerCase() === name.trim().toLowerCase() &&
        c.type === type
    )

    return existing?.id ?? null
  }

  async function handleImport() {
    if (!file) return

    setImporting(true)
    setError('')
    setSummary(null)

    try {
      const parsedRows = await parseFile(file)
      const items = normalizeRows(parsedRows)

      let createdCategories = 0
      let createdSubcategories = 0

      for (const item of items) {
        let categoryId = null

        try {
          const { data } = await client.post('/categories', {
            name: item.name,
            type: item.type,
          })
          categoryId = data.id
          createdCategories += 1
        } catch {
          categoryId = await findCategoryId(item.name, item.type)
        }

        if (categoryId && item.subcategories.length > 0) {
          for (const subName of item.subcategories) {
            try {
              await client.post('/subcategories', {
                name: subName,
                category_id: categoryId,
              })
              createdSubcategories += 1
            } catch {
              // ignore duplicates
            }
          }
        }
      }

      setSummary({
        categories: createdCategories,
        subcategories: createdSubcategories,
      })

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
              <div className="alert alert-success">
                Imported {summary.categories} categories and {summary.subcategories} subcategories.
              </div>
            )}

            <div className="mb-3">
              <label className="form-label">Download examples</label>

              <div className="d-flex flex-wrap gap-2">
                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm"
                  onClick={() =>
                    window.open(
                      'http://localhost:8000/api/categories/import/template/csv',
                      '_blank'
                    )
                  }
                >
                  CSV
                </button>

                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm"
                  onClick={() =>
                    window.open(
                      'http://localhost:8000/api/categories/import/template/json',
                      '_blank'
                    )
                  }
                >
                  JSON
                </button>

                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm"
                  onClick={() =>
                    window.open(
                      'http://localhost:8000/api/categories/import/template/yaml',
                      '_blank'
                    )
                  }
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