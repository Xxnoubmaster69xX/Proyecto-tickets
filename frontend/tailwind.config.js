/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: ['class', '[data-theme="dark"]'], // In case we want to use 'dark:' variant
  theme: {
    extend: {
      colors: {
        background: 'var(--bg-color)',
        surface: 'var(--surface-color)',
        surfaceLight: 'var(--surface-light-color)',
        primary: 'var(--primary-color)',
        primaryHover: 'var(--primary-hover)',
        accent: 'var(--gold-color)',
        textPrimary: 'var(--text-primary)',
        textSecondary: 'var(--text-secondary)',
        borderTheme: 'var(--border-color)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'Avenir', 'Helvetica', 'Arial', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
