/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/index.html",
        "./src/tos.html",
        "./src/privacy.html",
        "./src/js/**/*.js",
        "./src/img/bubble.svg",
        "./src/img/times.svg"
    ],
    theme: {
        extend: {
            spacing: {
                'chat-sm': '30rem',
                'chat-md': '60rem',
            }
        },
    },
    safelist: [
        'w-12',
        'h-12',
    ],
    plugins: [
        require("daisyui"),
        // https://github.com/tailwindlabs/tailwindcss-forms
        require('@tailwindcss/forms'),
        // https://github.com/tailwindlabs/tailwindcss-typography
        require("@tailwindcss/typography")
    ],
}
