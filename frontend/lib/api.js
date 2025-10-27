export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

export async function generateVideo(payload) {
  try {
    const res = await fetch(`${API_BASE}/api/generate-video`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    if (!res.ok) throw new Error('Request failed')
    return await res.json()
  } catch (e) {
    console.error(e)
    return null
  }
}

export async function getStatus(id) {
  try {
    const res = await fetch(`${API_BASE}/api/status/${id}`)
    if (!res.ok) throw new Error('Request failed')
    return await res.json()
  } catch (e) {
    console.error(e)
    return null
  }
}
