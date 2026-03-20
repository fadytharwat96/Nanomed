# Nanomed - MVP Backend

FastAPI backend for Nanomed with modular structure, SQLAlchemy persistence, placeholder OTP auth, JWT access tokens, and role-based route protection.

## Project structure
```text
backend/app/
  core/        # security + dependencies (current user / RBAC)
  db/          # SQLAlchemy base + session
  models/      # ORM models
  routers/     # API route groups
  schemas/     # Pydantic schemas
  services/    # business logic
```

## Features implemented
- SQLAlchemy persistent storage (`DATABASE_URL` configurable)
- OTP placeholder flow (`send-otp`, `verify-otp`)
- JWT access tokens (HMAC-SHA256)
- Role-based access control (`patient`, `nurse`, `admin`)
- Current user dependency (`/v1/auth/me`)
- Protected profile/request endpoints using authenticated user context
- Nurse request lifecycle endpoints (`arrive`, `start`, `complete`, `reject`)
- Existing dispatch behavior preserved (nearest online nurse assignment)

## API endpoints
### Health
- `GET /health`

### Auth
- `POST /v1/auth/send-otp`
- `POST /v1/auth/verify-otp`
- `GET /v1/auth/me`

### Profiles (protected: patient/admin)
- `POST /v1/profiles`
- `GET /v1/profiles`

### Nurses (protected: patient/nurse/admin)
- `GET /v1/nurses/online`

### Requests (protected: patient/admin)
- `POST /v1/requests`
- `GET /v1/requests/{request_id}`

### Nurse Lifecycle (protected: nurse/admin)
- `GET /v1/nurse/requests`
- `POST /v1/nurse/requests/{request_id}/arrive`
- `POST /v1/nurse/requests/{request_id}/start`
- `POST /v1/nurse/requests/{request_id}/complete`
- `POST /v1/nurse/requests/{request_id}/reject`

## Run locally
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open docs: `http://127.0.0.1:8000/docs`

## Environment variables
- `DATABASE_URL` (default: `sqlite:///./nanomed.db`)
- `SECRET_KEY` (default: `nanomed-dev-secret`)
- `ACCESS_TOKEN_EXPIRE_SECONDS` (default: `86400`)

## Seed users
- Admin: phone `0000000000`, role `admin`
- Nurse Aya: phone `01111111111`, role `nurse`
- Nurse Mariam: phone `02222222222`, role `nurse`

## Tests
```bash
cd backend
pytest -q
```

> Note: OTP is placeholder-only for now and always issues code `123456` for development/testing.
