export const validatePasswordMatch = (password: string, confirmation: string): string => {
  if (password !== confirmation) return 'Пароли не совпадают.'
  if (password.length > 0 && password.length < 6) return 'Пароль должен быть не менее 6 символов.'
  return ''
}

export const formatPhone = (value: string): string => {
  let digits = value.replace(/\D/g, '')
  if (!digits) return ''
  if (digits.startsWith('8')) digits = `7${digits.slice(1)}`
  if (!digits.startsWith('7')) digits = `7${digits}`
  digits = digits.slice(0, 11)

  let result = '+7'
  if (digits.length > 1) result += ` (${digits.slice(1, 4)}`
  if (digits.length >= 4) result += ')'
  if (digits.length > 4) result += ` ${digits.slice(4, 7)}`
  if (digits.length > 7) result += ` ${digits.slice(7, 9)}`
  if (digits.length > 9) result += ` ${digits.slice(9, 11)}`
  return result
}

export const allowPhoneKey = (event: KeyboardEvent): void => {
  const allowedKeys = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', 'Home', 'End']
  if (allowedKeys.includes(event.key) || event.ctrlKey || event.metaKey) return
  if (!/\d/.test(event.key)) event.preventDefault()
}
