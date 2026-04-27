const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function validateRegisterForm(form) {
  const errors = {}

  const name = form.name.trim()
  const email = form.email.trim()
  const password = form.password

  if (!name) {
    errors.name = 'Name is required.'
  }

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