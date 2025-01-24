import { defineConfig, loadEnv } from "vite";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import react from "@vitejs/plugin-react";
import process from "process";
import dotenv from "dotenv";

dotenv.config({ path: "../.env" });

// Utility for ESM compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load environment variables based on the current mode.
  const env = loadEnv(mode, process.cwd());

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": resolve(__dirname, "./src"),
      },
    },
    server: {
      host: true,
      port: parseInt(env.VITE_APP_PORT) || 3000,
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
      port: parseInt(env.VITE_APP_PORT) || 5000,
    },
  };
});
