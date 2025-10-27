export default function VideoCard({ videoUrl, status }) {
  return (
    <div className="card p-4">
      <h2 className="text-lg font-semibold mb-3">Preview</h2>
      <div className="relative aspect-video w-full bg-slate-100 dark:bg-slate-900 rounded-md overflow-hidden">
        {videoUrl ? (
          <video controls className="w-full h-full">
            <source src={videoUrl} type="video/mp4" />
          </video>
        ) : (
          <img src="/placeholder.svg" alt="Video placeholder" className="w-full h-full object-cover" />
        )}
        {!videoUrl && status && (
          <div className="absolute inset-0 grid place-items-center bg-black/30 text-white text-sm">Rendering…</div>
        )}
      </div>
      {videoUrl && (
        <div className="mt-3 flex items-center gap-3">
          <a className="btn-outline" href={videoUrl} download>Download</a>
          <a className="text-sm text-slate-600 dark:text-slate-400 hover:underline" href={videoUrl} target="_blank">Open in new tab</a>
        </div>
      )}
    </div>
  )
}
