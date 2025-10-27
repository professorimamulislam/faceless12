/***** Tailwind config for Next.js app router *****/
module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,jsx,ts,tsx}',
    './components/**/*.{js,jsx,ts,tsx}',
    './pages/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#6366f1',
          600: '#5b5ee5',
          700: '#4f51d7'
        }
      }
    },
  },
  plugins: [],
}
