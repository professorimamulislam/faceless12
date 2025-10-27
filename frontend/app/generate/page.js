'use client'
import { useEffect, useMemo, useState } from 'react'
import { API_BASE, generateVideo, getStatus } from '../../lib/api'
import VideoCard from '../../components/VideoCard'

const STYLE_PRESETS = ['cinematic','anime','neon','watercolor','photoreal']

export default function GeneratePage() {
  const [prompt, setPrompt] = useState('A serene abstract landscape with moving light patterns and soft gradients')
  const [style, setStyle] = useState('cinematic')
  const [numScenes, setNumScenes] = useState(5)
  const [duration, setDuration] = useState(3)
  const [fps, setFps] = useState(24)
  const [addMusic, setAddMusic] = useState(true)
  const [addTts, setAddTts] = useState(false)
  const [voice, setVoice] = useState('en')

  const [jobId, setJobId] = useState(null)
  const [status, setStatus] = useState(null)
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('')
  const [videoUrl, setVideoUrl] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!jobId) return
    const iv = setInterval(async () => {
      const res = await getStatus(jobId)
      if (res) {
        setStatus(res.status)
        setProgress(Math.round(res.progress || 0))
        setMessage(res.message || '')
        if (res.status === 'completed') {
          setVideoUrl(`${API_BASE}${res.video_url}`)
          clearInterval(iv)
          setLoading(false)
        }
        if (res.status === 'failed') {
          clearInterval(iv)
          setLoading(false)
        }
      }
    }, 1500)
    return () => clearInterval(iv)
  }, [jobId])

  const canSubmit = prompt.trim().length > 0 && !loading

  async function onSubmit(e) {
    e.preventDefault()
    if (!canSubmit) return
    setLoading(true)
    setVideoUrl(null)
    setStatus('pending')
    setProgress(0)
    setMessage('Queued')
    const payload = {
      prompt,
      style,
      num_scenes: Number(numScenes),
      duration_per_scene: Number(duration),
      fps: Number(fps),
      add_music: Boolean(addMusic),
      add_tts: Boolean(addTts),
      voice,
    }
    const res = await generateVideo(payload)
    if (res && res.job_id) {
      setJobId(res.job_id)
    } else {
      setLoading(false)
    }
  }

  return (
    <div className="grid lg:grid-cols-2 gap-8">
      <form onSubmit={onSubmit} className="card p-6 space-y-4">
        <div>
          <label className="label">Prompt</label>
          <textarea className="textarea h-32" value={prompt} onChange={e=>setPrompt(e.target.value)} placeholder="Describe the scenes you want to see" />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div>
            <label className="label">Style</label>
            <select className="select" value={style} onChange={e=>setStyle(e.target.value)}>
              {STYLE_PRESETS.map(s=> (<option key={s} value={s}>{s}</option>))}
            </select>
          </div>
          <div>
            <label className="label">Scenes</label>
            <input className="input" type="number" min={1} max={10} value={numScenes} onChange={e=>setNumScenes(e.target.value)} />
          </div>
          <div>
            <label className="label">Sec/scene</label>
            <input className="input" type="number" min={1} max={15} step="0.5" value={duration} onChange={e=>setDuration(e.target.value)} />
          </div>
          <div>
            <label className="label">FPS</label>
            <input className="input" type="number" min={8} max={60} value={fps} onChange={e=>setFps(e.target.value)} />
          </div>
          <div className="flex items-center gap-2">
            <input id="music" type="checkbox" checked={addMusic} onChange={e=>setAddMusic(e.target.checked)} />
            <label htmlFor="music" className="label">Background music</label>
          </div>
          <div className="flex items-center gap-2">
            <input id="tts" type="checkbox" checked={addTts} onChange={e=>setAddTts(e.target.checked)} />
            <label htmlFor="tts" className="label">Voiceover (TTS)</label>
          </div>
          {addTts && (
            <div>
              <label className="label">Voice</label>
              <input className="input" value={voice} onChange={e=>setVoice(e.target.value)} />
            </div>
          )}
        </div>

        <div className="flex items-center gap-3">
          <button className="btn-primary" disabled={!canSubmit}>Generate Video</button>
          {loading && (
            <span className="text-sm text-slate-500">Submitting...</span>
          )}
        </div>

        {status && (
          <div className="space-y-2">
            <div className="text-sm text-slate-600 dark:text-slate-400">{message}</div>
            <div className="w-full h-2 rounded bg-slate-200 dark:bg-slate-800 overflow-hidden">
              <div className="h-full bg-brand" style={{width: `${progress}%`}} />
            </div>
          </div>
        )}
      </form>

      <div>
        <VideoCard videoUrl={videoUrl} status={status} />
      </div>
    </div>
  )
}
