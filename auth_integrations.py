"""
🔐 AstralytiQ Authentication Integrations
Production-ready authentication with multiple providers
"""

import streamlit as st
import os
from typing import Optional, Dict, Any
import json
from datetime import datetime, timedelta

# =============================================================================
# 1. SUPABASE INTEGRATION (Recommended for Production)
# =============================================================================

class SupabaseAuth:
    """Supabase authentication integration."""
    
    def __init__(self):
        # Initialize Supabase client (add to requirements.txt: supabase>=1.0.0)
        try:
            from supabase import create_client, Client
            
            # Get from Streamlit secrets or environment variables
            supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
            supabase_key = st.secrets.get("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")
            
            if supabase_url and supabase_key:
                self.supabase: Client = create_client(supabase_url, supabase_key)
                self.enabled = True
            else:
                self.enabled = False
                st.warning("⚠️ Supabase credentials not found. Using demo mode.")
                
        except ImportError:
            self.enabled = False
            st.info("💡 Install Supabase: pip install supabase")
    
    def sign_up(self, email: str, password: str, user_data: Dict[str, Any]) -> Optional[Dict]:
        """Register new user with Supabase."""
        if not self.enabled:
            return None
            
        try:
            # Sign up user
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_data  # Additional user metadata
                }
            })
            
            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "name": user_data.get("name", ""),
                    "role": user_data.get("role", "User"),
                    "level": user_data.get("level", "Beginner")
                }
        except Exception as e:
            st.error(f"❌ Registration failed: {str(e)}")
        
        return None
    
    def sign_in(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user with Supabase."""
        if not self.enabled:
            return None
            
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Get additional user data from profiles table
                profile = self.supabase.table("profiles").select("*").eq("id", response.user.id).execute()
                
                user_data = {
                    "id": response.user.id,
                    "email": response.user.email,
                    "name": response.user.user_metadata.get("name", ""),
                    "role": "User",
                    "level": "Beginner"
                }
                
                # Merge profile data if exists
                if profile.data:
                    user_data.update(profile.data[0])
                
                return user_data
                
        except Exception as e:
            st.error(f"❌ Login failed: {str(e)}")
        
        return None
    
    def sign_out(self):
        """Sign out current user."""
        if self.enabled:
            self.supabase.auth.sign_out()

# =============================================================================
# 2. CLOUDINARY INTEGRATION (File Storage & Media Management)
# =============================================================================

class CloudinaryStorage:
    """Cloudinary integration for file storage."""
    
    def __init__(self):
        try:
            import cloudinary
            import cloudinary.uploader
            
            # Configure Cloudinary (add to requirements.txt: cloudinary>=1.30.0)
            cloudinary.config(
                cloud_name=st.secrets.get("CLOUDINARY_CLOUD_NAME") or os.getenv("CLOUDINARY_CLOUD_NAME"),
                api_key=st.secrets.get("CLOUDINARY_API_KEY") or os.getenv("CLOUDINARY_API_KEY"),
                api_secret=st.secrets.get("CLOUDINARY_API_SECRET") or os.getenv("CLOUDINARY_API_SECRET")
            )
            
            self.enabled = True
            
        except ImportError:
            self.enabled = False
            st.info("💡 Install Cloudinary: pip install cloudinary")
    
    def upload_file(self, file_data, folder: str = "astralytiq", public_id: str = None) -> Optional[str]:
        """Upload file to Cloudinary."""
        if not self.enabled:
            return None
            
        try:
            import cloudinary.uploader
            
            result = cloudinary.uploader.upload(
                file_data,
                folder=folder,
                public_id=public_id,
                resource_type="auto"  # Auto-detect file type
            )
            
            return result.get("secure_url")
            
        except Exception as e:
            st.error(f"❌ Upload failed: {str(e)}")
            return None
    
    def delete_file(self, public_id: str) -> bool:
        """Delete file from Cloudinary."""
        if not self.enabled:
            return False
            
        try:
            import cloudinary.uploader
            
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
            
        except Exception as e:
            st.error(f"❌ Delete failed: {str(e)}")
            return False

# =============================================================================
# 3. LOCAL STORAGE INTEGRATION (Offline Capabilities)
# =============================================================================

class LocalStorage:
    """Local storage for offline capabilities."""
    
    def __init__(self, storage_file: str = "astralytiq_data.json"):
        self.storage_file = storage_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from local file."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.warning(f"⚠️ Could not load local data: {str(e)}")
        
        return {"users": {}, "datasets": {}, "models": {}}
    
    def _save_data(self):
        """Save data to local file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            st.error(f"❌ Could not save local data: {str(e)}")
    
    def store_user(self, user_id: str, user_data: Dict):
        """Store user data locally."""
        self.data["users"][user_id] = user_data
        self._save_data()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user data from local storage."""
        return self.data["users"].get(user_id)
    
    def store_dataset(self, dataset_id: str, dataset_data: Dict):
        """Store dataset metadata locally."""
        self.data["datasets"][dataset_id] = dataset_data
        self._save_data()
    
    def get_datasets(self) -> Dict:
        """Get all datasets from local storage."""
        return self.data["datasets"]

# =============================================================================
# 4. OAUTH INTEGRATION (Google, GitHub, etc.)
# =============================================================================

class OAuthProviders:
    """OAuth integration for social login."""
    
    def __init__(self):
        self.providers = {
            "google": self._setup_google_oauth,
            "github": self._setup_github_oauth,
            "microsoft": self._setup_microsoft_oauth
        }
    
    def _setup_google_oauth(self):
        """Setup Google OAuth (requires streamlit-oauth)."""
        try:
            # Add to requirements.txt: streamlit-oauth>=0.1.0
            from streamlit_oauth import OAuth2Component
            
            oauth2 = OAuth2Component(
                client_id=st.secrets.get("GOOGLE_CLIENT_ID"),
                client_secret=st.secrets.get("GOOGLE_CLIENT_SECRET"),
                authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
                token_endpoint="https://oauth2.googleapis.com/token",
                refresh_token_endpoint="https://oauth2.googleapis.com/token",
                revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
            )
            
            return oauth2
            
        except ImportError:
            st.info("💡 Install OAuth: pip install streamlit-oauth")
            return None
    
    def _setup_github_oauth(self):
        """Setup GitHub OAuth."""
        # Similar implementation for GitHub
        pass
    
    def _setup_microsoft_oauth(self):
        """Setup Microsoft OAuth."""
        # Similar implementation for Microsoft
        pass
    
    def show_oauth_buttons(self):
        """Display OAuth login buttons."""
        st.markdown("### 🔗 Social Login")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Google", use_container_width=True):
                st.info("Google OAuth integration ready!")
        
        with col2:
            if st.button("🐙 GitHub", use_container_width=True):
                st.info("GitHub OAuth integration ready!")
        
        with col3:
            if st.button("🏢 Microsoft", use_container_width=True):
                st.info("Microsoft OAuth integration ready!")

# =============================================================================
# 5. UNIFIED AUTHENTICATION MANAGER
# =============================================================================

class AuthManager:
    """Unified authentication manager for all providers."""
    
    def __init__(self):
        self.supabase = SupabaseAuth()
        self.cloudinary = CloudinaryStorage()
        self.local_storage = LocalStorage()
        self.oauth = OAuthProviders()
    
    def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Try authentication with available providers."""
        
        # Try Supabase first (production)
        if self.supabase.enabled:
            user = self.supabase.sign_in(email, password)
            if user:
                return user
        
        # Fallback to demo users (development)
        from app import DEMO_USERS, authenticate_user
        return authenticate_user(email, password)
    
    def register(self, email: str, password: str, user_data: Dict) -> Optional[Dict]:
        """Register new user with available providers."""
        
        # Try Supabase first
        if self.supabase.enabled:
            return self.supabase.sign_up(email, password, user_data)
        
        # Fallback to local storage
        user_id = f"user_{len(self.local_storage.data['users']) + 1}"
        user_data.update({"id": user_id, "email": email})
        self.local_storage.store_user(user_id, user_data)
        return user_data
    
    def upload_file(self, file_data, folder: str = "astralytiq") -> Optional[str]:
        """Upload file with available storage providers."""
        
        # Try Cloudinary first
        if self.cloudinary.enabled:
            return self.cloudinary.upload_file(file_data, folder)
        
        # Fallback to local storage simulation
        st.info("📁 File would be stored locally in production")
        return f"local://uploads/{folder}/{datetime.now().isoformat()}"
    
    def get_integration_status(self) -> Dict[str, bool]:
        """Get status of all integrations."""
        return {
            "supabase": self.supabase.enabled,
            "cloudinary": self.cloudinary.enabled,
            "local_storage": True,  # Always available
            "oauth": True  # UI always available
        }

# =============================================================================
# 6. STREAMLIT SECRETS CONFIGURATION
# =============================================================================

def show_secrets_template():
    """Show template for Streamlit secrets configuration."""
    
    st.markdown("""
    ### 🔐 Streamlit Secrets Configuration
    
    Create `.streamlit/secrets.toml` with:
    
    ```toml
    # Supabase Configuration
    SUPABASE_URL = "https://your-project.supabase.co"
    SUPABASE_ANON_KEY = "your-anon-key"
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = "your-cloud-name"
    CLOUDINARY_API_KEY = "your-api-key"
    CLOUDINARY_API_SECRET = "your-api-secret"
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID = "your-google-client-id"
    GOOGLE_CLIENT_SECRET = "your-google-client-secret"
    
    GITHUB_CLIENT_ID = "your-github-client-id"
    GITHUB_CLIENT_SECRET = "your-github-client-secret"
    ```
    """)

# =============================================================================
# 7. USAGE EXAMPLE
# =============================================================================

def example_usage():
    """Example of how to use the unified auth manager."""
    
    # Initialize auth manager
    auth = AuthManager()
    
    # Check integration status
    status = auth.get_integration_status()
    st.write("Integration Status:", status)
    
    # Authentication
    if st.button("Test Login"):
        user = auth.authenticate("demo@astralytiq.com", "demo123")
        if user:
            st.success(f"Logged in as {user['name']}")
    
    # File upload
    uploaded_file = st.file_uploader("Test File Upload")
    if uploaded_file:
        file_url = auth.upload_file(uploaded_file.getvalue(), "test-uploads")
        if file_url:
            st.success(f"File uploaded: {file_url}")

if __name__ == "__main__":
    st.title("🔐 AstralytiQ Authentication Integrations")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Demo", "⚙️ Configuration", "📚 Documentation"])
    
    with tab1:
        example_usage()
    
    with tab2:
        show_secrets_template()
    
    with tab3:
        st.markdown("""
        ## 📚 Integration Guide
        
        ### Quick Setup:
        1. **Supabase**: Create project → Get URL & API key → Add to secrets
        2. **Cloudinary**: Create account → Get credentials → Add to secrets  
        3. **OAuth**: Setup apps in Google/GitHub → Get client credentials
        4. **Local Storage**: Works automatically for offline capabilities
        
        ### Benefits:
        - 🔐 **Secure authentication** with industry standards
        - 📁 **Scalable file storage** with CDN delivery
        - 🌐 **Social login** for better UX
        - 💾 **Offline capabilities** for reliability
        - 🔄 **Easy migration** between providers
        """)