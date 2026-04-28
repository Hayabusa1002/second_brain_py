const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function validateForm(profile) {
  const errors = {}

  const name = profile.name.trim()
  const email = profile.email.trim()

  if (!name) {
    errors.name = 'Name is required.'
  }

  if (!email) {
    errors.email = 'Email is required.'
  } else if (!emailRegex.test(email)) {
    errors.email = 'Enter a valid email address.'
  }

  return errors
}