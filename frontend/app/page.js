import Hero from '../components/Hero'

export default function HomePage() {
  return (
    <div className="space-y-12">
      <Hero />

      <section className="grid md:grid-cols-3 gap-6">
        <div className="card p-6">
          <h3 className="font-semibold mb-2">Local-Only</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">All generation runs on your machine. No external APIs.</p>
        </div>
        <div className="card p-6">
          <h3 className="font-semibold mb-2">Faceless by Design</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">Prompts are guided to avoid faces and watermarks.</p>
        </div>
        <div className="card p-6">
          <h3 className="font-semibold mb-2">Simple Workflow</h3>
          <p className="text-sm text-slate-600 dark:text-slate-400">Type a prompt, pick a style, and render.</p>
        </div>
      </section>
    </div>
  )
}
