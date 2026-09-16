import axios from 'axios'
export type ListingTag = { name: string; selected: boolean }
export type CarListing = { id: string | number; title: string; category?: string; action?: string; price?: number; location?: string; description?: string; image?: string; detailimg?: string; name?: string; avatar?: string; owner_email?: string; tags: ListingTag[]; date?: string }
export const profileCarsUrl = (email: string) => `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/profiles/${encodeURIComponent(email)}/cars`
export const CAR_API_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/cars`
export const SELLER_CARS_API_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/seller-cars`
export const BUYER_REQUESTS_API_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/buyer-requests`
export const UPLOAD_API_URL = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/uploads`
const normalizeTags = (tags?: string[]): ListingTag[] => (tags || []).map((name) => ({ name, selected: false }))
export const fetchCarListings = async (): Promise<CarListing[]> => {
  const { data } = await axios.get<CarListing[]>(CAR_API_URL)
  return data.map((item) => ({ ...item, tags: normalizeTags(item.tags as unknown as string[]) }))
}
export const saveCarListingTags = async (input: CarListing | CarListing[]) => {
  const items = Array.isArray(input) ? input : [input]
  await Promise.all(items.map((item) => fetch(`${CAR_API_URL}/${item.id}/tags`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tags: item.tags.map((tag) => tag.name) }),
  })))
}
