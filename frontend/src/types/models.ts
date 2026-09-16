export type User = {
  id: number
  email: string
  phone: string
  password: string
  name?: string
  imageUrl?: string
}

export type UserUpdate = Partial<Pick<User, 'name' | 'phone' | 'password' | 'imageUrl'>>
