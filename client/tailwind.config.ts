import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'blue': {
          '800': '#074685',
          '950': '#082549',
        },
        'white': {
          '50': '#FFFFFF',
          '100': '#E4E6E9',
        },
        'red': {
          '500': '#FF3232',
        },
        'gray': {
          '700': '#494F55',
        }
      },
    },
  },
  plugins: [],
} satisfies Config;
