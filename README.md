# Mindit Backend Deployment Guide

## 1. Environment Variables
You need to set the following secrets in Koyeb (or your `.env` file for local dev):

- **DATABASE_URL**: Must be the **Transaction Pooler** URL (Port 6543) from Supabase.
  - Go to Supabase -> Database -> Connection Pooling.
  - Copy the URI and replace `[password]`.
  - Ensure it starts with `postgresql+asyncpg://` (you might need to change `postgres://` manually).
  - Ensure `?pgbouncer=true` is at the end.

- **SUPABASE_JWT_SECRET**:
  - Go to Supabase -> Project Settings -> API.
  - Copy the `JWT Secret`.

- **GOOGLE_API_KEY**:
  - Your Gemini API Key.

## 2. Local Testing (Docker)

```bash
# Build
docker build -t mindit-backend .

# Run (Make sure .env exists with real values)
docker run --env-file .env -p 8000:8000 mindit-backend
```

## 3. Deployment to Koyeb

1. **Create App**: Connect your GitHub repo.
2. **Build Settings**:
   - Dockerfile: `mindit-backend/Dockerfile`
3. **Environment Variables**:
   - Add the variables from Step 1.
4. **Expose Port**: 8000 (HTTP).

## 4. Verification

- Visit `https://<your-app>.koyeb.app/` -> Should see `{"status": "ok", ...}`.
- Test `/ingest/url` with a JWT token.
