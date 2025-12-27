import { defineConfig } from 'vite'

export default defineConfig({
    server: {
        host: true, // Already set by CLI, but good to be explicit
        allowedHosts: [
            'tonilogar.com',
            'www.tonilogar.com',
            'localhost'
        ]
    }
})
