import './globals.css'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { ThemeProvider } from '../components/ThemeProvider'

export const metadata = {
  title: 'Faceless AI Video - Generate Videos from Prompts',
  description: 'Create faceless AI videos locally from text prompts. No external APIs required.',
  openGraph: {
    title: 'Faceless AI Video',
    description: 'Generate faceless AI videos locally from prompts.',
    url: 'http://localhost:3000',
    type: 'website'
  },
  keywords: ['AI video', 'stable diffusion', 'moviepy', 'ffmpeg', 'local generation']
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <Navbar />
          <main className="container-page py-10">{children}</main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  )
}
