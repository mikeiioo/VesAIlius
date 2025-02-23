/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  plugins: [],
  // ...existing configuration...
  theme: {
    extend: {
      colors: {
        gray: {
          //850: '#182434', // Custom gray color
          850: '#253141',
        },
      },
    },
  },
  // ...existing configuration...
}

