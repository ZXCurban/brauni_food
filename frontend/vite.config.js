import { defineConfig } from 'vite'

import path from 'path'

export default defineConfig({

    build: {

        outDir: path.resolve(
            __dirname,
            '../backend/static'
        ),

        emptyOutDir: false,

        rollupOptions: {

            input: {

                main: path.resolve(
                    __dirname,
                    'src/js/main.js'
                ),
            },

            output: {

                entryFileNames:
                    'js/[name].js',

                assetFileNames:
                    'css/[name][extname]',
            },
        },
    },
})