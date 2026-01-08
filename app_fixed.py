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

# Enterprise-grade CSS styling
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
    
    /* Loading states and skeleton screens */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-indicator.online {
        background: #c6f6d5;
        color: #22543d;
    }
    
    .status-indicator.offline {
        background: #fed7d7;
        color: #742a2a;
    }
    
    .status-indicator.processing {
        background: #fef5e7;
        color: #744210;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Progress bars */
    .progress-container {
        background: #e2e8f0;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Enhanced cards with micro-interactions */
    .enhanced-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .enhanced-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: left 0.3s ease;
    }
    
    .enhanced-card:hover::before {
        left: 0;
    }
    
    .enhanced-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .enterprise-header h1 {
            font-size: 2rem;
        }
        
        .enterprise-header p {
            font-size: 1rem;
        }
        
        .metric-card, .enhanced-card {
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
    
    @media (max-width: 480px) {
        .enterprise-header {
            padding: 1.5rem;
        }
        
        .enterprise-header h1 {
            font-size: 1.8rem;
        }
        
        .metric-card, .enhanced-card {
            padding: 1rem;
        }
        
        .metric-card h2 {
            font-size: 1.8rem;
        }
        
        .main-container {
            margin: 0.25rem;
            padding: 0.5rem;
        }
    }
    
    /* Accessibility Improvements */
    .enhanced-card:focus-within {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
    
    .stButton > button:focus {
        outline: 2px solid #667eea;
        outline-offset: 2px;
    }
    
    .status-indicator {
        role: status;
        aria-live: polite;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .metric-card, .enhanced-card {
            border: 2px solid #000;
        }
        
        .enterprise-header {
            background: #000;
            color: #fff;
        }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        .metric-card, .enhanced-card, .stButton > button {
            transition: none;
        }
        
        .loading-spinner {
            animation: none;
        }
        
        .status-dot {
            animation: none;
        }
        
        @keyframes loading, spin, pulse {
            to { transform: none; }
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        }
        
        .enhanced-card, .metric-card {
            background: #2d3748;
            color: #e2e8f0;
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .enhanced-card h3, .metric-card h3 {
            color: #e2e8f0;
        }
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
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
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
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Navigation styling */
    .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Demo data generation
@st.cache_data
def generate_enterprise_demo_data():
    """Generate comprehensive enterprise demo data."""
    np.random.seed(42)
    
    # Enterprise datasets
    datasets = []
    dataset_types = ['Customer Analytics', 'Sales Forecasting', 'Risk Assessment', 'Market Intelligence', 'Operational Metrics']
    for i in range(15):
        datasets.append({
            'id': f'ds_{i+1:03d}',
            'name': f'{np.random.choice(dataset_types)} Dataset {i+1}',
            'type': np.random.choice(['CSV', 'Parquet', 'JSON', 'Delta Lake']),
            'size': f"{np.random.randint(10, 5000)} MB",
            'rows': np.random.randint(10000, 10000000),
            'columns': np.random.randint(10, 200),
            'created': datetime.now() - timedelta(days=np.random.randint(1, 365)),
            'status': np.random.choice(['Active', 'Processing', 'Archived'], p=[0.8, 0.15, 0.05]),
            'quality_score': np.random.uniform(0.85, 0.99),
            'last_updated': datetime.now() - timedelta(hours=np.random.randint(1, 168))
        })
    
    # ML models with enterprise metrics
    models = []
    model_types = ['Deep Learning', 'Ensemble', 'Time Series', 'NLP', 'Computer Vision', 'Recommendation']
    for i in range(12):
        models.append({
            'id': f'ml_{i+1:03d}',
            'name': f'{np.random.choice(model_types)} Model v{np.random.randint(1,5)}.{np.random.randint(0,10)}',
            'type': np.random.choice(model_types),
            'accuracy': np.random.uniform(0.82, 0.97),
            'precision': np.random.uniform(0.80, 0.95),
            'recall': np.random.uniform(0.78, 0.93),
            'f1_score': np.random.uniform(0.79, 0.94),
            'status': np.random.choice(['Training', 'Deployed', 'Testing', 'Completed'], p=[0.1, 0.6, 0.1, 0.2]),
            'created': datetime.now() - timedelta(days=np.random.randint(1, 180)),
            'deployment_date': datetime.now() - timedelta(days=np.random.randint(1, 90)),
            'requests_per_day': np.random.randint(1000, 100000),
            'avg_latency': np.random.randint(50, 300),
            'cost_per_month': np.random.randint(100, 5000)
        })
    
    # Enterprise dashboards
    dashboards = []
    dashboard_types = ['Executive Summary', 'Operational KPIs', 'ML Performance', 'Data Quality', 'Business Intelligence']
    for i in range(8):
        dashboards.append({
            'id': f'dash_{i+1:03d}',
            'name': f'{np.random.choice(dashboard_types)} Dashboard',
            'widgets': np.random.randint(6, 20),
            'views_today': np.random.randint(50, 500),
            'views_total': np.random.randint(1000, 50000),
            'last_updated': datetime.now() - timedelta(minutes=np.random.randint(5, 1440)),
            'status': 'Active',
            'refresh_rate': np.random.choice(['Real-time', '5 minutes', '15 minutes', 'Hourly']),
            'users': np.random.randint(5, 100)
        })
    
    return {
        'datasets': datasets,
        'models': models,
        'dashboards': dashboards,
        'metrics': {
            'total_datasets': len(datasets),
            'active_models': len([m for m in models if m['status'] == 'Deployed']),
            'total_dashboards': len(dashboards),
            'data_processed_tb': round(np.random.uniform(5.2, 50.8), 1),
            'api_calls_today': np.random.randint(50000, 500000),
            'uptime_percentage': 99.97,
            'active_users': np.random.randint(150, 1500),
            'cost_savings': f"${np.random.randint(50000, 500000):,}",
            'model_accuracy_avg': 0.924,
            'data_quality_score': 0.967
        }
    }

# Enhanced UI Components
def render_loading_state(message="Loading..."):
    """Render professional loading state."""
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div class="loading-spinner"></div>
        <p style="margin-top: 1rem; color: #667eea; font-weight: 500;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def render_status_indicator(status, label="Status"):
    """Render professional status indicator."""
    status_classes = {
        'online': 'online',
        'active': 'online', 
        'deployed': 'online',
        'completed': 'online',
        'offline': 'offline',
        'failed': 'offline',
        'error': 'offline',
        'processing': 'processing',
        'training': 'processing',
        'pending': 'processing'
    }
    
    status_class = status_classes.get(status.lower(), 'processing')
    
    return f"""
    <div class="status-indicator {status_class}">
        <div class="status-dot"></div>
        <span>{label}: {status.title()}</span>
    </div>
    """

def render_progress_bar(percentage, label="Progress"):
    """Render professional progress bar."""
    return f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 500; color: #2d3748;">{label}</span>
            <span style="font-weight: 600; color: #667eea;">{percentage}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%;"></div>
        </div>
    </div>
    """

def render_enhanced_metric_card(title, value, subtitle="", trend=None, icon="📊"):
    """Render enhanced metric card with animations."""
    trend_indicator = ""
    if trend:
        trend_color = "#22543d" if trend > 0 else "#742a2a"
        trend_symbol = "↗️" if trend > 0 else "↘️"
        trend_indicator = f'<p style="color: {trend_color}; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{trend_symbol} {abs(trend)}% vs last period</p>'
    
    return f"""
    <div class="enhanced-card">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">{icon}</div>
            <div>
                <h3 style="color: #2d3748; font-size: 1.1rem; font-weight: 600; margin: 0;">{title}</h3>
                <h2 style="color: #667eea; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0 0 0;">{value}</h2>
            </div>
        </div>
        {f'<p style="color: #718096; margin: 0; font-size: 0.9rem;">{subtitle}</p>' if subtitle else ''}
        {trend_indicator}
    </div>
    """

def render_skeleton_card():
    """Render skeleton loading card."""
    return """
    <div class="enhanced-card">
        <div class="skeleton" style="height: 20px; margin-bottom: 1rem; border-radius: 4px;"></div>
        <div class="skeleton" style="height: 40px; margin-bottom: 0.5rem; border-radius: 4px; width: 60%;"></div>
        <div class="skeleton" style="height: 16px; border-radius: 4px; width: 80%;"></div>
    </div>
    """

# Session state initialization
if 'user_level' not in st.session_state:
    st.session_state.user_level = 'Advanced'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'demo_data' not in st.session_state:
    st.session_state.demo_data = generate_enterprise_demo_data()
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Enterprise user database
ENTERPRISE_USERS = {
    "admin@astralytiq.com": {
        "password": "admin123",
        "name": "System Administrator",
        "role": "Platform Admin",
        "level": "Advanced",
        "department": "IT Operations"
    },
    "data.scientist@astralytiq.com": {
        "password": "ds123",
        "name": "Dr. Sarah Chen",
        "role": "Senior Data Scientist",
        "level": "Advanced",
        "department": "Data Science"
    },
    "analyst@astralytiq.com": {
        "password": "analyst123",
        "name": "Michael Rodriguez",
        "role": "Business Analyst",
        "level": "Intermediate",
        "department": "Business Intelligence"
    }
}

def show_enterprise_login():
    """Enterprise-grade login interface."""
    st.markdown("""
    <div class="enterprise-header">
        <h1>⚡ AstralytiQ</h1>
        <p>Enterprise MLOps Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        # Production status indicator
        if PRODUCTION_MODE:
            st.markdown('<span class="status-badge status-success">Production Ready</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-info">Demo Mode</span>', unsafe_allow_html=True)
        
        st.markdown("### Welcome Back")
        st.markdown("Sign in to access your enterprise MLOps platform")
        
        # Login form
        with st.form("enterprise_login"):
            email = st.text_input("Email Address", placeholder="admin@astralytiq.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_demo = st.columns(2)
            
            with col_login:
                login_clicked = st.form_submit_button("Sign In", use_container_width=True)
            
            with col_demo:
                demo_clicked = st.form_submit_button("Demo Access", use_container_width=True)
            
            if login_clicked and email and password:
                if email in ENTERPRISE_USERS and ENTERPRISE_USERS[email]["password"] == password:
                    user = ENTERPRISE_USERS[email].copy()
                    user['email'] = email
                    st.session_state.authenticated = True
                    st.session_state.current_user = user
                    st.session_state.user_level = user["level"]
                    st.success(f"Welcome back, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            
            if demo_clicked:
                demo_user = ENTERPRISE_USERS["admin@astralytiq.com"].copy()
                demo_user['email'] = "admin@astralytiq.com"
                st.session_state.authenticated = True
                st.session_state.current_user = demo_user
                st.session_state.user_level = "Advanced"
                st.success("Welcome to Enterprise Demo!")
                st.rerun()
        
        # Enterprise features showcase
        st.markdown("### Platform Capabilities")
        
        features = [
            "🤖 Advanced ML Model Training & Deployment",
            "📊 Real-time Analytics & Monitoring", 
            "🔒 Enterprise Security & Compliance",
            "⚡ Auto-scaling Infrastructure",
            "🔄 CI/CD Pipeline Integration",
            "📈 Business Intelligence Dashboards"
        ]
        
        for feature in features:
            st.markdown(f"- {feature}")
        
        st.markdown("### Demo Credentials")
        st.code("""
Email: admin@astralytiq.com
Password: admin123

Email: data.scientist@astralytiq.com  
Password: ds123
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_enterprise_dashboard():
    """Enterprise-grade dashboard with advanced metrics."""
    st.markdown("""
    <div class="enterprise-header">
        <h1>📊 Executive Dashboard</h1>
        <p>Real-time Enterprise MLOps Metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show loading state briefly for demonstration
    if 'dashboard_loaded' not in st.session_state:
        render_loading_state("Loading enterprise metrics...")
        time.sleep(0.5)  # Brief loading simulation
        st.session_state.dashboard_loaded = True
        st.rerun()
    
    demo_data = st.session_state.demo_data
    metrics = demo_data['metrics']
    
    # Enhanced Key Performance Indicators with new components
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(render_enhanced_metric_card(
            title="Data Processed",
            value=f"{metrics['data_processed_tb']} TB",
            subtitle="This month",
            trend=15,
            icon="💾"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_enhanced_metric_card(
            title="Active Models",
            value=str(metrics['active_models']),
            subtitle="Production ready",
            trend=8,
            icon="🤖"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_enhanced_metric_card(
            title="API Calls",
            value=f"{metrics['api_calls_today']:,}",
            subtitle="Today",
            trend=12,
            icon="🔗"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(render_enhanced_metric_card(
            title="Cost Savings",
            value=metrics['cost_savings'],
            subtitle="This quarter",
            trend=23,
            icon="💰"
        ), unsafe_allow_html=True)
    
    # System Status Section with enhanced indicators
    st.markdown("## 🔍 System Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="enhanced-card">
            <h3 style="color: #2d3748; margin-bottom: 1rem;">System Health</h3>
            {render_status_indicator('online', 'All Systems')}
            {render_progress_bar(99.7, 'Uptime')}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="enhanced-card">
            <h3 style="color: #2d3748; margin-bottom: 1rem;">Model Performance</h3>
            {render_status_indicator('deployed', 'Models')}
            {render_progress_bar(92.4, 'Avg Accuracy')}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="enhanced-card">
            <h3 style="color: #2d3748; margin-bottom: 1rem;">Data Quality</h3>
            {render_status_indicator('active', 'Pipelines')}
            {render_progress_bar(96.7, 'Quality Score')}
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="enhanced-card">
            <h3 style="color: #2d3748; margin-bottom: 1rem;">User Activity</h3>
            {render_status_indicator('online', f'{metrics["active_users"]} Users')}
            {render_progress_bar(85, 'Engagement')}
        </div>
        """, unsafe_allow_html=True)
    
    # Advanced visualizations with enhanced styling
    st.markdown("## 📈 Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model performance trends
        models = demo_data['models']
        model_df = pd.DataFrame(models)
        
        fig = px.scatter(
            model_df, 
            x='accuracy', 
            y='requests_per_day',
            size='cost_per_month',
            color='type',
            title="Model Performance vs Usage",
            labels={
                'accuracy': 'Model Accuracy',
                'requests_per_day': 'Daily Requests',
                'cost_per_month': 'Monthly Cost ($)'
            },
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#48cae4', '#f72585', '#4cc9f0']
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            title_font_size=16,
            title_font_color='#2d3748'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Data processing pipeline with enhanced colors
        datasets = demo_data['datasets']
        dataset_df = pd.DataFrame(datasets)
        
        processing_data = dataset_df.groupby('status').size().reset_index(name='count')
        
        fig = px.pie(
            processing_data,
            values='count',
            names='status',
            title="Data Processing Pipeline Status",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            title_font_size=16,
            title_font_color='#2d3748'
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Real-time monitoring with enhanced charts
    st.markdown("## 🔍 Real-time System Monitoring")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Generate real-time CPU data
        cpu_data = np.random.normal(45, 10, 24)
        hours = list(range(24))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, 
            y=cpu_data,
            mode='lines+markers',
            name='CPU Usage (%)',
            line=dict(color='#667eea', width=3),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        fig.update_layout(
            title="CPU Usage (24h)",
            xaxis_title="Hour",
            yaxis_title="Usage (%)",
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            title_font_size=14,
            title_font_color='#2d3748'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Memory usage with gradient fill
        memory_data = np.random.normal(60, 15, 24)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, 
            y=memory_data,
            mode='lines+markers',
            name='Memory Usage (%)',
            line=dict(color='#764ba2', width=3),
            fill='tonexty',
            fillcolor='rgba(118, 75, 162, 0.1)'
        ))
        fig.update_layout(
            title="Memory Usage (24h)",
            xaxis_title="Hour", 
            yaxis_title="Usage (%)",
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            title_font_size=14,
            title_font_color='#2d3748'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # API response times with enhanced styling
        response_times = np.random.normal(150, 30, 24)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours,
            y=response_times,
            mode='lines+markers',
            name='Response Time (ms)',
            line=dict(color='#f093fb', width=3),
            fill='tonexty',
            fillcolor='rgba(240, 147, 251, 0.1)'
        ))
        fig.update_layout(
            title="API Response Time (24h)",
            xaxis_title="Hour",
            yaxis_title="Response Time (ms)",
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            title_font_size=14,
            title_font_color='#2d3748'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Auto-refresh functionality
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.session_state.demo_data = generate_enterprise_demo_data()
        st.session_state.dashboard_loaded = False
        st.rerun()

def show_user_profile():
    """Enterprise user profile with role-based access."""
    if st.session_state.current_user:
        user = st.session_state.current_user
        
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
        st.sidebar.markdown(f"🏢 {user['department']}")
        st.sidebar.markdown(f"⭐ {user['level']} User")
        
        # Session info
        if 'login_time' not in st.session_state:
            st.session_state.login_time = datetime.now()
        
        session_duration = datetime.now() - st.session_state.login_time
        hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        st.sidebar.markdown(f"⏱️ Session: {hours}h {minutes}m")
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.success("Logged out successfully!")
            st.rerun()

def show_navigation():
    """Enterprise navigation with role-based menu."""
    st.sidebar.markdown("### 🧭 Navigation")
    
    nav_options = [
        "📊 Executive Dashboard",
        "🤖 ML Operations", 
        "📈 Analytics & BI",
        "🔧 Data Engineering",
        "🔒 Security & Compliance",
        "⚙️ System Administration"
    ]
    
    selected = st.sidebar.selectbox("Navigate to:", nav_options)
    
    # Platform status
    st.sidebar.markdown("### 📊 Platform Status")
    st.sidebar.markdown("🟢 All Systems Operational")
    st.sidebar.markdown(f"⏱️ Uptime: 99.97%")
    st.sidebar.markdown(f"🔄 Last Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Integration status
    if PRODUCTION_MODE:
        st.sidebar.markdown("### 🔗 Integrations")
        st.sidebar.markdown("✅ Database: Connected")
        st.sidebar.markdown("✅ Storage: Connected") 
        st.sidebar.markdown("✅ OAuth: Configured")
        st.sidebar.markdown("✅ Monitoring: Active")
    
    return selected

def main():
    """Main enterprise application."""
    if not st.session_state.authenticated:
        show_enterprise_login()
        return
    
    # User profile
    show_user_profile()
    
    # Navigation
    selected_page = show_navigation()
    
    # Route to pages
    if "Dashboard" in selected_page:
        show_enterprise_dashboard()
    elif "ML Operations" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>🤖 ML Operations Center</h1>
            <p>Model Training, Deployment & Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 ML Operations interface coming soon - showcasing advanced MLOps capabilities")
    elif "Analytics" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>📈 Business Intelligence</h1>
            <p>Advanced Analytics & Reporting</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 BI Analytics interface coming soon - showcasing enterprise reporting")
    elif "Data Engineering" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>🔧 Data Engineering</h1>
            <p>ETL Pipelines & Data Processing</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 Data Engineering interface coming soon - showcasing pipeline management")
    elif "Security" in selected_page:
        st.markdown("""
        <div class="enterprise-header">
            <h1>🔒 Security & Compliance</h1>
            <p>Access Control & Audit Management</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 Security interface coming soon - showcasing enterprise security features")
    else:
        st.markdown("""
        <div class="enterprise-header">
            <h1>⚙️ System Administration</h1>
            <p>Platform Configuration & Management</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("🚧 Admin interface coming soon - showcasing system management capabilities")

if __name__ == "__main__":
    main()