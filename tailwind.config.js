/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './cart/templates/**/*.html',  // Include all template files
    './cart/**/*.py',         // Include Python files (views, forms, etc.)
    "./cart/static/js/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

