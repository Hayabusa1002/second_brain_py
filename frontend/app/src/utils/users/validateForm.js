const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const ALLOWED_ROLES = ['partner', 'owner', 'admin']

export default function validateForm(form, mode = 'add') {
  const errors = {}

  const name = (form.name || '').trim()
  const email = (form.email || '').trim()
  const password = form.password || ''
  const role = form.role || ''

  if (!name) {
    errors.name = 'Name is required.'
  }

  if (!email) {
    errors.email = 'Email is required.'
  } else if (!emailRegex.test(email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (mode === 'add') {
    if (!password.trim()) {
      errors.password = 'Password is required.'
    } else if (password.length < 8) {
      errors.password = 'Password must be at least 8 characters.'
    }
  }

  if (!role) {
    errors.role = 'Role is required.'
  } else if (!ALLOWED_ROLES.includes(role)) {
    errors.role = 'Role is not valid.'
  }

  return errors
}