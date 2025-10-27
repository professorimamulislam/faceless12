import Link from 'next/link'
import TypingEffect from './TypingEffect'

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 -z-10 opacity-40 dark:opacity-30" aria-hidden>
        <div className="h-full w-full bg-gradient-to-br from-brand/30 via-fuchsia-300/30 to-sky-300/30 dark:from-brand/20 dark:via-fuchsia-500/10 dark:to-sky-500/10 blur-3xl" />
      </div>
      <div className="text-center py-16 md:py-24">
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight">
          Generate <span className="text-brand">Faceless</span> AI Videos
        </h1>
        <div className="mt-4 text-lg md:text-xl text-slate-600 dark:text-slate-400">
          <TypingEffect words={[
            'From plain prompts',
            'Locally. No APIs.',
            'Cinematic. Anime. Neon.'
          ]} />
        </div>
        <div className="mt-8 flex items-center justify-center gap-3">
          <Link href="/generate" className="btn-primary">Generate Video</Link>
          <a href="#how" className="btn-outline">Learn more</a>
        </div>
      </div>
      <div id="how" className="grid md:grid-cols-3 gap-6 pt-8">
        <div className="card p-6">
          <h3 className="font-semibold mb-2">Prompt in</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">Describe your scenes in natural language.</p>
        </div>
        <div className="card p-6">
          <h3 className="font-semibold mb-2">Local render</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">Images are generated locally and compiled.</p>
        </div>
        <div className="card p-6">
          <h3 className="font-semibold mb-2">Download</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">Preview, then download your MP4.</p>
        </div>
      </div>
    </section>
  )
}
