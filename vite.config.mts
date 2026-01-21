import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  root: "qianduan",
  plugins: [react()],
  server: {
    port: 5173
  },
  build: {
    outDir: "../dist"
  }
});

