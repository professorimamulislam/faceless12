export const metadata = { title: 'About - Faceless AI Video' }

export default function AboutPage() {
  return (
    <div className="prose prose-slate dark:prose-invert max-w-none">
      <h1>About</h1>
      <p>
        Faceless AI Video is a local-first tool that turns text prompts into short videos. It assembles multiple scenes, applies gentle camera motion, and can mix background music or an optional voiceover. When a local Stable Diffusion model is available, it uses it for image synthesis. Otherwise, it generates tasteful placeholders so the workflow remains usable offline.
      </p>
      <h2>Technology</h2>
      <ul>
        <li>Frontend: Next.js + TailwindCSS</li>
        <li>Backend: FastAPI (Python), MoviePy/FFmpeg</li>
        <li>Optional: Diffusers (Stable Diffusion) for local image generation</li>
        <li>Optional: Coqui TTS for text-to-speech</li>
      </ul>
    </div>
  )
}
