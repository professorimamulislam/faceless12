export default function Footer() {
  return (
    <footer className="mt-16 border-t border-slate-200 dark:border-slate-800">
      <div className="container-page py-8 text-sm text-slate-600 dark:text-slate-400 flex items-center justify-between">
        <div>© {new Date().getFullYear()} Faceless AI Video</div>
        <div className="space-x-4">
          <a className="hover:underline" href="/about">About</a>
          <a className="hover:underline" href="/contact">Contact</a>
        </div>
      </div>
    </footer>
  )
}
