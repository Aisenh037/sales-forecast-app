"""
Basic tests for AstralytiQ application.
"""

import pytest
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all required packages can be imported."""
    try:
        import streamlit
        import pandas
        import numpy
        import plotly
        import plotly.express
        import plotly.graph_objects
    except ImportError as e:
        pytest.fail(f"Failed to import required package: {e}")


def test_app_structure():
    """Test that the main app file exists and has basic structure."""
    app_file = project_root / "app.py"
    assert app_file.exists(), "app.py file should exist"
    
    with open(app_file, 'r') as f:
        content = f.read()
        
    # Check for essential components
    assert "import streamlit" in content, "Should import streamlit"
    assert "def main" in content, "Should have main function"
    assert "if __name__ == \"__main__\"" in content, "Should have main guard"


def test_requirements_files():
    """Test that requirements files exist."""
    requirements_file = project_root / "requirements.txt"
    dev_requirements_file = project_root / "requirements-dev.txt"
    
    assert requirements_file.exists(), "requirements.txt should exist"
    assert dev_requirements_file.exists(), "requirements-dev.txt should exist"


def test_docker_files():
    """Test that Docker configuration files exist."""
    dockerfile = project_root / "Dockerfile.streamlit"
    docker_compose = project_root / "docker-compose.yml"
    
    assert dockerfile.exists(), "Dockerfile.streamlit should exist"
    assert docker_compose.exists(), "docker-compose.yml should exist"


def test_github_workflows():
    """Test that GitHub workflow files exist."""
    ci_workflow = project_root / ".github" / "workflows" / "ci.yml"
    cd_workflow = project_root / ".github" / "workflows" / "cd.yml"
    
    assert ci_workflow.exists(), "CI workflow should exist"
    assert cd_workflow.exists(), "CD workflow should exist"


def test_documentation_files():
    """Test that documentation files exist."""
    readme = project_root / "README.md"
    contributing = project_root / "CONTRIBUTING.md"
    license_file = project_root / "LICENSE"
    
    assert readme.exists(), "README.md should exist"
    assert contributing.exists(), "CONTRIBUTING.md should exist"
    assert license_file.exists(), "LICENSE should exist"


def test_kubernetes_manifests():
    """Test that Kubernetes manifests exist."""
    k8s_dir = project_root / "k8s"
    
    assert k8s_dir.exists(), "k8s directory should exist"
    assert (k8s_dir / "namespace.yaml").exists(), "namespace.yaml should exist"
    assert (k8s_dir / "deployment.yaml").exists(), "deployment.yaml should exist"
    assert (k8s_dir / "service.yaml").exists(), "service.yaml should exist"
    assert (k8s_dir / "ingress.yaml").exists(), "ingress.yaml should exist"


if __name__ == "__main__":
    pytest.main([__file__])