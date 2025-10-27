'use client'
import { useState } from 'react'

export const metadata = { title: 'Contact - Faceless AI Video' }

export default function ContactPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')

  function onSubmit(e) {
    e.preventDefault()
    const subject = encodeURIComponent('Faceless AI Video - Contact')
    const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\n${message}`)
    window.location.href = `mailto:support@example.com?subject=${subject}&body=${body}`
  }

  return (
    <form onSubmit={onSubmit} className="card p-6 max-w-2xl">
      <h1 className="text-xl font-semibold mb-4">Contact</h1>
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label className="label">Name</label>
          <input className="input" value={name} onChange={e=>setName(e.target.value)} />
        </div>
        <div>
          <label className="label">Email</label>
          <input className="input" type="email" value={email} onChange={e=>setEmail(e.target.value)} />
        </div>
        <div className="md:col-span-2">
          <label className="label">Message</label>
          <textarea className="textarea h-32" value={message} onChange={e=>setMessage(e.target.value)} />
        </div>
      </div>
      <div className="mt-4">
        <button className="btn-primary">Send Email</button>
      </div>
    </form>
  )
}
