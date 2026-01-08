#!/usr/bin/env python3
"""
AstralytiQ Development Environment Setup Script

This script sets up the development environment for AstralytiQ Enterprise MLOps Platform.
It handles virtual environment creation, dependency installation, and initial configuration.
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path


def run_command(command, check=True, shell=False):
    """Run a command and handle errors."""
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return None


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")


def check_git():
    """Check if Git is installed."""
    print("📦 Checking Git installation...")
    result = run_command("git --version", check=False)
    if result is None or result.returncode != 0:
        print("❌ Git is not installed. Please install Git first.")
        sys.exit(1)
    print("✅ Git is installed")


def create_virtual_environment():
    """Create Python virtual environment."""
    print("🔧 Creating virtual environment...")
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        return
    
    run_command("python -m venv venv")
    print("✅ Virtual environment created")


def activate_virtual_environment():
    """Get activation command for virtual environment."""
    system = platform.system().lower()
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"


def install_dependencies(dev=True):
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    
    # Determine pip command based on OS
    system = platform.system().lower()
    if system == "windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    run_command(f"{pip_cmd} install --upgrade pip")
    
    # Install requirements
    run_command(f"{pip_cmd} install -r requirements.txt")
    
    if dev:
        print("📦 Installing development dependencies...")
        run_command(f"{pip_cmd} install -r requirements-dev.txt")
    
    print("✅ Dependencies installed")


def setup_pre_commit_hooks():
    """Set up pre-commit hooks."""
    print("🔧 Setting up pre-commit hooks...")
    
    system = platform.system().lower()
    if system == "windows":
        pre_commit_cmd = "venv\\Scripts\\pre-commit"
    else:
        pre_commit_cmd = "venv/bin/pre-commit"
    
    run_command(f"{pre_commit_cmd} install")
    print("✅ Pre-commit hooks installed")


def create_env_file():
    """Create .env file from template."""
    print("⚙️  Setting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        return
    
    if env_example.exists():
        # Copy from example
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created from template")
    else:
        # Create basic .env file
        env_content = """# AstralytiQ Configuration
APP_NAME=AstralytiQ
APP_VERSION=1.0.0
DEBUG=true
DEMO_MODE=true

# Database Configuration (Optional)
# DATABASE_URL=postgresql://user:password@localhost:5432/astralytiq
# MONGODB_URL=mongodb://localhost:27017/astralytiq
# REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# External Services (Optional)
# SUPABASE_URL=your-supabase-url
# SUPABASE_KEY=your-supabase-key
# CLOUDINARY_URL=your-cloudinary-url

# Monitoring
LOG_LEVEL=INFO
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Basic .env file created")


def create_streamlit_config():
    """Create Streamlit configuration."""
    print("🎯 Setting up Streamlit configuration...")
    
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    config_file = streamlit_dir / "config.toml"
    if not config_file.exists():
        config_content = """[server]
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
"""
        with open(config_file, 'w') as f:
            f.write(config_content)
        print("✅ Streamlit config.toml created")
    
    secrets_file = streamlit_dir / "secrets.toml"
    if not secrets_file.exists():
        secrets_content = """# Streamlit Secrets
# Add your sensitive configuration here

[database]
# host = "localhost"
# port = 5432
# database = "astralytiq"
# username = "your_username"
# password = "your_password"

[auth]
# jwt_secret = "your-jwt-secret"
# supabase_url = "your-supabase-url"
# supabase_key = "your-supabase-key"
"""
        with open(secrets_file, 'w') as f:
            f.write(secrets_content)
        print("✅ Streamlit secrets.toml created")


def create_directories():
    """Create necessary directories."""
    print("📁 Creating project directories...")
    
    directories = [
        "data",
        "logs",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "tests/performance",
        "docs",
        "scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Project directories created")


def run_initial_tests():
    """Run initial tests to verify setup."""
    print("🧪 Running initial tests...")
    
    system = platform.system().lower()
    if system == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Test basic imports
    test_script = """
import streamlit
import pandas
import numpy
import plotly
print("✅ All core dependencies imported successfully")
"""
    
    result = run_command(f'{python_cmd} -c "{test_script}"', check=False)
    if result and result.returncode == 0:
        print("✅ Initial tests passed")
    else:
        print("⚠️  Some tests failed, but setup is complete")


def print_next_steps():
    """Print next steps for the user."""
    system = platform.system().lower()
    activate_cmd = activate_virtual_environment()
    
    if system == "windows":
        streamlit_cmd = "venv\\Scripts\\streamlit"
    else:
        streamlit_cmd = "venv/bin/streamlit"
    
    print("\n🎉 Setup complete! Next steps:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print(f"2. Start the application: {streamlit_cmd} run app.py")
    print("3. Open your browser to: http://localhost:8501")
    print("4. Review and update .env file with your configuration")
    print("5. Review and update .streamlit/secrets.toml for sensitive data")
    print("\n📚 Additional commands:")
    print("- Run tests: pytest")
    print("- Format code: black .")
    print("- Lint code: flake8 .")
    print("- Type check: mypy .")
    print("\n🔗 Useful links:")
    print("- Documentation: README.md")
    print("- Contributing: CONTRIBUTING.md")
    print("- Issues: https://github.com/yourusername/astralytiq-enterprise/issues")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="AstralytiQ Development Setup")
    parser.add_argument("--no-dev", action="store_true", help="Skip development dependencies")
    parser.add_argument("--no-hooks", action="store_true", help="Skip pre-commit hooks")
    parser.add_argument("--no-test", action="store_true", help="Skip initial tests")
    args = parser.parse_args()
    
    print("🚀 AstralytiQ Enterprise MLOps Platform Setup")
    print("=" * 50)
    
    # Check prerequisites
    check_python_version()
    check_git()
    
    # Setup environment
    create_virtual_environment()
    install_dependencies(dev=not args.no_dev)
    
    # Setup configuration
    create_env_file()
    create_streamlit_config()
    create_directories()
    
    # Setup development tools
    if not args.no_dev and not args.no_hooks:
        setup_pre_commit_hooks()
    
    # Run tests
    if not args.no_test:
        run_initial_tests()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()