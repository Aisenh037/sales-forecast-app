# 🐳 Docker Strategy: Enterprise Deployment

AstralytiQ utilizes a multi-container architecture orchestrated via Docker Compose, ensuring identical behavior across development, staging, and production.

## 🏗️ Docker Architecture

### 1. Multi-Stage Builds
We use multi-stage builds to keep production images lightweight (<300MB):
- **Stage 1 (Builder)**: Installs build-essential, compiles C-extensions.
- **Stage 2 (Production)**: Copies only the site-packages and app code.

### 2. Service Definitions

| Service | Port | Description |
| :--- | :--- | :--- |
| `frontend` | `8501` | Streamlit Dashboard |
| `backend` | `8000` | FastAPI Forecasting Engine |
| `db` | `5432` | PostgreSQL (Development only) |
| `nginx` | `80/443` | Reverse Proxy & SSL Termination |

## 🚀 Running the Stack

### Developer Mode
```bash
docker-compose --profile dev up -d
```

### Production Mode
```bash
docker-compose --profile prod up -d --build
```

## 🔒 Security
- Images are scanned via **Trivy** in the CI pipeline.
- Containers run as non-root users (`uid 1000`).
- Sensitive keys are passed via `.env` or Docker Secrets.
