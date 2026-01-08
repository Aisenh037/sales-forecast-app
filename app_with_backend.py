"""
⚡ AstralytiQ: Enterprise MLOps Platform with Backend Integration
Industry-grade MLOps platform with FastAPI backend integration

Perfect for SDE/DE Campus Placements - Demonstrates:
- Full-stack development (Streamlit + FastAPI)
- JWT authentication and authorization
- Real-time API integration
- Database connectivity
- WebSocket real-time updates
- Production-ready architecture
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Import backend integration
from backend_integration import (
    enhanced_login_form, is_authenticated, get_current_user, logout_user,
    show_backend_status, show_api_documentation, setup_auto_refresh,
    show_real_time_metrics, get_cached_datasets, get_cached_models,
    get_cached_metrics, check_backend_connection
)

# Configuration
st.set_page_config(
    page_title="AstralytiQ - Enterprise MLOps Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with backend integration styling
st.markdown("""
<style>
    /* Modern Enterprise Theme */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .enterprise-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .enterprise-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .enterprise-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .backend-status {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .backend-offline {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .api-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 1rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .metric-card h3 {
        color: #2d3748;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    
    .metric-card h2 {
        color: #667eea;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-card p {
        color: #718096;
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }
    
    .auth-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-success {
        background: #c6f6d5;
        color: #22543d;
    }
    
    .status-warning {
        background: #fef5e7;
        color: #744210;
    }
    
    .status-info {
        background: #bee3f8;
        color: #2a4365;
    }
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .enterprise-header h1 {
            font-size: 2rem;
        }
        
        .enterprise-header p {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem;
            margin: 0.5rem 0;
        }
        
        .metric-card h2 {
            font-size: 2rem;
        }
        
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .auth-card {
            padding: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def show_backend_integration_dashboard():
    """Enhanced dashboard with backend integration."""
    st.markdown("""
    <div class="enterprise-header">
        <h1>📊 Enterprise Dashboard</h1>
        <p>Real-time MLOps Metrics with Backend Integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend status indicator
    if check_backend_connection():
        st.markdown("""
        <div class="backend-status">
            <h3>🟢 Backend Connected</h3>
            <p>Real-time data from FastAPI backend • JWT Authentication Active • Database Operational</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="backend-status backend-offline">
            <h3>🟡 Demo Mode</h3>
            <p>Backend offline • Using cached demo data • Start backend for full functionality</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Setup auto-refresh
    setup_auto_refresh()
    
    # Real-time metrics from backend
    st.markdown("## 📈 Real-time Metrics")
    show_real_time_metrics()
    
    # Backend data integration
    st.markdown("## 🗄️ Backend Data Integration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Datasets from Backend")
        datasets = get_cached_datasets()
        
        if datasets:
            df = pd.DataFrame(datasets)
            st.dataframe(
                df[['name', 'type', 'status', 'rows', 'columns']].head(5),
                use_container_width=True
            )
            st.info(f"✅ Loaded {len(datasets)} datasets from backend API")
        else:
            st.warning("⚠️ No datasets available from backend")
    
    with col2:
        st.markdown("### 🤖 ML Models from Backend")
        models = get_cached_models()
        
        if models:
            df = pd.DataFrame(models)
            st.dataframe(
                df[['name', 'type', 'status', 'accuracy']].head(5),
                use_container_width=True
            )
            st.info(f"✅ Loaded {len(models)} models from backend API")
        else:
            st.warning("⚠️ No models available from backend")
    
    # API Integration Demo
    st.markdown("## 🔗 API Integration Demo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            # Clear cache and refresh
            get_cached_datasets.clear()
            get_cached_models.clear()
            get_cached_metrics.clear()
            st.success("✅ Data refreshed from backend!")
            st.rerun()
    
    with col2:
        if st.button("📊 Test API", use_container_width=True):
            with st.spinner("Testing API endpoints..."):
                time.sleep(1)
                if check_backend_connection():
                    st.success("✅ All API endpoints responding")
                else:
                    st.error("❌ Backend connection failed")
    
    with col3:
        if st.button("🔍 View Logs", use_container_width=True):
            st.info("📋 Check backend logs at http://localhost:8081/health/detailed")
    
    # Real-time visualizations
    st.markdown("## 📈 Real-time Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Real-time metrics chart
        if models:
            model_df = pd.DataFrame(models)
            if 'accuracy' in model_df.columns and 'type' in model_df.columns:
                fig = px.bar(
                    model_df.groupby('type')['accuracy'].mean().reset_index(),
                    x='type',
                    y='accuracy',
                    title="Model Accuracy by Type (Backend Data)",
                    color_discrete_sequence=['#667eea']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Dataset status distribution
        if datasets:
            dataset_df = pd.DataFrame(datasets)
            if 'status' in dataset_df.columns:
                status_counts = dataset_df['status'].value_counts()
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Dataset Status Distribution (Backend Data)",
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Inter, sans-serif")
                )
                st.plotly_chart(fig, use_container_width=True)

def show_user_profile_with_backend():
    """Enhanced user profile with backend integration."""
    user = get_current_user()
    
    if user:
        st.sidebar.markdown("### 👤 User Profile")
        
        # Professional avatar
        avatar_letter = user['name'][0].upper()
        st.sidebar.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="
                width: 60px; 
                height: 60px; 
                border-radius: 50%; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                display: flex; 
                align-items: center; 
                justify-content: center; 
                margin: 0 auto; 
                color: white; 
                font-size: 24px; 
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            ">
                {avatar_letter}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown(f"**{user['name']}**")
        st.sidebar.markdown(f"*{user['role']}*")
        st.sidebar.markdown(f"📧 {user['email']}")
        if user.get('department'):
            st.sidebar.markdown(f"🏢 {user['department']}")
        
        # Authentication status
        if is_authenticated():
            st.sidebar.markdown("🔐 **Authenticated via Backend**")
            st.sidebar.markdown("✅ JWT Token Active")
        else:
            st.sidebar.markdown("🔓 **Demo Mode**")
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.success("Logged out successfully!")
            st.rerun()

def show_navigation_with_backend():
    """Enhanced navigation with backend integration."""
    st.sidebar.markdown("### 🧭 Navigation")
    
    nav_options = [
        "📊 Enterprise Dashboard",
        "🔗 Backend Integration", 
        "🤖 ML Operations",
        "📈 Analytics & BI",
        "🔧 Data Engineering",
        "🔒 Security & Compliance"
    ]
    
    selected = st.sidebar.selectbox("Navigate to:", nav_options)
    
    # Backend status in sidebar
    show_backend_status()
    
    # API documentation links
    show_api_documentation()
    
    return selected

def show_backend_integration_page():
    """Dedicated page for backend integration demo."""
    st.markdown("""
    <div class="enterprise-header">
        <h1>🔗 Backend Integration</h1>
        <p>FastAPI Backend Integration Showcase</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Backend connection status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 FastAPI Backend")
        
        if check_backend_connection():
            st.markdown("""
            <div class="api-card">
                <h4>✅ Backend Online</h4>
                <p><strong>URL:</strong> http://localhost:8081</p>
                <p><strong>Status:</strong> Healthy</p>
                <p><strong>Authentication:</strong> JWT Active</p>
                <p><strong>Database:</strong> SQLite Connected</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="api-card">
                <h4>❌ Backend Offline</h4>
                <p><strong>Status:</strong> Connection Failed</p>
                <p><strong>Mode:</strong> Demo Mode Active</p>
                <p><strong>Action:</strong> Start backend server</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📚 API Documentation")
        
        st.markdown("""
        <div class="api-card">
            <h4>📖 Available Endpoints</h4>
            <p><strong>Swagger UI:</strong> <a href="http://localhost:8081/docs" target="_blank">/docs</a></p>
            <p><strong>ReDoc:</strong> <a href="http://localhost:8081/redoc" target="_blank">/redoc</a></p>
            <p><strong>Health Check:</strong> <a href="http://localhost:8081/health" target="_blank">/health</a></p>
            <p><strong>OpenAPI JSON:</strong> <a href="http://localhost:8081/openapi.json" target="_blank">/openapi.json</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    # API Endpoints Demo
    st.markdown("## 🔌 API Endpoints Demo")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Authentication", "Datasets", "ML Models", "Metrics"])
    
    with tab1:
        st.markdown("### 🔐 Authentication API")
        st.code("""
POST /api/v1/auth/login
{
  "email": "admin@astralytiq.com",
  "password": "admin123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "admin@astralytiq.com",
    "name": "System Administrator",
    "role": "Platform Admin"
  }
}
        """, language="json")
    
    with tab2:
        st.markdown("### 📊 Datasets API")
        st.code("""
GET /api/v1/datasets
Authorization: Bearer <token>

Response:
[
  {
    "id": "ds_001",
    "name": "Customer Analytics Dataset 1",
    "type": "CSV",
    "size_mb": 1250,
    "rows": 500000,
    "columns": 25,
    "status": "Active",
    "quality_score": 0.95
  }
]
        """, language="json")
    
    with tab3:
        st.markdown("### 🤖 ML Models API")
        st.code("""
GET /api/v1/models
Authorization: Bearer <token>

Response:
[
  {
    "id": "ml_001",
    "name": "Deep Learning Model v2.1",
    "type": "Deep Learning",
    "accuracy": 0.94,
    "precision_score": 0.92,
    "recall_score": 0.89,
    "f1_score": 0.90,
    "status": "Deployed"
  }
]
        """, language="json")
    
    with tab4:
        st.markdown("### 📈 Metrics API")
        st.code("""
GET /api/v1/metrics
Authorization: Bearer <token>

Response:
{
  "total_datasets": 15,
  "active_models": 8,
  "total_dashboards": 6,
  "data_processed_tb": 45.7,
  "api_calls_today": 125847,
  "uptime_percentage": 99.97,
  "active_users": 1247
}
        """, language="json")
    
    # Backend Setup Instructions
    st.markdown("## 🛠️ Backend Setup Instructions")
    
    st.markdown("""
    ### Quick Start
    
    1. **Install Dependencies**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```
    
    2. **Start Backend Server**
    ```bash
    python main.py
    ```
    
    3. **Access API Documentation**
    - Swagger UI: http://localhost:8081/docs
    - ReDoc: http://localhost:8081/redoc
    
    4. **Test Authentication**
    ```bash
    curl -X POST "http://localhost:8081/api/v1/auth/login" \\
         -H "Content-Type: application/json" \\
         -d '{"email": "admin@astralytiq.com", "password": "admin123"}'
    ```
    """)

def main():
    """Main application with backend integration."""
    if not is_authenticated():
        enhanced_login_form()
        return
    
    # User profile with backend integration
    show_user_profile_with_backend()
    
    # Navigation with backend integration
    selected_page = show_navigation_with_backend()
    
    # Route to pages
    if "Dashboard" in selected_page:
        show_backend_integration_dashboard()
    elif "Backend Integration" in selected_page:
        show_backend_integration_page()
    elif "ML Operations" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>🤖 ML Operations Center</h1>
            <p>Model Training, Deployment & Monitoring with Backend Integration</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 ML Operations interface with backend integration coming in Phase 3")
    elif "Analytics" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>📈 Business Intelligence</h1>
            <p>Advanced Analytics & Reporting with Real-time Backend Data</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 BI Analytics interface with backend integration coming in Phase 3")
    elif "Data Engineering" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>🔧 Data Engineering</h1>
            <p>ETL Pipelines & Data Processing with Backend APIs</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 Data Engineering interface with backend integration coming in Phase 3")
    else:
        st.markdown("""
        <div class="enterprise-header">
            <h1>🔒 Security & Compliance</h1>
            <p>Access Control & Audit Management with JWT Authentication</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 Security interface with enhanced backend authentication coming in Phase 4")

if __name__ == "__main__":
    main()