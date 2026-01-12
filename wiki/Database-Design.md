# 🗄️ Database Design: AstralytiQ

AstralytiQ utilizes a hybrid data approach, leveraging both local SQLite for rapid development and PostgreSQL (via Supabase) for production enterprise environments.

## 🗺️ Schema Overview

### 1. Users & Authentication
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `email` | String | Unique Identifier |
| `hashed_password` | String | Bcrypt hash |
| `role` | Enum | `admin`, `data_scientist`, `analyst` |
| `department` | String | User organization unit |

### 2. Datasets
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `name` | String | Dataset Label |
| `storage_uri` | String | Cloud Storage/Local Path |
| `quality_score` | Float | Calculated 0.0-1.0 |
| `meta_features` | JSONB | Column types, row counts, etc. |

### 3. ML Models
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `version` | String | SemVer (e.g., 1.0.4) |
| `model_type` | String | `Prophet`, `XGBoost`, etc. |
| `metrics` | JSONB | Accuracy, F1, MAPE |
| `status` | String | `training`, `deployed`, `archived` |

## 🔄 Migrations
We use **Alembic** for managing production database migrations to ensure schema consistency across environments.
