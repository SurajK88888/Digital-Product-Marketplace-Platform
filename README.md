# Digital Product Marketplace Platform

> Enterprise-grade, multi-vendor marketplace for digital products — themes, plugins, scripts, templates, e-books, and licensed software.

[![CI](https://github.com/your-org/digital-product-marketplace/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/digital-product-marketplace/actions/workflows/ci.yml)

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 15, React 19, TypeScript (strict), Tailwind CSS, Shadcn UI |
| **State** | Zustand, TanStack Query v5, Framer Motion |
| **Backend** | FastAPI, Python 3.12, SQLAlchemy (async), Alembic |
| **Database** | PostgreSQL 16 (primary), Redis 7 (cache/queue) |
| **Storage** | AWS S3 / Cloudflare R2 (private product vault) |
| **Auth** | JWT (RS256) + HttpOnly refresh tokens + 2FA (TOTP) |
| **Payments** | Stripe Payment Intents + Webhooks |
| **DevOps** | Docker, Kubernetes (EKS), Terraform, GitHub Actions |
| **Observability** | OpenTelemetry, Sentry, Prometheus, Loguru |

---

## Project Structure

```
digital-product-marketplace/
├── apps/
│   ├── frontend/          # Next.js 15 App Router web application
│   └── backend/           # FastAPI async REST API
├── packages/
│   ├── shared-types/      # Cross-stack TypeScript types
│   ├── shared-utils/      # Shared utility functions
│   └── design-system/     # Reusable UI component library
├── infrastructure/
│   ├── docker/            # Dockerfiles & Docker Compose
│   ├── k8s/               # Kubernetes manifests
│   └── terraform/         # Infrastructure as Code
├── docs/                  # API docs, architecture diagrams, runbooks
└── .github/workflows/     # CI/CD pipelines
```

---

## Prerequisites

Ensure you have the following installed:

- **Node.js** ≥ 20.0.0
- **npm** ≥ 10.0.0
- **Python** ≥ 3.12
- **Docker** + **Docker Compose** v2+
- **Git**

---

## Quick Start (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/your-org/digital-product-marketplace.git
cd digital-product-marketplace
```

### 2. Configure environment variables

```bash
# Root environment (frontend + Docker Compose)
cp .env.example .env

# Backend environment
cp apps/backend/.env.example apps/backend/.env
```

Edit `.env` and `apps/backend/.env` with your local values.

### 3. Start the full stack with Docker Compose

```bash
docker compose -f infrastructure/docker/docker-compose.dev.yml up
```

Services available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/api/docs
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

### 4. Local development (without Docker)

#### Frontend

```bash
npm install          # Install all workspace dependencies
npm run dev:frontend # Start Next.js dev server with Turbopack
```

#### Backend

```bash
cd apps/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start FastAPI dev server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Running Tests

### Frontend

```bash
npm run type-check   # TypeScript type-checking
npm run lint         # ESLint
npm run format:check # Prettier check
```

### Backend

```bash
cd apps/backend

# Lint & format
ruff check .
ruff format --check .

# Type-check
mypy app/

# Unit + integration tests
pytest --cov=app --cov-report=term-missing -v
```

---

## Database Migrations

```bash
cd apps/backend

# Create a new migration (after modifying SQLAlchemy models)
alembic revision --autogenerate -m "add_users_table"

# Apply all pending migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1

# View migration history
alembic history
```

---

## Code Quality Standards

This project enforces strict code quality via pre-commit hooks (Husky):

- **Conventional Commits** — all commit messages must follow `type(scope): subject` format
- **ESLint** — zero tolerance for TypeScript `any`, unused variables, or import ordering violations
- **Ruff** — Python linting and formatting (replaces Flake8 + isort + Black)
- **Mypy** — strict Python type checking

```bash
# Install pre-commit hooks after cloning
npm install        # Installs Husky hooks automatically via `prepare` script
```

---

## Environment Variables

All environment variables are documented in:
- [`.env.example`](./.env.example) — Root (frontend + Docker)
- [`apps/backend/.env.example`](./apps/backend/.env.example) — Backend

> ⚠️ **Never commit `.env` files.** They are excluded via `.gitignore`.

---

## Architecture

For the complete Phase 0 architecture blueprint, refer to:
- [`.agents/memory/long_term_memory.md`](./.agents/memory/long_term_memory.md)
- [`docs/architecture/overview.md`](./docs/architecture/overview.md)

---

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit using Conventional Commits: `git commit -m "feat(auth): add TOTP 2FA verification"`
3. Push and open a Pull Request against `develop`
4. Ensure all CI checks pass before requesting review

---

## License

Proprietary — All rights reserved.
