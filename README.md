# chat-backend

---

A real-time chat API. Think mini WhatsApp.

---

## What it does

Sign up, log in, create rooms for different groups of people — your gaming friends, your dev colleagues, whoever — and chat with them in real time. Messages broadcast instantly to everyone in the room and get saved to the database. No refresh needed.

---

## Tech Stack

FastAPI · PostgreSQL · SQLAlchemy 2.0 · WebSockets · Docker · Alembic · JWT Auth · bcrypt · GitHub Actions · Render ·
NGINX · Redis 
---

## Features

- Real-time messaging via WebSockets with per-room connection management
- JWT authentication with protected routes
- Full CRUD for users, rooms, and messages
- Query parameters — filter, limit, skip, search
- Alembic migrations for schema versioning
- 19 pytest tests with a dedicated test database
- NGINX reverse proxy — single controlled entry point, app port never exposed directly
- Redis pub/sub for WebSocket scaling — messages broadcast across multiple server instances, not just local connections
- Redis fallback — app stays live if Redis goes down, falls back to direct broadcast automatically
- Structured JSON logging and observability — request tracing, user activity, and error tracking across all routers and WebSocket connections
- CI/CD — GitHub Actions runs tests, builds Docker image, pushes to DockerHub, deploys to Render automatically
- Live on Render
  

---

## Run it locally

```bash
docker-compose up --build
```

---

## Live API

https://chat-backend-latest-axii.onrender.com

Hit `/docs` for Swagger UI — FastAPI's built-in interactive API explorer.

---

## What's next

Next: engineering tradeoffs, failure cases, and scaling decisions.
