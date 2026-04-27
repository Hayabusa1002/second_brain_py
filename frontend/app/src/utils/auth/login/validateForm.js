const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function validateForm(form) {
  const errors = {}

  const email = form.email.trim()
  const password = form.password

  if (!email) {
    errors.email = 'Email is required.'
  } else if (!emailRegex.test(email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (!password.trim()) {
    errors.password = 'Password is required.'
  }

  return errors
}