/** @type {import('tailwindcss').Config} */

export default {

    content: [
        "../backend/templates/**/*.html",
        "./src/js/**/*.js",
    ],

    theme: {

        extend: {

          colors: {

            primary: '#191654',
            accent: '#fc9e49',
            surface: '#f8f5f0',
            dark: '#0f1020',

          },

          fontFamily: {
            futura: ['Futura PT', 'sans-serif'],
          },
        },
    },
    plugins: [],
}