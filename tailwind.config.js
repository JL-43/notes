module.exports = {
  content: [
    "./utils/**/*.py",
    "./**/*.html",
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            'th': {
              padding: '0.75rem',
              borderWidth: '1px',
              borderColor: '#e5e7eb',
            },
            'td': {
              padding: '0.75rem',
              borderWidth: '1px',
              borderColor: '#e5e7eb',
            },
            'table': {
              borderCollapse: 'collapse',
              width: '100%',
            }
          }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography')
  ]
}