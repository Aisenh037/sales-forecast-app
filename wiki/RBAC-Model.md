# 🔐 RBAC Model: Role-Based Access Control

AstralytiQ enforces Enterprise-grade security through strict role-based segmentation. This ensures that users only access features and data appropriate for their organizational function.

## 👥 Role Definitions

### 1. 🛡️ System Administrator (`admin`)
- **Control**: Full platform access.
- **Capabilities**: 
  - Manage user accounts and roles.
  - View billing and cloud infrastructure metrics.
  - Override model deployments.
  - Access system logs and audit trails.

### 2. 🧪 Data Scientist (`data_scientist`)
- **Control**: ML Lifecycle management.
- **Capabilities**:
  - Upload and preprocess datasets.
  - Initiate model training jobs.
  - Compare model versions and performance.
  - Deploy models to staging/production.

### 3. 📊 Business Analyst (`analyst`)
- **Control**: Read-only business intelligence.
- **Capabilities**:
  - View executive dashboards and sales forecasts.
  - Export PDF/CSV reports.
  - View data quality summaries (cannot modify data).

## 🔒 Implementation
Permissions are checked at the **API Gateway Layer** (FastAPI) using JWT scopes. The Streamlit frontend dynamically hides/shows UI components based on the `session_state['user']['role']`.
