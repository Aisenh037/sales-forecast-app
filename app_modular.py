"""
🚀 AstralytiQ: Educational MLOps Platform (Modular Version)
Enterprise-grade MLOps platform with modular architecture

This is the modular version that demonstrates clean code organization
while maintaining Streamlit Cloud compatibility.
"""

import streamlit as st
from datetime import datetime

# Import modular components
from components.auth import show_login_form, show_signup_form, show_demo_mode, show_user_profile
from components.dashboard import show_dashboard, show_analytics
from components.data_management import show_data_management
from components.ml_studio import show_ml_studio
from utils.data_generator import generate_demo_data
from utils.auth_utils import register_user, authenticate_user, get_demo_user, clear_session
from utils.navigation import get_navigation_options, show_user_level_selector, show_sidebar_status

# Configuration
st.set_page_config(
    page_title="AstralytiQ - Educational MLOps Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Demo mode configuration
DEMO_MODE = st.secrets.get("DEMO_MODE", "true").lower() == "true"

# Initialize production integrations
try:
    from auth_integrations import AuthManager
    auth_manager = AuthManager()
    PRODUCTION_MODE = auth_manager.get_integration_status()["supabase"] or auth_manager.get_integration_status()["cloudinary"]
except ImportError:
    auth_manager = None
    PRODUCTION_MODE = False

# Professional CSS styling
st.markdown("""
<style>
    /* Professional enterprise theme */
    .stApp {
        background-color: #FAFBFC !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        color: #1a202c;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    .subtitle {
        color: #718096;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .auth-card {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .info-card {
        background: #EBF8FF;
        border: 1px solid #90CDF4;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    .success-card {
        background: #F0FFF4;
        border: 1px solid #9AE6B4;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
    }
    
    /* Professional button styling */
    .stButton > button {
        background-color: #4299E1;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3182CE;
        transform: translateY(-1px);
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #CBD5E0;
        padding: 0.75rem;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 6px;
        border: 1px solid #CBD5E0;
    }
</style>
""", unsafe_allow_html=True)

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
if 'login_time' not in st.session_state:
    st.session_state.login_time = None

def show_login_page():
    """Display enhanced login/signup page with professional enterprise design."""
    st.markdown('<h1 class="main-header">AstralytiQ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Enterprise MLOps Platform</p>', unsafe_allow_html=True)
    
    # Show production status
    if auth_manager:
        status = auth_manager.get_integration_status()
        if status["supabase"] or status["cloudinary"]:
            st.markdown("""
            <div class="success-card">
                <h4 style="margin: 0 0 0.5rem 0; color: #2D3748;">Production Services Active</h4>
                <p style="margin: 0; color: #4A5568;">Database: Connected | Storage: Connected | OAuth: Ready</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Authentication mode selector
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Tab selection for Login/Signup
            auth_mode = st.radio(
                "Authentication Options:",
                ["Login", "Sign Up", "Demo Access"],
                horizontal=True,
                key="auth_mode"
            )
            
            if auth_mode == "Login":
                login_button, forgot_password, email, password = show_login_form()
                
                if login_button:
                    if email and password:
                        user = authenticate_user(email, password, auth_manager)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.current_user = user
                            st.session_state.current_user['email'] = email
                            st.session_state.user_level = user["level"]
                            st.session_state.login_time = datetime.now()
                            st.success(f"Welcome back, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.warning("Please enter both email and password")
                
                if forgot_password:
                    st.info("Password reset functionality will be available soon. Please use demo credentials for now.")
            
            elif auth_mode == "Sign Up":
                signup_result = show_signup_form()
                signup_button, name, email, password, confirm_password, role, level, terms_accepted, newsletter = signup_result
                
                if signup_button:
                    # Validation
                    if not all([name, email, password, confirm_password]):
                        st.error("Please fill in all required fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif not terms_accepted:
                        st.error("Please accept the Terms of Service to continue")
                    elif "@" not in email or "." not in email:
                        st.error("Please enter a valid email address")
                    else:
                        # Attempt registration
                        user = register_user(name, email, password, role, level, auth_manager)
                        if user:
                            st.success("Account created successfully!")
                            st.info("Please switch to Login tab to sign in with your new account")
                            
                            # Show success details
                            st.markdown(f"""
                            <div class="success-card">
                                <h4 style="margin: 0 0 0.5rem 0; color: #2D3748;">Welcome to AstralytiQ, {name}!</h4>
                                <p style="margin: 0; color: #4A5568;"><strong>Email:</strong> {email}</p>
                                <p style="margin: 0; color: #4A5568;"><strong>Role:</strong> {role}</p>
                                <p style="margin: 0; color: #4A5568;"><strong>Level:</strong> {level}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Registration failed. Email may already be registered.")
            
            else:  # Demo Access
                demo_buttons = show_demo_mode()
                
                if demo_buttons['beginner']:
                    demo_user = get_demo_user('Beginner')
                    st.session_state.authenticated = True
                    st.session_state.current_user = demo_user
                    st.session_state.user_level = demo_user["level"]
                    st.session_state.login_time = datetime.now()
                    st.success(f"Welcome to Beginner Demo, {demo_user['name']}!")
                    st.rerun()
                
                elif demo_buttons['intermediate']:
                    demo_user = get_demo_user('Intermediate')
                    st.session_state.authenticated = True
                    st.session_state.current_user = demo_user
                    st.session_state.user_level = demo_user["level"]
                    st.session_state.login_time = datetime.now()
                    st.success(f"Welcome to Intermediate Demo, {demo_user['name']}!")
                    st.rerun()
                
                elif demo_buttons['advanced']:
                    demo_user = get_demo_user('Advanced')
                    st.session_state.authenticated = True
                    st.session_state.current_user = demo_user
                    st.session_state.user_level = demo_user["level"]
                    st.session_state.login_time = datetime.now()
                    st.success(f"Welcome to Advanced Demo, {demo_user['name']}!")
                    st.rerun()
            
            # OAuth integration
            if auth_manager:
                st.markdown("---")
                st.markdown("**Social Authentication**")
                auth_manager.oauth.show_oauth_buttons()
            
            # Demo credentials info
            st.markdown("---")
            st.markdown("""
            <div class="info-card">
                <h4 style="margin: 0 0 0.5rem 0; color: #2B6CB0;">Demo Credentials</h4>
                <p style="margin: 0; color: #2C5282;"><strong>Email:</strong> demo@astralytiq.com</p>
                <p style="margin: 0; color: #2C5282;"><strong>Password:</strong> demo123</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Features preview
            st.markdown("""
            <div class="metric-card">
                <h4 style="margin: 0 0 1rem 0; color: #2D3748;">Platform Capabilities</h4>
                <ul style="margin: 0; color: #4A5568;">
                    <li>ML Model Training & Deployment</li>
                    <li>Data Pipeline Management</li>
                    <li>Analytics & Monitoring</li>
                    <li>Multi-tenant Architecture</li>
                    <li>Enterprise Security</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_header():
    """Display the main header with branding."""
    st.markdown('<h1 class="main-header">AstralytiQ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Educational MLOps Platform - Learn, Build, and Deploy ML</p>', unsafe_allow_html=True)

def main():
    """Main application function."""
    # Check authentication status
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    show_header()
    
    # User profile and logout
    logout_clicked = show_user_profile(st.session_state.current_user)
    if logout_clicked:
        clear_session()
        st.success("Logged out successfully!")
        st.rerun()
    
    # User level selector
    user_level = show_user_level_selector()
    
    # Navigation
    st.sidebar.markdown("### Navigation")
    nav_options = get_navigation_options(user_level)
    selected_page = st.sidebar.selectbox("Choose a page:", nav_options)
    
    # Show user level info
    level_colors = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}
    st.sidebar.markdown(f"**Current Level:** {level_colors[user_level]} {user_level}")
    
    # Show sidebar status
    show_sidebar_status(auth_manager)
    
    # Route to appropriate page
    if selected_page == "Dashboard":
        show_dashboard(st.session_state.demo_data)
    elif selected_page == "Data Management":
        show_data_management(st.session_state.demo_data, auth_manager)
    elif selected_page == "ML Studio":
        show_ml_studio(st.session_state.demo_data, user_level)
    elif selected_page == "Analytics":
        show_analytics(st.session_state.demo_data)
    else:
        # Handle other pages with placeholder content
        st.header(selected_page)
        st.info(f"This is the {selected_page} page. Content coming soon!")
        
        if selected_page == "Data Pipelines":
            st.markdown("""
            ### Data Pipeline Management
            
            **Features:**
            - Visual pipeline builder
            - Automated data transformations
            - Scheduling and monitoring
            - Error handling and recovery
            """)
        
        elif selected_page == "Model Registry":
            st.markdown("""
            ### Centralized Model Registry
            
            **Features:**
            - Model versioning and lineage
            - Performance comparison
            - Deployment tracking
            - Collaboration tools
            """)

if __name__ == "__main__":
    main()