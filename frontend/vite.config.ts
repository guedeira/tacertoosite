import { resolve } from "node:path";

import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  plugins: [vue()],
  build: {
    outDir: "../docs",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        scams: resolve(__dirname, "golpes/index.html"),
        terms: resolve(__dirname, "politicas/termos-de-uso.html"),
      },
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "https://api-tacertoosite.guedeira.dev",
        // target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
  },
});
