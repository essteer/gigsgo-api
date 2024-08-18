/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/templates/**/*.{html, jinja}"],
  theme: {
    extend: {},
    fontFamily: {
      notoSerif: ["Noto Serif"],
      oswald: ["Oswald"],
    }
  },
  plugins: [],
};
