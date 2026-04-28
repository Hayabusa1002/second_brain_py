export default function parseAuthErrors(
  err,
  fallbackMessage = 'Request failed. Try again.'
) {
  const detail = err.response?.data?.detail

  if (typeof detail === 'string' && detail.trim()) {
    return detail
  }

  return fallbackMessage
}