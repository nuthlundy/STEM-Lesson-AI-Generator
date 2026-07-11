# Development Adapter

This directory contains the Express + Vite adapter used exclusively for running the application in the Google AI Studio development environment, where only port 3000 is exposed to the internet.

## Migration Path to Production Architecture

In production (as specified by `19_PROJECT_STRUCTURE.md`), the application is meant to be served using:
- **Frontend**: Next.js 15 (Currently mocked by Vite + React for rapid preview in this environment)
- **Backend**: Python FastAPI service running independently on a separate port or container (e.g., port 8000).

To migrate to the full production architecture:
1. Replace `adapter/server.ts` with a standard production ingress/reverse proxy (like Nginx) or rely on cloud load balancing.
2. Run the frontend statically or via standard Next.js `npm run start`.
3. Run the Python backend independently via `uvicorn backend.main:app --host 0.0.0.0 --port 8000`.

The `adapter/server.ts` here simply:
1. Hosts the frontend static files/Vite HMR.
2. Spawns the Python FastAPI backend as a child process on port 8000.
3. Proxies all `/api/*` requests to the Python backend to ensure correct full-stack development functionality in a single-port environment.
