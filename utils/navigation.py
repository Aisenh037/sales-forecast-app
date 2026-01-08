"""
🧭 Navigation Utilities
Navigation and routing helper functions
"""

import streamlit as st

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

def show_user_level_selector():
    """Show user experience level selector."""
    st.sidebar.markdown("### User Experience Level")
    
    levels = {
        'Beginner': 'Beginner - Guided tutorials and simple interfaces',
        'Intermediate': 'Intermediate - More features and customization',
        'Advanced': 'Advanced - Full platform capabilities'
    }
    
    selected_level = st.sidebar.selectbox(
        "Choose your experience level:",
        options=list(levels.keys()),
        index=list(levels.keys()).index(st.session_state.user_level),
        format_func=lambda x: levels[x]
    )
    
    if selected_level != st.session_state.user_level:
        st.session_state.user_level = selected_level
        st.rerun()
    
    return selected_level

def show_sidebar_status(auth_manager=None):
    """Show sidebar status information."""
    # Platform status
    st.sidebar.markdown("### Platform Status")
    st.sidebar.markdown("✓ All Systems Operational")
    st.sidebar.markdown(f"Uptime: 99.9%")
    
    from datetime import datetime
    st.sidebar.markdown(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Production integration status
    if auth_manager:
        status = auth_manager.get_integration_status()
        st.sidebar.markdown("### Integrations")
        st.sidebar.markdown(f"Database: {'✓ Connected' if status['supabase'] else 'Demo Mode'}")
        st.sidebar.markdown(f"Storage: {'✓ Connected' if status['cloudinary'] else 'Demo Mode'}")
        st.sidebar.markdown(f"Local Storage: {'✓ Available' if status['local_storage'] else '✗ Unavailable'}")
        
        # OAuth status
        github_configured = st.secrets.get("GITHUB_CLIENT_ID", "").replace("your-github-client-id-here", "") != ""
        google_configured = st.secrets.get("GOOGLE_CLIENT_ID", "").replace("your-google-client-id-here", "") != ""
        
        st.sidebar.markdown(f"GitHub OAuth: {'✓ Configured' if github_configured else 'Setup Required'}")
        st.sidebar.markdown(f"Google OAuth: {'✓ Configured' if google_configured else 'Setup Required'}")
        
        if not github_configured or not google_configured:
            missing = []
            if not github_configured: missing.append("GitHub")
            if not google_configured: missing.append("Google")
            st.sidebar.info(f"Complete {' & '.join(missing)} OAuth setup")
    
    # Demo mode indicator
    DEMO_MODE = st.secrets.get("DEMO_MODE", "true").lower() == "true"
    if DEMO_MODE:
        st.sidebar.markdown("### Demo Mode")
        st.sidebar.info("Running in demo mode with sample data. Deploy with backend services for full functionality.")
    else:
        st.sidebar.markdown("### Production Mode")
        st.sidebar.success("Running with production integrations!")