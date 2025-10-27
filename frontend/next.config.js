/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === 'production'
// For GitHub Pages, set NEXT_PUBLIC_BASE_PATH=/your-repo-name in the workflow env
const repoBase = process.env.NEXT_PUBLIC_BASE_PATH || ''

const nextConfig = {
  reactStrictMode: true,
  output: 'export',           // static export
  images: { unoptimized: true },
  basePath: repoBase,         // subpath for GitHub Pages
  assetPrefix: repoBase,      // ensure assets resolve under subpath
}

module.exports = nextConfig
