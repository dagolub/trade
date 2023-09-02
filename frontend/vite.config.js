import {defineConfig} from 'vite'
import postcss from './postcss.config.js'
import react from '@vitejs/plugin-react'

export default defineConfig({
    server: {
        proxy: {
            '/websocket': {
                target: 'ws://localhost:3000', // WebSocket server address
                changeOrigin: true,
                ws: true,
            },
        },
        hmr:{
            port: 3000
        }
    },
    define: {
        'process.en': process.env
    },
    css: {
        postcss
    },
    plugins: [react()],
    resolve: {
        alias: [
            {
                find: /^~.+/,
                replacement: (val) => {
                    return val.replace(/^~/, "")
                }
            }
        ]
    },
    build: {
        commonjsOptions: {
            transformMixedEsModules: true
        }
    }
})