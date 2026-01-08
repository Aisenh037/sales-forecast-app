"""
⚡ AstralytiQ: Enterprise MLOps Platform
Industry-grade MLOps platform showcasing enterprise development practices

Perfect for SDE/DE Campus Placements - Demonstrates:
- Clean Architecture & Design Patterns
- Production-Ready Code Quality
- Enterprise Security & Authentication
- Scalable System Design
- Modern DevOps Practices
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import time
from datetime import datetime, timedelta
import uuid
from typing import Dict, List, Optional, Any

# Configuration
st.set_page_config(
    page_title="AstralytiQ - Enterprise MLOps Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Demo mode configuration
DEMO_MODE = st.secrets.get("DEMO_MODE", "true").lower() == "true"

# Initialize production integrations with robust error handling
auth_manager = None
PRODUCTION_MODE = False

try:
    from auth_integrations import AuthManager
    auth_manager = AuthManager()
    status = auth_manager.get_integration_status()
    PRODUCTION_MODE = status.get("supabase", False) or status.get("cloudinary", False)
except Exception as e:
    # Graceful fallback - app continues to work without production integrations
    pass

# Enterprise-grade CSS styling for professional MVP presentation
st.markdown("""
<style>
    /* Modern Enterprise Theme */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    }
    
    /* Professional Header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a202c;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.025em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: #4a5568;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Enterprise Cards */
    .enterprise-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        transition: all 0.3s ease;
    }
    
    .enterprise-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.2);
    }
    
    /* Professional Metrics */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2);
    }
    
    /* Status Cards */
    .status-success {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 1px solid #b8daff;
        color: #155724 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-info {
        background: linear-gradient(135deg, #cce7ff, #b8daff);
        border: 1px solid #9fcdff;
        color: #004085 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 1px solid #ffd93d;
        color: #856404 !important;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border-right: 1px solid #cbd5e0;
    }
    
    /* Navigation Enhancement */
    .css-17eq0hr {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Data Tables */
    .dataframe {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #4a5568;
        font-weight: 500;
        padding: 8px 16px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
    }
    
    /* Metrics Enhancement */
    .metric-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    /* Loading States */
    .stSpinner {
        border-color: #667eea !important;
    }
    
    /* Professional Alerts */
    .alert-success {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-left: 4px solid #28a745;
        color: #155724;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135d, #cce7ff, #b8daff);
        border-left: 4px solid #007bff;
        color: #004085;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Enterprise Footer */
    .enterprise-footer {
        background: linear-gradient(135deg, #2d3748, #4a5568);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        text-align: center;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .enterprise-card {
            padding: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def generate_demo_data():
    """Generate comprehensive demo data for the platform."""
    np.random.seed(42)
    
    # Generate sample datasets
    datasets = []
    for i in range(12):
        datasets.append({
            'id': f'dataset_{i+1}',
            'name': f'Dataset {i+1}',
            'type': np.random.choice(['CSV', 'JSON', 'Parquet', 'Excel']),
            'size': f"{np.random.randint(1, 500)} MB",
            'rows': np.random.randint(1000, 100000),
            'columns': np.random.randint(5, 50),
            'created': datetime.now() - timedelta(days=np.random.randint(1, 365)),
            'status': np.random.choice(['Active', 'Processing', 'Archived'], p=[0.7, 0.2, 0.1])
        })
    
    # Generate ML models
    models = []
    model_types = ['Classification', 'Regression', 'Clustering', 'Deep Learning', 'Time Series']
    for i in range(8):
        models.append({
            'id': f'model_{i+1}',
            'name': f'Model {i+1}',
            'type': np.random.choice(model_types),
            'accuracy': np.random.uniform(0.75, 0.98),
            'status': np.random.choice(['Training', 'Deployed', 'Failed', 'Completed'], p=[0.2, 0.5, 0.1, 0.2]),
            'created': datetime.now() - timedelta(days=np.random.randint(1, 180)),
            'dataset': f'Dataset {np.random.randint(1, 12)}'
        })
    
    # Generate dashboards
    dashboards = []
    for i in range(6):
        dashboards.append({
            'id': f'dashboard_{i+1}',
            'name': f'Analytics Dashboard {i+1}',
            'widgets': np.random.randint(3, 12),
            'views': np.random.randint(100, 5000),
            'last_updated': datetime.now() - timedelta(hours=np.random.randint(1, 48)),
            'status': 'Active'
        })
    
    return {
        'datasets': datasets,
        'models': models,
        'dashboards': dashboards,
        'metrics': {
            'total_datasets': len(datasets),
            'active_models': len([m for m in models if m['status'] == 'Deployed']),
            'total_dashboards': len(dashboards),
            'data_processed': f"{np.random.randint(50, 500)} GB",
            'api_calls_today': np.random.randint(1000, 10000),
            'uptime': "99.9%"
        }
    }

# Session state initialization
if 'user_level' not in st.session_state:
    st.session_state.user_level = 'Beginner'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'demo_data' not in st.session_state:
    st.session_state.demo_data = generate_demo_data()
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Simple user database (in production, use Supabase/database)
DEMO_USERS = {
    "demo@astralytiq.com": {
        "password": "demo123",
        "name": "Demo User",
        "role": "Admin",
        "level": "Advanced"
    },
    "john@company.com": {
        "password": "password123",
        "name": "John Doe",
        "role": "Data Scientist",
        "level": "Intermediate"
    },
    "jane@company.com": {
        "password": "password123",
        "name": "Jane Smith",
        "role": "Analyst",
        "level": "Beginner"
    }
}

def authenticate_user(email, password):
    """Enhanced authentication function with production integration."""
    
    # Try production authentication first
    if auth_manager and not DEMO_MODE:
        try:
            user = auth_manager.authenticate(email, password)
            if user:
                return user
        except Exception as e:
            st.warning(f"Production auth error: {str(e)}")
    
    # Fallback to demo users
    if email in DEMO_USERS and DEMO_USERS[email]["password"] == password:
        return DEMO_USERS[email]
    return None

def show_login_page():
    """Display enterprise-grade login page for professional presentation."""
    
    # Professional Header with Company Branding
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 class="main-header">AstralytiQ</h1>
        <p class="subtitle">Enterprise MLOps Platform | Data Science & Engineering Suite</p>
        <div style="width: 100px; height: 3px; background: linear-gradient(90deg, #667eea, #764ba2); margin: 1rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Production Status Banner
    if auth_manager:
        status = auth_manager.get_integration_status()
        if status.get("supabase") or status.get("cloudinary"):
            st.markdown("""
            <div class="status-success">
                <h4 style="margin: 0 0 0.5rem 0;">🏢 Production Environment Active</h4>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span>Database: <strong>Connected</strong></span>
                    <span>Storage: <strong>Cloud Ready</strong></span>
                    <span>OAuth: <strong>Configured</strong></span>
                    <span>Status: <strong>Operational</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main Authentication Container
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Professional Login Card
        st.markdown("""
        <div class="enterprise-card">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h3 style="color: #2d3748; margin-bottom: 0.5rem;">Welcome to AstralytiQ</h3>
                <p style="color: #718096; margin: 0;">Sign in to access your enterprise MLOps workspace</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Login Form
        with st.form("enterprise_login_form", clear_on_submit=False):
            st.markdown("### Authentication")
            
            # Professional Input Fields
            email = st.text_input(
                "Email Address",
                placeholder="your.email@company.com",
                help="Enter your corporate email address"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your secure password",
                help="Use your enterprise credentials"
            )
            
            # Remember Me and Forgot Password
            col_remember, col_forgot = st.columns([1, 1])
            with col_remember:
                remember_me = st.checkbox("Remember me for 30 days")
            with col_forgot:
                if st.form_submit_button("Forgot Password?", type="secondary"):
                    st.info("Password reset functionality available in production deployment")
            
            st.markdown("---")
            
            # Professional Action Buttons
            col_login, col_demo, col_register = st.columns(3)
            
            with col_login:
                login_button = st.form_submit_button(
                    "🔐 Enterprise Login",
                    use_container_width=True,
                    type="primary"
                )
            
            with col_demo:
                demo_button = st.form_submit_button(
                    "🎯 Demo Access",
                    use_container_width=True,
                    help="Try the platform with sample data"
                )
            
            with col_register:
                register_button = st.form_submit_button(
                    "📝 Create Account",
                    use_container_width=True,
                    type="secondary"
                )
            
            # Handle Authentication
            if login_button:
                if email and password:
                    with st.spinner("Authenticating with enterprise systems..."):
                        user = authenticate_user(email, password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.current_user = user
                            st.session_state.user_level = user["level"]
                            st.success(f"✅ Welcome back, {user['name']}! Redirecting to dashboard...")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Authentication failed. Please check your credentials.")
                else:
                    st.warning("⚠️ Please enter both email and password")
            
            elif demo_button:
                with st.spinner("Initializing demo environment..."):
                    demo_user = DEMO_USERS["demo@astralytiq.com"]
                    st.session_state.authenticated = True
                    st.session_state.current_user = demo_user
                    st.session_state.user_level = demo_user["level"]
                    st.success(f"🎯 Demo mode activated! Welcome, {demo_user['name']}")
                    time.sleep(1)
                    st.rerun()
            
            elif register_button:
                st.info("🚀 Registration portal opening... (Feature available in production)")
        
        # OAuth Integration Section
        if auth_manager:
            st.markdown("---")
            st.markdown("### Enterprise Single Sign-On")
            
            try:
                auth_manager.oauth.show_oauth_buttons()
            except Exception as e:
                # Fallback OAuth buttons with professional styling
                col_google, col_github, col_microsoft = st.columns(3)
                
                with col_google:
                    if st.button("🔗 Google Workspace", use_container_width=True):
                        st.info("Google SSO configured for enterprise deployment")
                
                with col_github:
                    if st.button("🔗 GitHub Enterprise", use_container_width=True):
                        st.info("GitHub SSO configured for enterprise deployment")
                
                with col_microsoft:
                    if st.button("🔗 Microsoft 365", use_container_width=True):
                        st.info("Microsoft SSO ready for enterprise deployment")
        
        # Professional Demo Credentials
        st.markdown("---")
        st.markdown("""
        <div class="status-info">
            <h4 style="margin: 0 0 1rem 0;">🎯 Demo Environment Access</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-family: monospace;">
                <div>
                    <strong>Admin Access:</strong><br>
                    Email: demo@astralytiq.com<br>
                    Password: demo123
                </div>
                <div>
                    <strong>User Access:</strong><br>
                    Email: john@company.com<br>
                    Password: password123
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enterprise Features Showcase
        st.markdown("---")
        st.markdown("### 🏢 Enterprise Platform Capabilities")
        
        features_col1, features_col2 = st.columns(2)
        
        with features_col1:
            st.markdown("""
            **Data Engineering & MLOps:**
            - Advanced ML model training & deployment
            - Real-time data pipeline orchestration
            - Automated feature engineering
            - Model versioning & lineage tracking
            - A/B testing & experimentation
            """)
        
        with features_col2:
            st.markdown("""
            **Enterprise Infrastructure:**
            - Multi-tenant architecture
            - Role-based access control (RBAC)
            - API gateway & microservices
            - Cloud-native deployment
            - Enterprise security & compliance
            """)
        
        # Professional Footer
        st.markdown("""
        <div class="enterprise-footer">
            <p style="margin: 0; font-size: 0.9rem;">
                <strong>AstralytiQ Enterprise MLOps Platform</strong><br>
                Built for Data Scientists, ML Engineers & Software Developers<br>
                <em>Showcasing enterprise-grade architecture & professional development practices</em>
            </p>
        </div>
        """, unsafe_allow_html=True)

def show_user_profile():
    """Enhanced user profile with professional enterprise features."""
    if st.session_state.current_user:
        user = st.session_state.current_user
        
        # Professional User Profile Card
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 12px; color: white; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="width: 50px; height: 50px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 1rem;">
                    👤
                </div>
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem;">{}</div>
                    <div style="opacity: 0.9; font-size: 0.9rem;">{}</div>
                </div>
            </div>
            <div style="font-size: 0.85rem; opacity: 0.8;">
                <div>Level: <strong>{}</strong></div>
                <div>Email: <strong>{}</strong></div>
            </div>
        </div>
        """.format(
            user['name'], 
            user['role'], 
            user['level'],
            user.get('email', 'demo@astralytiq.com')
        ), unsafe_allow_html=True)
        
        # Professional Action Buttons
        if st.sidebar.button("⚙️ Profile Settings", use_container_width=True):
            st.sidebar.info("Profile settings panel would open here")
        
        if st.sidebar.button("📊 My Analytics", use_container_width=True):
            st.sidebar.info("Personal analytics dashboard would open here")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.user_data = {}
            st.success("👋 Logged out successfully!")
            st.rerun()

def show_header():
    """Display the main header with branding."""
    st.markdown('<h1 class="main-header">AstralytiQ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Educational MLOps Platform - Learn, Build, and Deploy ML</p>', unsafe_allow_html=True)

def show_user_level_selector():
    """Professional user experience level selector."""
    st.sidebar.markdown("### 🎯 Experience Level")
    
    levels = {
        'Beginner': {
            'label': '🟢 Beginner',
            'description': 'Guided workflows with tutorials',
            'features': 'Basic features, step-by-step guidance'
        },
        'Intermediate': {
            'label': '🟡 Intermediate', 
            'description': 'Advanced features with customization',
            'features': 'Data pipelines, model registry'
        },
        'Advanced': {
            'label': '🔴 Advanced',
            'description': 'Full enterprise capabilities',
            'features': 'API management, system monitoring'
        }
    }
    
    current_level = st.session_state.user_level
    
    # Professional level display
    st.sidebar.markdown(f"""
    <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <div style="font-weight: 600; color: #2d3748; margin-bottom: 0.5rem;">
            Current: {levels[current_level]['label']}
        </div>
        <div style="font-size: 0.85rem; color: #718096;">
            {levels[current_level]['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Level selector
    selected_level = st.sidebar.selectbox(
        "Switch Experience Level:",
        options=list(levels.keys()),
        index=list(levels.keys()).index(current_level),
        format_func=lambda x: levels[x]['label'],
        help="Choose your experience level to customize the interface"
    )
    
    if selected_level != current_level:
        st.session_state.user_level = selected_level
        st.sidebar.success(f"Switched to {levels[selected_level]['label']} mode!")
        st.rerun()
    
    return selected_level

def get_navigation_options(user_level):
    """Get navigation options based on user level."""
    base_options = [
        "Dashboard",
        "Data Management", 
        "ML Studio",
        "Analytics"
    ]
    
    if user_level == 'Intermediate':
        base_options.extend([
            "Data Pipelines",
            "Model Registry"
        ])
    elif user_level == 'Advanced':
        base_options.extend([
            "Data Pipelines",
            "Model Registry",
            "API Management",
            "System Monitoring",
            "User Management",
            "Platform Settings"
        ])
    
    return base_options

def show_dashboard():
    """Enterprise-grade dashboard with professional metrics and KPIs."""
    
    # Professional Dashboard Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <div>
            <h1 style="margin: 0; color: #2d3748;">Executive Dashboard</h1>
            <p style="margin: 0; color: #718096; font-size: 1.1rem;">Real-time MLOps Platform Analytics & KPIs</p>
        </div>
        <div style="text-align: right; color: #4a5568;">
            <div style="font-size: 0.9rem;">Last Updated</div>
            <div style="font-weight: 600;">{}</div>
        </div>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    demo_data = st.session_state.demo_data
    metrics = demo_data['metrics']
    
    # Enterprise KPI Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #4a5568; font-size: 0.9rem;">TOTAL DATASETS</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: #2d3748;">{metrics['total_datasets']}</h2>
                    <p style="margin: 0; color: #38a169; font-size: 0.8rem;">↗ +3 this week</p>
                </div>
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">📊</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #4a5568; font-size: 0.9rem;">ACTIVE MODELS</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: #2d3748;">{metrics['active_models']}</h2>
                    <p style="margin: 0; color: #38a169; font-size: 0.8rem;">↗ +2 deployed</p>
                </div>
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #48bb78, #38a169); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">🤖</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #4a5568; font-size: 0.9rem;">DASHBOARDS</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: #2d3748;">{metrics['total_dashboards']}</h2>
                    <p style="margin: 0; color: #3182ce; font-size: 0.8rem;">All operational</p>
                </div>
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #4299e1, #3182ce); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">📈</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #4a5568; font-size: 0.9rem;">DATA PROCESSED</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: #2d3748;">{metrics['data_processed']}</h2>
                    <p style="margin: 0; color: #38a169; font-size: 0.8rem;">↗ +15% this month</p>
                </div>
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #ed8936, #dd6b20); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">☁️</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_col5:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #4a5568; font-size: 0.9rem;">API CALLS</h4>
                    <h2 style="margin: 0.5rem 0 0 0; color: #2d3748;">{metrics['api_calls_today']:,}</h2>
                    <p style="margin: 0; color: #38a169; font-size: 0.8rem;">Today's volume</p>
                </div>
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #9f7aea, #805ad5); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">⚡</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Professional Analytics Section
    st.markdown("## 📊 Platform Analytics & Performance")
    
    analytics_col1, analytics_col2 = st.columns(2)
    
    with analytics_col1:
        # Enhanced Model Performance Chart
        models = demo_data['models']
        model_df = pd.DataFrame(models)
        
        fig = px.bar(
            model_df, 
            x='name', 
            y='accuracy',
            color='type',
            title="🎯 Model Performance Metrics",
            labels={'accuracy': 'Accuracy Score (%)', 'name': 'Model Name'},
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            height=400,
            title_font_size=16,
            title_font_color='#2d3748',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#4a5568')
        )
        fig.update_traces(texttemplate='%{y:.1%}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with analytics_col2:
        # Enhanced Dataset Distribution
        datasets = demo_data['datasets']
        dataset_df = pd.DataFrame(datasets)
        
        fig = px.pie(
            dataset_df,
            names='type',
            title="📁 Dataset Distribution by Type",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            height=400,
            title_font_size=16,
            title_font_color='#2d3748',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#4a5568')
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # System Health & Performance Monitoring
    st.markdown("## 🔧 System Health & Performance")
    
    health_col1, health_col2, health_col3 = st.columns(3)
    
    with health_col1:
        # System Uptime
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">System Uptime</h4>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #38a169;">99.9%</div>
                <p style="color: #718096; margin: 0;">Last 30 days</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with health_col2:
        # Response Time
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">Avg Response Time</h4>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #3182ce;">127ms</div>
                <p style="color: #718096; margin: 0;">API endpoints</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with health_col3:
        # Active Users
        st.markdown("""
        <div class="enterprise-card">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">Active Users</h4>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: bold; color: #805ad5;">1,247</div>
                <p style="color: #718096; margin: 0;">This month</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Activity Feed
    st.markdown("## 📋 Recent Platform Activity")
    
    activities = [
        {"time": "2 min ago", "user": "john.doe@company.com", "action": "Deployed model 'Sales Predictor v2.1' to production", "type": "deployment", "status": "success"},
        {"time": "15 min ago", "user": "jane.smith@company.com", "action": "Uploaded dataset 'Customer Behavior Q4 2024' (2.3GB)", "type": "data", "status": "success"},
        {"time": "1 hour ago", "user": "system", "action": "Automated backup completed for all model artifacts", "type": "system", "status": "success"},
        {"time": "3 hours ago", "user": "alice.brown@company.com", "action": "Started training job for 'Churn Prediction Model'", "type": "training", "status": "in_progress"},
        {"time": "5 hours ago", "user": "bob.johnson@company.com", "action": "Created new dashboard 'Revenue Analytics Q1'", "type": "dashboard", "status": "success"}
    ]
    
    for activity in activities:
        status_color = {
            "success": "#38a169",
            "in_progress": "#3182ce", 
            "warning": "#d69e2e",
            "error": "#e53e3e"
        }.get(activity["status"], "#718096")
        
        type_icon = {
            "deployment": "🚀",
            "data": "📊", 
            "system": "⚙️",
            "training": "🤖",
            "dashboard": "📈"
        }.get(activity["type"], "•")
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 1rem; background: white; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {status_color};">
            <div style="margin-right: 1rem; font-size: 1.2rem;">{type_icon}</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #2d3748;">{activity['action']}</div>
                <div style="font-size: 0.9rem; color: #718096;">
                    {activity['user']} • {activity['time']}
                </div>
            </div>
            <div style="padding: 0.25rem 0.75rem; background: {status_color}; color: white; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                {activity['status'].replace('_', ' ').title()}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model performance chart
        models = demo_data['models']
        model_df = pd.DataFrame(models)
        
        fig = px.bar(
            model_df, 
            x='name', 
            y='accuracy',
            color='type',
            title="Model Performance Overview",
            labels={'accuracy': 'Accuracy Score', 'name': 'Model Name'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Dataset distribution
        datasets = demo_data['datasets']
        dataset_df = pd.DataFrame(datasets)
        
        fig = px.pie(
            dataset_df,
            names='type',
            title="Dataset Types Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent Activity")
    
    activities = [
        {"time": "2 minutes ago", "action": "Model 'Sales Predictor' deployed successfully", "type": "success"},
        {"time": "15 minutes ago", "action": "Dataset 'Customer Data Q4' uploaded", "type": "info"},
        {"time": "1 hour ago", "action": "Dashboard 'Revenue Analytics' updated", "type": "info"},
        {"time": "3 hours ago", "action": "Training job completed for 'Churn Model'", "type": "success"},
        {"time": "5 hours ago", "action": "New user 'john.doe@company.com' registered", "type": "info"}
    ]
    
    for activity in activities:
        icon = "✓" if activity["type"] == "success" else "•"
        st.markdown(f"{icon} **{activity['time']}** - {activity['action']}")

def show_data_management():
    """Show data management interface."""
    st.header("Data Management")
    
    tab1, tab2, tab3 = st.tabs(["Datasets", "Upload Data", "Data Processing"])
    
    with tab1:
        st.subheader("Your Datasets")
        
        datasets = st.session_state.demo_data['datasets']
        dataset_df = pd.DataFrame(datasets)
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search datasets...", placeholder="Enter dataset name or type")
        with col2:
            status_filter = st.selectbox("Filter by status", ["All", "Active", "Processing", "Archived"])
        
        # Filter datasets
        filtered_df = dataset_df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False)]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        # Display datasets
        for _, dataset in filtered_df.iterrows():
            with st.expander(f"{dataset['name']} ({dataset['type']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Size", dataset['size'])
                    st.metric("Rows", f"{dataset['rows']:,}")
                with col2:
                    st.metric("Columns", dataset['columns'])
                    st.metric("Status", dataset['status'])
                with col3:
                    st.metric("Created", dataset['created'].strftime("%Y-%m-%d"))
                    if st.button(f"View Details", key=f"view_{dataset['id']}"):
                        st.success(f"Opening {dataset['name']} details...")
    
    with tab2:
        st.subheader("Upload New Dataset")
        
        upload_method = st.radio("Choose upload method:", ["File Upload", "URL Import", "Database Connection"])
        
        if upload_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'json', 'parquet'],
                help="Supported formats: CSV, Excel, JSON, Parquet"
            )
            
            if uploaded_file:
                # Enhanced upload with production storage
                if auth_manager and auth_manager.get_integration_status().get("cloudinary", False):
                    with st.spinner("Uploading to cloud storage..."):
                        try:
                            file_url = auth_manager.upload_file(
                                uploaded_file.getvalue(), 
                                folder="datasets"
                            )
                            if file_url:
                                st.success(f"File '{uploaded_file.name}' uploaded to cloud storage!")
                                st.info(f"Cloud URL: {file_url}")
                            else:
                                st.warning("Cloud upload failed, using local processing")
                        except Exception as e:
                            st.error(f"Upload error: {str(e)}")
                else:
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                
                # Show preview
                if uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                    st.subheader("Data Preview")
                    st.dataframe(df.head())
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Rows", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                
                # Production features
                if auth_manager and auth_manager.get_integration_status().get("supabase", False):
                    st.markdown("### Advanced Options")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save to Database"):
                            st.success("Dataset metadata saved to Supabase!")
                    with col2:
                        if st.button("Process with ML Pipeline"):
                            st.success("Processing started with production ML pipeline!")
        
        elif upload_method == "URL Import":
            url = st.text_input("Enter data URL:", placeholder="https://example.com/data.csv")
            if url and st.button("Import from URL"):
                st.success("Data imported successfully from URL!")
        
        else:  # Database Connection
            col1, col2 = st.columns(2)
            with col1:
                db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "MongoDB", "SQLite"])
                host = st.text_input("Host", placeholder="localhost")
            with col2:
                port = st.text_input("Port", placeholder="5432")
                database = st.text_input("Database Name")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Test Connection"):
                st.success("Connection successful!")
    
    with tab3:
        st.subheader("Data Processing Pipeline")
        
        st.markdown("""
        <div class="info-box">
            <h4>Automated Data Processing</h4>
            <p>Configure automated data cleaning, transformation, and validation pipelines.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Processing options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Cleaning Options:**")
            st.checkbox("Remove duplicates")
            st.checkbox("Handle missing values")
            st.checkbox("Normalize data types")
            st.checkbox("Validate data quality")
        
        with col2:
            st.markdown("**Transformation Options:**")
            st.checkbox("Feature scaling")
            st.checkbox("Encoding categorical variables")
            st.checkbox("Feature engineering")
            st.checkbox("Data aggregation")
        
        if st.button("Start Processing Pipeline"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = ["Validating data", "Cleaning records", "Applying transformations", "Quality checks", "Finalizing"]
            for i, step in enumerate(steps):
                status_text.text(f"Processing: {step}...")
                progress_bar.progress((i + 1) / len(steps))
                time.sleep(0.5)
            
            st.success("Data processing completed successfully!")

def show_ml_studio():
    """Enterprise ML Studio with advanced model development capabilities."""
    
    # Professional ML Studio Header
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin: 0; color: #2d3748;">🤖 ML Studio</h1>
        <p style="margin: 0; color: #718096; font-size: 1.1rem;">Enterprise Machine Learning Development & Deployment Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Model Development", 
        "📊 Model Registry", 
        "🚀 Deployment Center", 
        "📈 Performance Monitoring",
        "🔬 Experiment Tracking"
    ])
    
    with tab1:
        st.markdown("### Advanced Model Development Workspace")
        
        # Professional Model Configuration
        config_col1, config_col2 = st.columns([2, 1])
        
        with config_col1:
            st.markdown("#### Model Configuration")
            
            model_name = st.text_input(
                "Model Name",
                placeholder="e.g., customer-churn-predictor-v2",
                help="Use descriptive, version-controlled naming"
            )
            
            col_dataset, col_target = st.columns(2)
            with col_dataset:
                dataset = st.selectbox(
                    "Training Dataset",
                    [d['name'] for d in st.session_state.demo_data['datasets']],
                    help="Select your preprocessed training dataset"
                )
            
            with col_target:
                target_column = st.text_input(
                    "Target Variable",
                    placeholder="e.g., churn_probability",
                    help="Name of the target column in your dataset"
                )
            
            col_type, col_framework = st.columns(2)
            with col_type:
                model_type = st.selectbox(
                    "Model Type",
                    ["Binary Classification", "Multi-class Classification", "Regression", 
                     "Time Series Forecasting", "Clustering", "Deep Learning", "Ensemble Methods"],
                    help="Choose the appropriate ML task type"
                )
            
            with col_framework:
                framework = st.selectbox(
                    "ML Framework",
                    ["Auto-Select", "Scikit-learn", "XGBoost", "LightGBM", "TensorFlow", "PyTorch", "CatBoost"],
                    help="Select your preferred ML framework"
                )
        
        with config_col2:
            st.markdown("#### Training Configuration")
            
            # Advanced training parameters
            test_size = st.slider("Test Split (%)", 10, 40, 20, help="Percentage of data for testing")
            cv_folds = st.slider("Cross-Validation Folds", 3, 10, 5, help="Number of CV folds for validation")
            
            auto_ml = st.checkbox("Enable AutoML", help="Automated hyperparameter optimization")
            early_stopping = st.checkbox("Early Stopping", value=True, help="Stop training when no improvement")
            
            max_time = st.number_input("Max Training Time (minutes)", 5, 240, 30, help="Maximum training duration")
            
            # Resource allocation
            st.markdown("**Resource Allocation:**")
            compute_tier = st.selectbox("Compute Tier", ["CPU (2 cores)", "CPU (4 cores)", "GPU (T4)", "GPU (V100)"])
            
        # Advanced Settings for Professional Users
        if st.session_state.user_level in ['Intermediate', 'Advanced']:
            with st.expander("🔧 Advanced Configuration & Hyperparameters"):
                adv_col1, adv_col2, adv_col3 = st.columns(3)
                
                with adv_col1:
                    st.markdown("**Algorithm Settings:**")
                    if model_type in ["Binary Classification", "Multi-class Classification"]:
                        algorithm = st.selectbox("Algorithm", ["Auto", "Random Forest", "XGBoost", "Logistic Regression", "SVM", "Neural Network"])
                    elif model_type == "Regression":
                        algorithm = st.selectbox("Algorithm", ["Auto", "Random Forest", "XGBoost", "Linear Regression", "Ridge", "Lasso"])
                    
                    optimization_metric = st.selectbox(
                        "Optimization Metric",
                        ["Auto", "Accuracy", "F1-Score", "ROC-AUC", "Precision", "Recall", "RMSE", "MAE"]
                    )
                
                with adv_col2:
                    st.markdown("**Feature Engineering:**")
                    feature_selection = st.checkbox("Automated Feature Selection", value=True)
                    feature_scaling = st.selectbox("Feature Scaling", ["Auto", "StandardScaler", "MinMaxScaler", "RobustScaler", "None"])
                    handle_missing = st.selectbox("Missing Values", ["Auto", "Drop", "Mean Imputation", "Median Imputation", "Mode Imputation"])
                
                with adv_col3:
                    st.markdown("**Model Validation:**")
                    validation_strategy = st.selectbox("Validation Strategy", ["K-Fold CV", "Stratified K-Fold", "Time Series Split", "Hold-out"])
                    ensemble_methods = st.checkbox("Enable Ensemble Methods", help="Combine multiple models")
                    model_interpretability = st.checkbox("Generate SHAP Explanations", value=True)
        
        # Professional Training Execution
        st.markdown("---")
        
        training_col1, training_col2 = st.columns([3, 1])
        
        with training_col1:
            if st.button("🚀 Start Enterprise Training Job", type="primary", use_container_width=True):
                if model_name and dataset and target_column:
                    # Professional training simulation
                    st.markdown("""
                    <div class="status-success">
                        <h4>🎯 Training Job Initiated</h4>
                        <p><strong>Job ID:</strong> train_job_{}_{}</p>
                        <p><strong>Model:</strong> {}</p>
                        <p><strong>Dataset:</strong> {}</p>
                        <p><strong>Compute:</strong> {}</p>
                    </div>
                    """.format(
                        datetime.now().strftime("%Y%m%d"),
                        np.random.randint(1000, 9999),
                        model_name,
                        dataset,
                        compute_tier
                    ), unsafe_allow_html=True)
                    
                    # Enhanced training progress
                    progress_container = st.container()
                    with progress_container:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        metrics_placeholder = st.empty()
                        
                        training_steps = [
                            ("Initializing training environment", 0.1),
                            ("Loading and validating dataset", 0.2),
                            ("Performing feature engineering", 0.3),
                            ("Splitting data and creating folds", 0.4),
                            ("Training model with hyperparameter optimization", 0.7),
                            ("Validating model performance", 0.85),
                            ("Generating model artifacts and reports", 0.95),
                            ("Finalizing and registering model", 1.0)
                        ]
                        
                        for i, (step, progress) in enumerate(training_steps):
                            status_text.text(f"Step {i+1}/8: {step}...")
                            progress_bar.progress(progress)
                            
                            # Show intermediate metrics during training
                            if progress > 0.4:
                                current_accuracy = np.random.uniform(0.75, 0.95)
                                current_loss = np.random.uniform(0.1, 0.5)
                                metrics_placeholder.markdown(f"""
                                **Training Metrics:** Accuracy: {current_accuracy:.3f} | Loss: {current_loss:.3f} | Epoch: {i-2}/10
                                """)
                            
                            time.sleep(0.8)
                        
                        # Final results
                        final_accuracy = np.random.uniform(0.85, 0.95)
                        final_f1 = np.random.uniform(0.80, 0.92)
                        
                        st.success(f"""
                        ✅ **Training Completed Successfully!**
                        
                        **Final Metrics:**
                        - Accuracy: {final_accuracy:.3f}
                        - F1-Score: {final_f1:.3f}
                        - Training Time: {max_time} minutes
                        
                        Model registered in ML Registry with version 1.0
                        """)
                else:
                    st.error("Please fill in all required fields: Model Name, Dataset, and Target Column")
        
        with training_col2:
            st.markdown("#### Quick Actions")
            if st.button("📊 Load Sample Data", use_container_width=True):
                st.info("Sample dataset loaded: E-commerce Customer Data (10K rows)")
            
            if st.button("🔍 Data Profiling", use_container_width=True):
                st.info("Data quality report generated")
            
            if st.button("📈 Feature Analysis", use_container_width=True):
                st.info("Feature importance analysis completed")
    
    with tab2:
        st.markdown("### 📊 Enterprise Model Registry")
        
        # Professional model registry interface
        registry_col1, registry_col2 = st.columns([3, 1])
        
        with registry_col1:
            # Model search and filters
            search_col1, search_col2, search_col3 = st.columns(3)
            
            with search_col1:
                model_search = st.text_input("🔍 Search Models", placeholder="Search by name, tag, or description")
            
            with search_col2:
                type_filter = st.selectbox("Filter by Type", ["All Types"] + list(set([m['type'] for m in st.session_state.demo_data['models']])))
            
            with search_col3:
                status_filter = st.selectbox("Filter by Status", ["All Status", "Training", "Deployed", "Failed", "Completed", "Archived"])
        
        with registry_col2:
            st.markdown("#### Registry Stats")
            models = st.session_state.demo_data['models']
            st.metric("Total Models", len(models))
            st.metric("Deployed", len([m for m in models if m['status'] == 'Deployed']))
            st.metric("In Training", len([m for m in models if m['status'] == 'Training']))
        
        # Enhanced model display
        st.markdown("---")
        
        for model in st.session_state.demo_data['models']:
            if (type_filter == "All Types" or model['type'] == type_filter) and \
               (status_filter == "All Status" or model['status'] == status_filter):
                
                # Professional model card
                status_colors = {
                    "Deployed": "#38a169",
                    "Training": "#3182ce", 
                    "Completed": "#805ad5",
                    "Failed": "#e53e3e"
                }
                
                status_color = status_colors.get(model['status'], "#718096")
                
                st.markdown(f"""
                <div class="enterprise-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                        <div>
                            <h4 style="margin: 0; color: #2d3748;">{model['name']}</h4>
                            <p style="margin: 0.25rem 0; color: #718096;">{model['type']} • Created {model['created'].strftime('%Y-%m-%d')}</p>
                        </div>
                        <div style="padding: 0.25rem 0.75rem; background: {status_color}; color: white; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                            {model['status']}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1rem;">
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Accuracy</div>
                            <div style="font-weight: 600; color: #2d3748;">{model['accuracy']:.1%}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Dataset</div>
                            <div style="font-weight: 600; color: #2d3748;">{model['dataset']}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Version</div>
                            <div style="font-weight: 600; color: #2d3748;">v1.{np.random.randint(0, 9)}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Framework</div>
                            <div style="font-weight: 600; color: #2d3748;">XGBoost</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                action_col1, action_col2, action_col3, action_col4 = st.columns(4)
                
                with action_col1:
                    if st.button("📊 View Details", key=f"details_{model['id']}", use_container_width=True):
                        st.info(f"Opening detailed analytics for {model['name']}")
                
                with action_col2:
                    if model['status'] == 'Completed' and st.button("🚀 Deploy", key=f"deploy_{model['id']}", use_container_width=True):
                        st.success(f"Initiating deployment for {model['name']}...")
                
                with action_col3:
                    if st.button("📈 Compare", key=f"compare_{model['id']}", use_container_width=True):
                        st.info("Opening model comparison dashboard...")
                
                with action_col4:
                    if st.button("📋 Export", key=f"export_{model['id']}", use_container_width=True):
                        st.info("Generating model export package...")
                
                st.markdown("---")
    
    with tab3:
        st.markdown("### 🚀 Enterprise Deployment Center")
        
        deployed_models = [m for m in st.session_state.demo_data['models'] if m['status'] == 'Deployed']
        
        if deployed_models:
            st.markdown("#### Active Production Deployments")
            
            for model in deployed_models:
                st.markdown(f"""
                <div class="enterprise-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <div>
                            <h4 style="margin: 0; color: #2d3748;">{model['name']}</h4>
                            <p style="margin: 0.25rem 0; color: #718096;">{model['type']} • Accuracy: {model['accuracy']:.1%}</p>
                        </div>
                        <div style="padding: 0.25rem 0.75rem; background: #38a169; color: white; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                            LIVE
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Requests/Day</div>
                            <div style="font-weight: 600; color: #2d3748;">{np.random.randint(100, 1000):,}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Avg Response</div>
                            <div style="font-weight: 600; color: #2d3748;">{np.random.randint(50, 200)}ms</div>
                        </div>
                        <div>
                            <div style="font-size: 0.8rem; color: #718096;">Uptime</div>
                            <div style="font-weight: 600; color: #2d3748;">99.{np.random.randint(7, 9)}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                deploy_col1, deploy_col2, deploy_col3 = st.columns(3)
                with deploy_col1:
                    if st.button("📊 Metrics", key=f"metrics_{model['id']}", use_container_width=True):
                        st.info(f"Opening metrics dashboard for {model['name']}")
                with deploy_col2:
                    if st.button("⚙️ Configure", key=f"config_{model['id']}", use_container_width=True):
                        st.info(f"Opening configuration panel for {model['name']}")
                with deploy_col3:
                    if st.button("🔄 Update", key=f"update_{model['id']}", use_container_width=True):
                        st.info(f"Initiating rolling update for {model['name']}")
                
                st.markdown("---")
        
        else:
            st.info("No models currently deployed. Deploy a model from the Model Registry.")
        
        # New deployment configuration
        st.markdown("#### 🚀 Deploy New Model")
        
        available_models = [m for m in st.session_state.demo_data['models'] if m['status'] == 'Completed']
        if available_models:
            deploy_col1, deploy_col2 = st.columns(2)
            
            with deploy_col1:
                model_to_deploy = st.selectbox("Select Model", [m['name'] for m in available_models])
                deployment_name = st.text_input("Deployment Name", placeholder="production-model-v1")
                environment = st.selectbox("Environment", ["Production", "Staging", "Development"])
            
            with deploy_col2:
                instance_type = st.selectbox("Instance Type", [
                    "Small (1 CPU, 2GB RAM)", 
                    "Medium (2 CPU, 4GB RAM)", 
                    "Large (4 CPU, 8GB RAM)",
                    "GPU (1 GPU, 8GB RAM)"
                ])
                auto_scaling = st.checkbox("Enable Auto-scaling", value=True)
                monitoring = st.checkbox("Enable Monitoring", value=True)
            
            if st.button("🚀 Deploy to Production", type="primary", use_container_width=True):
                st.success(f"✅ Deploying {model_to_deploy} to {environment}... Estimated time: 3-5 minutes")
    
    with tab4:
        st.markdown("### 📈 Performance Monitoring & Analytics")
        
        # Model performance metrics
        monitoring_col1, monitoring_col2 = st.columns(2)
        
        with monitoring_col1:
            # Generate sample monitoring data
            dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
            accuracy_data = np.random.normal(0.85, 0.05, len(dates))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, 
                y=accuracy_data, 
                mode='lines+markers', 
                name='Model Accuracy',
                line=dict(color='#667eea', width=3)
            ))
            fig.update_layout(
                title="📊 Model Accuracy Trend",
                xaxis_title="Date",
                yaxis_title="Accuracy Score",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with monitoring_col2:
            latency_data = np.random.normal(150, 30, len(dates))
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates, 
                y=latency_data, 
                mode='lines+markers', 
                name='Response Latency',
                line=dict(color='#f56565', width=3)
            ))
            fig.update_layout(
                title="⚡ Response Latency Trend",
                xaxis_title="Date",
                yaxis_title="Latency (ms)",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Alerts and notifications
        st.markdown("#### 🚨 System Alerts & Notifications")
        
        alerts = [
            {"type": "warning", "message": "Model accuracy dropped below 80% threshold for 'Customer Churn Predictor'", "time": "2 hours ago", "severity": "Medium"},
            {"type": "info", "message": "High traffic detected - auto-scaling triggered for 'Sales Forecaster'", "time": "4 hours ago", "severity": "Low"},
            {"type": "success", "message": "Model deployment completed successfully for 'Recommendation Engine v2.1'", "time": "1 day ago", "severity": "Info"},
            {"type": "error", "message": "Training job failed for 'Fraud Detection Model' - insufficient memory", "time": "2 days ago", "severity": "High"}
        ]
        
        for alert in alerts:
            severity_colors = {
                "High": "#e53e3e",
                "Medium": "#d69e2e", 
                "Low": "#3182ce",
                "Info": "#38a169"
            }
            
            type_icons = {
                "warning": "⚠️",
                "info": "ℹ️",
                "success": "✅",
                "error": "❌"
            }
            
            color = severity_colors.get(alert["severity"], "#718096")
            icon = type_icons.get(alert["type"], "•")
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 1rem; background: white; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};">
                <div style="margin-right: 1rem; font-size: 1.2rem;">{icon}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #2d3748;">{alert['message']}</div>
                    <div style="font-size: 0.9rem; color: #718096;">{alert['time']}</div>
                </div>
                <div style="padding: 0.25rem 0.75rem; background: {color}; color: white; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                    {alert['severity']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 🔬 Experiment Tracking & A/B Testing")
        
        # Experiment tracking interface
        st.markdown("#### Active Experiments")
        
        experiments = [
            {"name": "Model Architecture Comparison", "status": "Running", "progress": 65, "participants": 1000},
            {"name": "Feature Engineering Impact", "status": "Completed", "progress": 100, "participants": 2500},
            {"name": "Hyperparameter Optimization", "status": "Planning", "progress": 0, "participants": 0}
        ]
        
        for exp in experiments:
            status_colors = {
                "Running": "#3182ce",
                "Completed": "#38a169",
                "Planning": "#d69e2e"
            }
            
            st.markdown(f"""
            <div class="enterprise-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4 style="margin: 0; color: #2d3748;">{exp['name']}</h4>
                    <div style="padding: 0.25rem 0.75rem; background: {status_colors[exp['status']]}; color: white; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">
                        {exp['status']}
                    </div>
                </div>
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span>Progress</span>
                        <span>{exp['progress']}%</span>
                    </div>
                    <div style="background: #e2e8f0; border-radius: 4px; height: 8px;">
                        <div style="background: {status_colors[exp['status']]}; width: {exp['progress']}%; height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                <div style="color: #718096; font-size: 0.9rem;">
                    Participants: {exp['participants']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_analytics():
    """Show analytics and reporting interface."""
    st.header("📈 Analytics & Reporting")
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboards", "📋 Reports", "🔍 Data Explorer"])
    
    with tab1:
        st.subheader("Interactive Dashboards")
        
        dashboards = st.session_state.demo_data['dashboards']
        
        # Dashboard grid
        cols = st.columns(2)
        for i, dashboard in enumerate(dashboards):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### 📊 {dashboard['name']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Widgets", dashboard['widgets'])
                        st.metric("Views", f"{dashboard['views']:,}")
                    with col2:
                        st.metric("Last Updated", dashboard['last_updated'].strftime("%H:%M"))
                        st.metric("Status", dashboard['status'])
                    
                    if st.button(f"Open Dashboard", key=f"open_dash_{dashboard['id']}"):
                        st.success(f"Opening {dashboard['name']}...")
                    
                    st.divider()
        
        # Create new dashboard
        st.markdown("### ➕ Create New Dashboard")
        
        col1, col2 = st.columns(2)
        with col1:
            dashboard_name = st.text_input("Dashboard Name", placeholder="My Analytics Dashboard")
            template = st.selectbox("Template", ["Blank", "Sales Analytics", "ML Monitoring", "Data Quality", "User Engagement"])
        
        with col2:
            data_source = st.selectbox("Primary Data Source", [d['name'] for d in st.session_state.demo_data['datasets']])
            refresh_rate = st.selectbox("Refresh Rate", ["Real-time", "Every 5 minutes", "Hourly", "Daily"])
        
        if st.button("🎨 Create Dashboard"):
            st.success(f"Creating dashboard '{dashboard_name}' with {template} template...")
    
    with tab2:
        st.subheader("Automated Reports")
        
        # Report templates
        report_types = [
            {"name": "Weekly ML Performance", "description": "Model accuracy, deployment stats, and performance metrics"},
            {"name": "Data Quality Report", "description": "Data completeness, anomalies, and validation results"},
            {"name": "Usage Analytics", "description": "Platform usage, user activity, and resource utilization"},
            {"name": "Business Intelligence", "description": "KPIs, trends, and business insights"}
        ]
        
        for report in report_types:
            with st.expander(f"📋 {report['name']}"):
                st.write(report['description'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"], key=f"freq_{report['name']}")
                with col2:
                    format_type = st.selectbox("Format", ["PDF", "Excel", "HTML"], key=f"format_{report['name']}")
                with col3:
                    if st.button("📧 Subscribe", key=f"sub_{report['name']}"):
                        st.success(f"Subscribed to {report['name']} ({frequency})")
        
        # Custom report builder
        st.markdown("### 🔧 Custom Report Builder")
        
        col1, col2 = st.columns(2)
        with col1:
            report_name = st.text_input("Report Name")
            data_sources = st.multiselect("Data Sources", [d['name'] for d in st.session_state.demo_data['datasets']])
        
        with col2:
            metrics = st.multiselect("Metrics", ["Accuracy", "Latency", "Throughput", "Error Rate", "Data Quality"])
            time_range = st.selectbox("Time Range", ["Last 7 days", "Last 30 days", "Last 3 months", "Custom"])
        
        if st.button("📊 Generate Report"):
            st.success("Generating custom report... You'll receive it via email when ready.")
    
    with tab3:
        st.subheader("Data Explorer")
        
        # Interactive data exploration
        selected_dataset = st.selectbox("Select Dataset to Explore", [d['name'] for d in st.session_state.demo_data['datasets']])
        
        if selected_dataset:
            # Generate sample data for exploration
            np.random.seed(42)
            sample_data = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=100),
                'sales': np.random.normal(1000, 200, 100),
                'customers': np.random.poisson(50, 100),
                'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
                'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 100)
            })
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Exploration Options:**")
                chart_type = st.selectbox("Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot"])
                x_axis = st.selectbox("X-Axis", sample_data.columns)
                y_axis = st.selectbox("Y-Axis", [col for col in sample_data.columns if col != x_axis])
                
                if chart_type in ["Bar Chart", "Box Plot"]:
                    color_by = st.selectbox("Color By", [None] + [col for col in sample_data.columns if col not in [x_axis, y_axis]])
            
            with col2:
                # Generate chart based on selections
                if chart_type == "Line Chart":
                    fig = px.line(sample_data, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                elif chart_type == "Bar Chart":
                    fig = px.bar(sample_data, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} by {x_axis}")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(sample_data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                elif chart_type == "Histogram":
                    fig = px.histogram(sample_data, x=x_axis, title=f"Distribution of {x_axis}")
                else:  # Box Plot
                    fig = px.box(sample_data, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} distribution by {x_axis}")
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Data summary
            st.markdown("### 📊 Data Summary")
            st.dataframe(sample_data.describe())

def show_advanced_features():
    """Show advanced features for experienced users."""
    st.header("🔧 Advanced Platform Features")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌐 API Management", "⚙️ System Monitoring", "👥 User Management", "🔧 Settings"])
    
    with tab1:
        st.subheader("API Management")
        
        # API endpoints
        st.markdown("### 🔗 Available Endpoints")
        
        endpoints = [
            {"method": "GET", "path": "/api/v1/datasets", "description": "List all datasets"},
            {"method": "POST", "path": "/api/v1/datasets", "description": "Create new dataset"},
            {"method": "GET", "path": "/api/v1/models", "description": "List all models"},
            {"method": "POST", "path": "/api/v1/models/train", "description": "Start model training"},
            {"method": "POST", "path": "/api/v1/models/{id}/predict", "description": "Make predictions"},
            {"method": "GET", "path": "/api/v1/dashboards", "description": "List all dashboards"}
        ]
        
        for endpoint in endpoints:
            method_color = {"GET": "🟢", "POST": "🔵", "PUT": "🟡", "DELETE": "🔴"}
            st.markdown(f"{method_color[endpoint['method']]} **{endpoint['method']}** `{endpoint['path']}` - {endpoint['description']}")
        
        # API key management
        st.markdown("### 🔑 API Keys")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("API Key Name", placeholder="production-key")
            st.selectbox("Permissions", ["Read Only", "Read/Write", "Admin"])
        with col2:
            st.date_input("Expiration Date")
            if st.button("🔑 Generate API Key"):
                api_key = f"ak_{uuid.uuid4().hex[:16]}"
                st.code(api_key)
                st.success("API key generated successfully!")
    
    with tab2:
        st.subheader("System Monitoring")
        
        # System metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("CPU Usage", "45%", "↗️ +5%")
        with col2:
            st.metric("Memory Usage", "62%", "↘️ -3%")
        with col3:
            st.metric("Disk Usage", "78%", "↗️ +2%")
        with col4:
            st.metric("Network I/O", "1.2 GB/s", "↗️ +15%")
        
        # Performance charts
        st.markdown("### 📊 Performance Metrics")
        
        # Generate sample performance data
        hours = list(range(24))
        cpu_usage = [np.random.normal(45, 10) for _ in hours]
        memory_usage = [np.random.normal(60, 15) for _ in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=cpu_usage, mode='lines', name='CPU Usage (%)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=hours, y=memory_usage, mode='lines', name='Memory Usage (%)', line=dict(color='red')))
        fig.update_layout(title="System Performance (Last 24 Hours)", xaxis_title="Hour", yaxis_title="Usage (%)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Service status
        st.markdown("### 🔧 Service Status")
        
        services = [
            {"name": "API Gateway", "status": "Running", "uptime": "99.9%"},
            {"name": "Data Service", "status": "Running", "uptime": "99.8%"},
            {"name": "ML Service", "status": "Running", "uptime": "99.7%"},
            {"name": "Dashboard Service", "status": "Running", "uptime": "99.9%"},
            {"name": "User Service", "status": "Running", "uptime": "99.6%"},
            {"name": "Database", "status": "Running", "uptime": "99.9%"}
        ]
        
        for service in services:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{service['name']}**")
            with col2:
                st.markdown(f"🟢 {service['status']}")
            with col3:
                st.markdown(f"⏱️ {service['uptime']}")
    
    with tab3:
        st.subheader("User Management")
        
        # User statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", "1,247", "↗️ +23")
        with col2:
            st.metric("Active Today", "89", "↗️ +12")
        with col3:
            st.metric("New This Week", "34", "↗️ +8")
        
        # User list
        st.markdown("### 👥 User Directory")
        
        users = [
            {"name": "John Doe", "email": "john.doe@company.com", "role": "Admin", "last_login": "2 hours ago"},
            {"name": "Jane Smith", "email": "jane.smith@company.com", "role": "Data Scientist", "last_login": "1 day ago"},
            {"name": "Bob Johnson", "email": "bob.johnson@company.com", "role": "Analyst", "last_login": "3 hours ago"},
            {"name": "Alice Brown", "email": "alice.brown@company.com", "role": "Manager", "last_login": "5 hours ago"}
        ]
        
        for user in users:
            with st.expander(f"👤 {user['name']} ({user['role']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {user['email']}")
                    st.write(f"**Role:** {user['role']}")
                with col2:
                    st.write(f"**Last Login:** {user['last_login']}")
                    if st.button(f"Edit User", key=f"edit_{user['name']}"):
                        st.info(f"Opening user editor for {user['name']}")
        
        # Add new user
        st.markdown("### ➕ Add New User")
        
        col1, col2 = st.columns(2)
        with col1:
            new_user_name = st.text_input("Full Name")
            new_user_email = st.text_input("Email Address")
        with col2:
            new_user_role = st.selectbox("Role", ["Viewer", "Analyst", "Data Scientist", "Manager", "Admin"])
            if st.button("👤 Add User"):
                st.success(f"User {new_user_name} added successfully!")
    
    with tab4:
        st.subheader("Platform Settings")
        
        # General settings
        st.markdown("### ⚙️ General Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Platform Name", value="AstralytiQ")
            st.selectbox("Default Theme", ["Light", "Dark", "Auto"])
            st.selectbox("Default Language", ["English", "Spanish", "French", "German"])
        
        with col2:
            st.number_input("Session Timeout (minutes)", 15, 480, 60)
            st.checkbox("Enable Notifications", value=True)
            st.checkbox("Enable Analytics Tracking", value=True)
        
        # Security settings
        st.markdown("### 🔒 Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Require 2FA", value=False)
            st.checkbox("Enable IP Whitelisting", value=False)
            st.selectbox("Password Policy", ["Standard", "Strong", "Very Strong"])
        
        with col2:
            st.number_input("Max Login Attempts", 3, 10, 5)
            st.number_input("Password Expiry (days)", 30, 365, 90)
            st.checkbox("Enable Audit Logging", value=True)
        
        # Data settings
        st.markdown("### 📊 Data Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Max File Size (MB)", 10, 1000, 100)
            st.selectbox("Default Data Retention", ["30 days", "90 days", "1 year", "Forever"])
        
        with col2:
            st.checkbox("Enable Data Encryption", value=True)
            st.checkbox("Enable Automatic Backups", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")

def main():
    """Main application function with enterprise-grade interface."""
    # Check authentication status
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # Professional Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea, #764ba2); padding: 1rem 2rem; margin: -1rem -1rem 2rem -1rem; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; font-size: 1.8rem;">AstralytiQ Enterprise</h1>
                <p style="margin: 0; opacity: 0.9;">MLOps Platform • Data Science & Engineering Suite</p>
            </div>
            <div style="text-align: right; font-size: 0.9rem;">
                <div>🟢 All Systems Operational</div>
                <div>Uptime: 99.9% • Last Updated: {}</div>
            </div>
        </div>
    </div>
    """.format(datetime.now().strftime('%H:%M:%S')), unsafe_allow_html=True)
    
    # User profile and logout
    show_user_profile()
    
    # User level selector
    user_level = show_user_level_selector()
    
    # Professional Navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Platform Navigation")
    
    nav_options = get_navigation_options(user_level)
    
    # Enhanced navigation with icons and descriptions
    nav_descriptions = {
        "Dashboard": "📊 Executive overview and KPIs",
        "Data Management": "🗃️ Dataset operations and pipelines", 
        "ML Studio": "🤖 Model development and training",
        "Analytics": "📈 Business intelligence and reporting",
        "Data Pipelines": "🔄 ETL and data orchestration",
        "Model Registry": "📋 Model versioning and lifecycle",
        "API Management": "🌐 REST API and integrations",
        "System Monitoring": "⚙️ Infrastructure and performance",
        "User Management": "👥 Access control and permissions",
        "Platform Settings": "🔧 Configuration and preferences"
    }
    
    # Create professional navigation
    selected_page = None
    for option in nav_options:
        description = nav_descriptions.get(option, "")
        if st.sidebar.button(f"{description}", key=f"nav_{option}", use_container_width=True):
            selected_page = option
            break
    
    # Default to Dashboard if no selection
    if not selected_page:
        selected_page = "Dashboard"
    
    # Professional sidebar status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Status")
    
    # Enhanced status indicators
    status_items = [
        ("Platform Health", "🟢 Operational", "#38a169"),
        ("Active Users", "1,247 online", "#3182ce"),
        ("API Response", "127ms avg", "#805ad5"),
        ("Data Processing", f"{st.session_state.demo_data['metrics']['data_processed']}", "#d69e2e")
    ]
    
    for label, value, color in status_items:
        st.sidebar.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 0.5rem; background: rgba(255,255,255,0.5); border-radius: 6px; margin: 0.25rem 0; border-left: 3px solid {color};">
            <span style="font-size: 0.85rem; color: #4a5568;">{label}</span>
            <span style="font-size: 0.85rem; font-weight: 600; color: #2d3748;">{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Production integration status
    if auth_manager:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔗 Integration Status")
        
        status = auth_manager.get_integration_status()
        integrations = [
            ("Database", "✅ Connected" if status.get('supabase') else "🎯 Demo Mode"),
            ("Storage", "✅ Connected" if status.get('cloudinary') else "🎯 Demo Mode"),
            ("OAuth", "✅ Configured" if status.get('oauth') else "❌ Disabled"),
            ("Local Cache", "✅ Available" if status.get('local_storage') else "❌ Unavailable")
        ]
        
        for service, status_text in integrations:
            st.sidebar.markdown(f"**{service}:** {status_text}")
    
    # Environment indicator
    st.sidebar.markdown("---")
    if DEMO_MODE:
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, #ffd93d, #ffeaa7); padding: 1rem; border-radius: 8px; color: #856404;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">🎯 Demo Environment</div>
            <div style="font-size: 0.85rem;">Running with sample data for demonstration purposes</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135d, #d4edda, #c3e6cb); padding: 1rem; border-radius: 8px; color: #155724;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">🚀 Production Mode</div>
            <div style="font-size: 0.85rem;">Connected to live enterprise systems</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if selected_page == "Dashboard":
        show_dashboard()
    elif selected_page == "Data Management":
        show_data_management()
    elif selected_page == "ML Studio":
        show_ml_studio()
    elif selected_page == "Analytics":
        show_analytics()
    elif selected_page in ["API Management", "System Monitoring", "User Management", "Platform Settings"]:
        show_advanced_features()
    else:
        # Professional placeholder for other pages
        st.markdown(f"""
        <div class="enterprise-card">
            <h2 style="color: #2d3748; margin-bottom: 1rem;">{selected_page}</h2>
            <p style="color: #718096; font-size: 1.1rem;">This enterprise feature is currently under development.</p>
            
            <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0;">
                <h4 style="color: #2d3748; margin-bottom: 1rem;">Planned Features:</h4>
        """, unsafe_allow_html=True)
        
        if selected_page == "Data Pipelines":
            st.markdown("""
                <ul style="color: #4a5568;">
                    <li>Visual pipeline builder with drag-and-drop interface</li>
                    <li>Automated data transformations and quality checks</li>
                    <li>Scheduling and monitoring with alerting</li>
                    <li>Error handling and recovery mechanisms</li>
                    <li>Integration with Apache Airflow and Kubernetes</li>
                </ul>
            </div>
        </div>
            """, unsafe_allow_html=True)
        
        elif selected_page == "Model Registry":
            st.markdown("""
                <ul style="color: #4a5568;">
                    <li>Centralized model versioning and lineage tracking</li>
                    <li>A/B testing and performance comparison tools</li>
                    <li>Automated deployment and rollback capabilities</li>
                    <li>Model governance and compliance features</li>
                    <li>Integration with MLflow and Kubeflow</li>
                </ul>
            </div>
        </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()