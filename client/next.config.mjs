/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  source: '/api/proxy/:path*',

  destination: `${process.env.BACKEND_URL || 'http://localhost:8000'}/:path*`,
}

export default nextConfig
