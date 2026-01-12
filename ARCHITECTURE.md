# 🏗️ Technical Architecture: AstralytiQ

This document provides a detailed overview of the technical design, architectural patterns, and system components of AstralytiQ.

## 📐 Design Philosophy

AstralytiQ is built on three core pillars:
1.  **Decoupling**: Separation of concerns between the Presentation Layer (Streamlit) and the Business Logic/ML Layer (FastAPI).
2.  **Scalability**: Stateless backend design allowing Horizontal Pod Autoscaling (HPA) in Kubernetes environments.
3.  **Observability**: Integrated monitoring for both system resources and ML model health.

---

## 🏗️ System Components

### 1. Presentation Layer (Streamlit)
The frontend is a highly customized Streamlit application.
-   **Styling**: Uses custom CSS injection for an enterprise-grade "Glassmorphism" look.
-   **State Management**: Leverages `st.session_state` for local caching and user session persistence.
-   **Security**: Implements client-side route protection and JWT storage.

### 2. API Gateway & Backend (FastAPI)
The central nervous system of the platform.
-   **Asynchronous I/O**: High-performance request handling using `async/await`.
-   **Type Safety**: Strictly enforced Pydantic models for all request/response schemas.
-   **Integrations**: 
    -   **Supabase**: Managed PostgreSQL for persistent storage and auth.
    -   **Cloudinary**: CDN for optimized image and asset delivery.

### 3. Forecasting Engine (ML Service)
A specialized service for generating predictions.
-   **Models**: Implements a mix of classical Statistical models (Prophet, ARIMA) and Modern Regressors.
-   **Pipelines**: Standardized pre-processing for time-series cleaning and feature engineering.

---

## 🔐 Security & Authentication

AstralytiQ implements a standard SaaS security model:
-   **JWT (JSON Web Tokens)**: Secure, signed tokens for all cross-service communication.
-   **Bcrypt Hashing**: Passwords never stored in plain text.
-   **TLS/SSL**: All production traffic is encrypted (managed via Nginx/Cloud Load Balancers).

---

## 🚢 Deployment & CI/CD

The platform supports a "Build Once, Deploy Anywhere" philosophy:

### Containerization
-   **Multi-stage Dockerfiles**: Optimized images for production (significantly reduced size).
-   **Docker Compose**: Orchestrates the DB, Backend, and Frontend for local development.

### Cloud Integration
-   **GCP**: `cloudbuild.yaml` for automated deployments to Google Cloud Run.
-   **Azure**: `azure-pipelines.yml` for CI/CD.
-   **Render**: `render.yaml` for quick staging deployments.

---

## 📊 Performance Metrics

-   **API Latency**: Target < 200ms for standard queries.
-   **Cold Starts**: Optimized through container pre-warming and lightweight base images.
-   **Memory Footprint**: Frontend <150MB, Backend <100MB per instance.
