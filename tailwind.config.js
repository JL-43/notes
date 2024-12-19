/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./utils/**/*.py",    // matches your Python template files
    "./**/*.html",        // matches generated HTML files
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/typography'), // for prose classes used in your HTML template
  ],
};