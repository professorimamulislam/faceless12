'use client'
import { useEffect, useState } from 'react'

export default function TypingEffect({ words = [], speed = 45, pause = 900 }) {
  const [idx, setIdx] = useState(0)
  const [text, setText] = useState('')

  useEffect(() => {
    let cancelled = false
    const word = words[idx % words.length] || ''

    let i = 0
    const type = () => {
      if (cancelled) return
      if (i <= word.length) {
        setText(word.slice(0, i))
        i++
        setTimeout(type, speed)
      } else {
        setTimeout(() => setIdx(i => i + 1), pause)
      }
    }
    type()
    return () => { cancelled = true }
  }, [idx, words, speed, pause])

  return <span className="typing-caret">{text}</span>
}
