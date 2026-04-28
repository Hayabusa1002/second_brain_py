export default function validateForm(form) {
  const errors = {}

  const currentPassword = form.current_password.trim()
  const newPassword = form.new_password
  const confirmPassword = form.confirm_password

  if (!currentPassword) {
    errors.current_password = 'Current password is required.'
  }

  if (!newPassword.trim()) {
    errors.new_password = 'New password is required.'
  } else if (newPassword.length < 8) {
    errors.new_password = 'New password must be at least 8 characters.'
  } else if (newPassword === currentPassword) {
    errors.new_password = 'Password already used.'
  }

  if (!confirmPassword.trim()) {
    errors.confirm_password = 'Please confirm your new password.'
  } else if (newPassword !== confirmPassword) {
    errors.confirm_password = 'New passwords do not match.'
  }

  return errors
}