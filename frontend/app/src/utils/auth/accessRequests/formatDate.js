export default function formatDate(value) {
  return value
    ? new Date(value).toLocaleDateString('es-CO', {
        day: '2-digit',
        month: 'numeric',
        year: 'numeric',
      })
    : '—'
}