import postcss from 'postcss'; // Import postcss properly
import react from '@vitejs/plugin-react'; // Import the react plugin properly
import {defineConfig} from 'vite'; // Import defineConfig from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
    define: {
        'process.env': process.env
    },
    css: {
        postcss: {} // You can add postcss plugins and options here
    },
    plugins: [react()], // Use the react plugin as an array
    resolve: {
        alias: [
            {
                find: /^~.+/,
                replacement: (val) => {
                    return val.replace(/^~/, "");
                },
            },
        ],
    },
    build: {
        commonjsOptions: {
            transformMixedEsModules: true,
        }
    }
});