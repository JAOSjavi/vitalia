import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

// En local las pantallas piden a su propio origen y Vite reenvía a la API.
const API_LOCAL = "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { "/api": API_LOCAL },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/pruebas.ts",
  },
});
