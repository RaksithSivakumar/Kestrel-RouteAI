/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        kestrel: {
          ink: "#1b2430",
          navy: "#1f4e79",
          copper: "#c45c26",
          paper: "#f4f1ea",
          line: "#d8d2c8",
        },
      },
      fontFamily: {
        sans: ["Georgia", "ui-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
