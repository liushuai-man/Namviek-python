/**
 * @type {import('next').NextConfig}
 **/
const nextConfig = {
  output: 'standalone',
  webpack: config => {
    config.resolve.alias.canvas = false
    // Redirect @prisma/client to our runtime shim
    config.resolve.alias['@prisma/client'] = require('path').resolve(
      __dirname,
      'lib/prisma-shim.js'
    )
    config.resolve.alias['.prisma/client'] = require('path').resolve(
      __dirname,
      'lib/prisma-shim.js'
    )
    return config
  }
}

module.exports = nextConfig
