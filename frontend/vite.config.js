import { defineConfig, loadEnv } from "vite";
import path from "path";
import dotenv from "dotenv";
import react from "@vitejs/plugin-react";

// Load global .env variables
dotenv.config({ path: path.resolve(__dirname, "../.env") });

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
    define: {
      __API_URL__: JSON.stringify(
        `http://${env.PC_NAME}:${env.VITE_API_PORT}${env.FASTAPI_ROOT}/${env.FASTAPI_PREFIX}` ||
          "http://localhost:5000/api/v2",
      ),
    },
    server: {
      host: true,
      port: env.VITE_APP_PORT || 3000,
      strictPort: true,
    },
    preview: {
      port: env.VITE_APP_PORT || 5173,
    },
  };
});
