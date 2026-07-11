import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { spawn } from "child_process";
import { createProxyMiddleware } from "http-proxy-middleware";

async function startServer() {
  const app = express();
  const PORT = 3000;
  
  // Spawn Python FastAPI Backend on port 8000
  const pythonProcess = spawn("python3", ["-m", "venv", "venv"], { cwd: process.cwd() });
  
  // Actually, we should just run the python script directly if dependencies are installed globally, 
  // or use the venv if we set it up. Since we're in a container, let's just run it globally or inside the venv if created.
  // We'll wrap the startup in a shell script for simplicity, or just spawn uvicorn.
  
  // Let's spawn uvicorn directly if it's installed, or use python3 -m uvicorn
  const uvicornProcess = spawn("python3", ["-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"], {
    cwd: process.cwd(),
    stdio: "inherit",
    env: { ...process.env, PYTHONPATH: path.join(process.cwd(), "backend") }
  });

  uvicornProcess.on('error', (err) => {
    console.error('Failed to start Python backend:', err);
  });

  // Proxy API requests to the Python backend
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://127.0.0.1:8000",
      changeOrigin: true,
      ws: true,
    })
  );

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
  
  // Cleanup child process on exit
  process.on('SIGTERM', () => uvicornProcess.kill());
  process.on('SIGINT', () => uvicornProcess.kill());
}

startServer();
