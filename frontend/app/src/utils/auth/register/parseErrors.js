export default function parseErrors(err) {
  const detail = err.response?.data?.detail
  const errors = err.response?.data?.errors

  if (typeof detail === 'string') {
    return {
      error: detail,
      fieldErrors: {},
    }
  }

  if (Array.isArray(detail)) {
    const fieldErrors = {}

    detail.forEach((item) => {
      const field =
        item.field ||
        (Array.isArray(item.loc) ? item.loc[item.loc.length - 1] : null)

      const message = item.message || item.msg || 'Invalid value.'

      if (field) {
        fieldErrors[field] = message
      }
    })

    return {
      error:
        Object.keys(fieldErrors).length > 0
          ? 'Please review the highlighted fields.'
          : 'Registration failed. Please check the form.',
      fieldErrors,
    }
  }

  if (errors && typeof errors === 'object') {
    const fieldErrors = {}

    Object.entries(errors).forEach(([field, messages]) => {
      fieldErrors[field] = Array.isArray(messages)
        ? messages.join(', ')
        : messages
    })

    return {
      error:
        Object.keys(fieldErrors).length > 0
          ? 'Please review the highlighted fields.'
          : 'Registration failed. Please check the form.',
      fieldErrors,
    }
  }

  return {
    error: 'Registration failed. Try again.',
    fieldErrors: {},
  }
}