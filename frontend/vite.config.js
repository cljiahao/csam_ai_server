import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load environment variables based on the current mode

  const env = { ...process.env, ...loadEnv(mode, process.cwd(), "") };
  console.log(env.VITE_API_PATH);

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: true,
      port: env.APP_PORT || 3000,
      strictPort: true,
      open: true, // Automatically open the app in the browser
      proxy: {
        "/api": {
          target: env.API_PATH || "http://localhost:8000",
          changeOrigin: true,
          secure: false,
        },
      },
    },
    preview: {
      port: env.APP_PORT || 5173,
      open: true, // Automatically open the preview in the browser
      proxy: {
        "/api": {
          target: env.API_PATH || "http://localhost:5000",
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
});
