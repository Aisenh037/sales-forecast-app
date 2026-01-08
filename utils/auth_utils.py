"""
🔐 Authentication Utilities
Helper functions for user authentication and management
"""

import streamlit as st
from typing import Dict, Optional

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

def register_user(name, email, password, role, level, auth_manager=None):
    """Enhanced user registration function with production integration."""
    
    # Try production registration first
    if auth_manager and hasattr(auth_manager, 'register'):
        try:
            user_data = {
                "name": name,
                "role": role,
                "level": level
            }
            user = auth_manager.register(email, password, user_data)
            if user:
                return user
        except Exception as e:
            st.error(f"⚠️ Production registration error: {str(e)}")
    
    # Fallback to demo registration (add to DEMO_USERS)
    if email not in DEMO_USERS:
        DEMO_USERS[email] = {
            "password": password,
            "name": name,
            "role": role,
            "level": level
        }
        return DEMO_USERS[email]
    else:
        return None  # User already exists

def authenticate_user(email, password, auth_manager=None):
    """Enhanced authentication function with production integration."""
    
    # Try production authentication first
    if auth_manager and hasattr(auth_manager, 'authenticate'):
        try:
            user = auth_manager.authenticate(email, password)
            if user:
                return user
        except Exception as e:
            st.error(f"⚠️ Production auth error: {str(e)}")
    
    # Fallback to demo users
    if email in DEMO_USERS and DEMO_USERS[email]["password"] == password:
        return DEMO_USERS[email]
    return None

def get_demo_user(level: str) -> Dict:
    """Get demo user by experience level."""
    demo_mapping = {
        'Beginner': "jane@company.com",
        'Intermediate': "john@company.com", 
        'Advanced': "demo@astralytiq.com"
    }
    
    email = demo_mapping.get(level, "demo@astralytiq.com")
    user = DEMO_USERS[email].copy()
    user['email'] = email
    return user

def clear_session():
    """Clear all authentication session state."""
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.user_data = {}
    st.session_state.user_level = 'Beginner'
    if 'login_time' in st.session_state:
        del st.session_state.login_time
    if 'show_settings' in st.session_state:
        del st.session_state.show_settings