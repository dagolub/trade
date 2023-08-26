import './src/css/tailwind.config.js'
import 'autoprefixer'
import 'tailwindcss'
import autoprefixer
import tailwind
import tailwindConfig

export default {
  plugins: [tailwind(tailwindConfig), autoprefixer],
}