import { defineConfig, loadEnv } from "vite";
import path from "path";
import dotenv from "dotenv";
import react from "@vitejs/plugin-react";

dotenv.config({ path: "../.env" }); // load env vars from .env

// https://vitejs.dev/config/
export default defineConfig(({ _, mode }) => {
  // Load environment variables based on the current mode.
  const env = { ...process.env, ...loadEnv(mode, process.cwd()) };

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: true,
      port: env.VITE_APP_PORT,
      strictPort: true,
      proxy: {
        "/api": {
          target: env.VITE_DEV_API_URL, // Your actual API URL for development
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""), // Remove '/api' from the path when forwarding
        },
      },
    },
    preview: {
      port: env.VITE_APP_PORT,
    },
  };
});
