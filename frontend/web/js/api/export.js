function buildQuery(filters = {}) {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([k, v]) => {
        if (v !== undefined && v !== "") params.append(k, v)
    })
    const qs = params.toString()
    return qs ? `?${qs}` : ""
}

export function exportCsv(filters = {}) {
    window.location.href = `/api/export/csv${buildQuery(filters)}`
}

export function exportJson(filters = {}) {
    window.location.href = `/api/export/json${buildQuery(filters)}`
}

export function exportXlsx(filters = {}) {
    window.location.href = `/api/export/xlsx${buildQuery(filters)}`
}

export function exportPdf(filters = {}) {
    window.location.href = `/api/export/pdf${buildQuery(filters)}`
}