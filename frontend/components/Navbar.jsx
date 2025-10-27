import Link from 'next/link'
import ThemeToggle from './ThemeToggle'

export default function Navbar() {
  return (
    <header className="border-b border-slate-200 dark:border-slate-800">
      <div className="container-page py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/" className="font-semibold text-lg">Faceless AI Video</Link>
          <nav className="hidden md:flex items-center gap-4 text-sm text-slate-600 dark:text-slate-400">
            <Link href="/generate" className="hover:text-slate-900 dark:hover:text-slate-100 transition">Generate</Link>
            <Link href="/about" className="hover:text-slate-900 dark:hover:text-slate-100 transition">About</Link>
            <Link href="/contact" className="hover:text-slate-900 dark:hover:text-slate-100 transition">Contact</Link>
          </nav>
        </div>
        <div className="flex items-center gap-2">
          <Link href="/generate" className="btn-outline hidden sm:inline-flex">Try it</Link>
          <ThemeToggle />
        </div>
      </div>
    </header>
  )
}
