function buildQuery(filters = {}) {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([k, v]) => {
        if (v !== undefined && v !== "") params.append(k, v)
    })
    const qs = params.toString()
    return qs ? `?${qs}` : ""
}

function triggerDownload(url) {
    const a = document.createElement("a")
    a.href = url
    a.download = ""
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
}

export function exportCsv(filters = {}) {
    triggerDownload(`/api/export/csv${buildQuery(filters)}`)
}

export function exportJson(filters = {}) {
    triggerDownload(`/api/export/json${buildQuery(filters)}`)
}

export function exportXlsx(filters = {}) {
    triggerDownload(`/api/export/xlsx${buildQuery(filters)}`)
}

export function exportPdf(filters = {}) {
    triggerDownload(`/api/export/pdf${buildQuery(filters)}`)
}