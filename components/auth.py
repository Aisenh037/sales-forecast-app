"""
🔐 Authentication Components
All authentication-related UI components and logic
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Optional

def show_login_form():
    """Display the professional login form."""
    st.markdown("""
    <div class="auth-card">
        <h3 style="text-align: center; margin-bottom: 0.5rem; color: #2D3748;">Welcome Back</h3>
        <p style="text-align: center; margin-bottom: 1.5rem; color: #718096;">Sign in to your account</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="demo@astralytiq.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Sign In", use_container_width=True)
        with col2:
            forgot_password = st.form_submit_button("Forgot Password?", use_container_width=True)
        
        return login_button, forgot_password, email, password

def show_signup_form():
    """Display the professional signup/registration form."""
    st.markdown("""
    <div class="auth-card">
        <h3 style="text-align: center; margin-bottom: 0.5rem; color: #2D3748;">Create Account</h3>
        <p style="text-align: center; margin-bottom: 1.5rem; color: #718096;">Join the AstralytiQ platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email Address", placeholder="john@company.com")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
        
        with col2:
            role = st.selectbox("Role", [
                "Data Scientist", "ML Engineer", "Data Analyst", 
                "Product Manager", "Software Engineer", "Student", "Researcher", "Other"
            ])
            level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        newsletter = st.checkbox("Subscribe to platform updates and insights", value=True)
        
        signup_button = st.form_submit_button("Create Account", use_container_width=True)
        
        return signup_button, name, email, password, confirm_password, role, level, terms_accepted, newsletter

def show_demo_mode():
    """Display demo mode access."""
    st.markdown("""
    <div class="feature-card">
        <h3 style="text-align: center; margin-bottom: 1rem;">Try Demo Mode</h3>
        <p style="text-align: center; margin-bottom: 2rem;">Explore the platform instantly without registration</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    demo_buttons = {}
    with col1:
        demo_buttons['beginner'] = st.button("Beginner Demo", use_container_width=True)
    
    with col2:
        demo_buttons['intermediate'] = st.button("Intermediate Demo", use_container_width=True)
    
    with col3:
        demo_buttons['advanced'] = st.button("Advanced Demo", use_container_width=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>Demo Mode Features</h4>
        <p><strong>Beginner:</strong> Guided tutorials and simple interfaces</p>
        <p><strong>Intermediate:</strong> More features and customization options</p>
        <p><strong>Advanced:</strong> Full platform capabilities and admin features</p>
    </div>
    """, unsafe_allow_html=True)
    
    return demo_buttons

def show_user_profile(user):
    """Show enhanced user profile and logout option."""
    if not user:
        return False
        
    st.sidebar.markdown("### User Profile")
    
    # User avatar (using first letter of name)
    avatar_letter = user['name'][0].upper() if user['name'] else "U"
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
        ">
            {avatar_letter}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown(f"**Name:** {user['name']}")
    st.sidebar.markdown(f"**Email:** {user.get('email', 'N/A')}")
    st.sidebar.markdown(f"**Role:** {user['role']}")
    st.sidebar.markdown(f"**Level:** {user['level']}")
    
    # Session info
    if 'login_time' not in st.session_state:
        st.session_state.login_time = datetime.now()
    
    session_duration = datetime.now() - st.session_state.login_time
    hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    st.sidebar.markdown(f"**Session:** {hours}h {minutes}m")
    
    # Profile actions
    st.sidebar.markdown("---")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        settings_clicked = st.button("Settings", use_container_width=True)
    
    with col2:
        logout_clicked = st.button("Logout", use_container_width=True)
    
    return logout_clicked