#!/usr/bin/env python3
"""
AstralytiQ Deployment Script

This script handles deployment of AstralytiQ to various environments including
Streamlit Cloud, Docker, and Kubernetes.
"""

import os
import sys
import subprocess
import argparse
import json
import time
from pathlib import Path
from datetime import datetime


def run_command(command, check=True, shell=False, capture_output=True):
    """Run a command and handle errors."""
    try:
        if shell:
            result = subprocess.run(command, shell=True, check=check, capture_output=capture_output, text=True)
        else:
            result = subprocess.run(command.split(), check=check, capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        if capture_output:
            print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return None


def check_prerequisites():
    """Check if required tools are installed."""
    print("🔍 Checking prerequisites...")
    
    tools = {
        "git": "git --version",
        "docker": "docker --version",
        "kubectl": "kubectl version --client"
    }
    
    for tool, command in tools.items():
        result = run_command(command, check=False)
        if result is None or result.returncode != 0:
            print(f"⚠️  {tool} is not installed or not in PATH")
        else:
            print(f"✅ {tool} is available")


def build_docker_image(tag="latest", push=False):
    """Build Docker image."""
    print(f"🐳 Building Docker image with tag: {tag}")
    
    # Build arguments
    build_date = datetime.utcnow().isoformat() + "Z"
    vcs_ref = run_command("git rev-parse --short HEAD").stdout.strip()
    
    build_command = f"""docker build 
        -f Dockerfile.streamlit 
        -t astralytiq:{tag} 
        --build-arg BUILD_DATE={build_date}
        --build-arg VCS_REF={vcs_ref}
        --build-arg VERSION={tag}
        ."""
    
    result = run_command(build_command, shell=True, capture_output=False)
    if result.returncode == 0:
        print(f"✅ Docker image built successfully: astralytiq:{tag}")
        
        if push:
            push_docker_image(tag)
    else:
        print("❌ Docker build failed")
        sys.exit(1)


def push_docker_image(tag="latest"):
    """Push Docker image to registry."""
    print(f"📤 Pushing Docker image: astralytiq:{tag}")
    
    # Tag for registry (adjust registry URL as needed)
    registry_tag = f"ghcr.io/yourusername/astralytiq:{tag}"
    run_command(f"docker tag astralytiq:{tag} {registry_tag}")
    
    # Push to registry
    result = run_command(f"docker push {registry_tag}", capture_output=False)
    if result.returncode == 0:
        print(f"✅ Image pushed successfully: {registry_tag}")
    else:
        print("❌ Docker push failed")
        sys.exit(1)


def deploy_docker_compose(environment="development"):
    """Deploy using Docker Compose."""
    print(f"🚀 Deploying with Docker Compose ({environment})...")
    
    compose_file = "docker-compose.yml"
    if environment == "production":
        compose_file = "docker-compose.prod.yml"
    elif environment == "development":
        compose_file = "docker-compose.dev.yml"
    
    if not Path(compose_file).exists():
        compose_file = "docker-compose.yml"
    
    # Stop existing containers
    run_command(f"docker-compose -f {compose_file} down", check=False)
    
    # Start services
    result = run_command(f"docker-compose -f {compose_file} up -d", capture_output=False)
    if result.returncode == 0:
        print("✅ Docker Compose deployment successful")
        print("🌐 Application should be available at: http://localhost:8501")
    else:
        print("❌ Docker Compose deployment failed")
        sys.exit(1)


def deploy_kubernetes(namespace="astralytiq"):
    """Deploy to Kubernetes."""
    print(f"☸️  Deploying to Kubernetes namespace: {namespace}")
    
    k8s_dir = Path("k8s")
    if not k8s_dir.exists():
        print("❌ Kubernetes manifests directory not found")
        sys.exit(1)
    
    # Apply manifests
    manifests = [
        "namespace.yaml",
        "deployment.yaml",
        "service.yaml",
        "ingress.yaml"
    ]
    
    for manifest in manifests:
        manifest_path = k8s_dir / manifest
        if manifest_path.exists():
            print(f"📄 Applying {manifest}...")
            result = run_command(f"kubectl apply -f {manifest_path}")
            if result.returncode != 0:
                print(f"❌ Failed to apply {manifest}")
                sys.exit(1)
        else:
            print(f"⚠️  {manifest} not found, skipping...")
    
    print("✅ Kubernetes deployment successful")
    
    # Wait for deployment to be ready
    print("⏳ Waiting for deployment to be ready...")
    run_command(f"kubectl rollout status deployment/astralytiq-streamlit -n {namespace}", capture_output=False)
    
    # Get service information
    print("📊 Getting service information...")
    run_command(f"kubectl get services -n {namespace}", capture_output=False)


def deploy_streamlit_cloud():
    """Deploy to Streamlit Cloud."""
    print("☁️  Preparing for Streamlit Cloud deployment...")
    
    # Check if we're in a git repository
    result = run_command("git status", check=False)
    if result.returncode != 0:
        print("❌ Not in a git repository. Streamlit Cloud requires git.")
        sys.exit(1)
    
    # Check if there are uncommitted changes
    result = run_command("git status --porcelain")
    if result.stdout.strip():
        print("⚠️  You have uncommitted changes. Consider committing them first.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Push to main branch
    print("📤 Pushing to main branch...")
    current_branch = run_command("git branch --show-current").stdout.strip()
    
    if current_branch != "main":
        print(f"⚠️  Current branch is '{current_branch}', not 'main'")
        response = input("Push current branch to main? (y/N): ")
        if response.lower() == 'y':
            run_command("git push origin HEAD:main", capture_output=False)
        else:
            print("Please switch to main branch or push your changes to main")
            sys.exit(1)
    else:
        run_command("git push origin main", capture_output=False)
    
    print("✅ Code pushed to main branch")
    print("🌐 Now go to https://share.streamlit.io to deploy your app")
    print("📋 Repository URL: " + run_command("git remote get-url origin").stdout.strip())


def run_health_check(url="http://localhost:8501"):
    """Run health check on deployed application."""
    print(f"🏥 Running health check on {url}...")
    
    try:
        import requests
        response = requests.get(f"{url}/_stcore/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except ImportError:
        print("⚠️  requests library not available, skipping health check")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def run_smoke_tests():
    """Run basic smoke tests."""
    print("🧪 Running smoke tests...")
    
    # Test basic imports
    test_script = """
import sys
sys.path.append('.')
try:
    import app
    print("✅ App module imported successfully")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)
"""
    
    result = run_command(f'python -c "{test_script}"')
    if result.returncode == 0:
        print("✅ Smoke tests passed")
        return True
    else:
        print("❌ Smoke tests failed")
        return False


def cleanup_old_resources():
    """Clean up old Docker images and containers."""
    print("🧹 Cleaning up old resources...")
    
    # Remove old containers
    run_command("docker container prune -f", check=False)
    
    # Remove old images
    run_command("docker image prune -f", check=False)
    
    print("✅ Cleanup completed")


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="AstralytiQ Deployment Script")
    parser.add_argument("target", choices=["docker", "compose", "k8s", "streamlit"], 
                       help="Deployment target")
    parser.add_argument("--environment", "-e", default="development",
                       choices=["development", "staging", "production"],
                       help="Deployment environment")
    parser.add_argument("--tag", "-t", default="latest",
                       help="Docker image tag")
    parser.add_argument("--push", action="store_true",
                       help="Push Docker image to registry")
    parser.add_argument("--no-build", action="store_true",
                       help="Skip building Docker image")
    parser.add_argument("--no-tests", action="store_true",
                       help="Skip running tests")
    parser.add_argument("--cleanup", action="store_true",
                       help="Clean up old resources")
    
    args = parser.parse_args()
    
    print("🚀 AstralytiQ Deployment Script")
    print("=" * 40)
    print(f"Target: {args.target}")
    print(f"Environment: {args.environment}")
    print(f"Tag: {args.tag}")
    print("=" * 40)
    
    # Check prerequisites
    check_prerequisites()
    
    # Cleanup if requested
    if args.cleanup:
        cleanup_old_resources()
    
    # Run smoke tests
    if not args.no_tests:
        if not run_smoke_tests():
            print("❌ Smoke tests failed, aborting deployment")
            sys.exit(1)
    
    # Deploy based on target
    if args.target == "docker":
        if not args.no_build:
            build_docker_image(args.tag, args.push)
        
        # Run container
        print("🚀 Running Docker container...")
        run_command("docker stop astralytiq", check=False)
        run_command("docker rm astralytiq", check=False)
        
        run_command(f"""docker run -d 
            --name astralytiq 
            -p 8501:8501 
            -e DEMO_MODE=true 
            astralytiq:{args.tag}""", shell=True, capture_output=False)
        
        # Wait a bit for container to start
        time.sleep(5)
        run_health_check()
        
    elif args.target == "compose":
        if not args.no_build:
            build_docker_image(args.tag)
        deploy_docker_compose(args.environment)
        time.sleep(10)
        run_health_check()
        
    elif args.target == "k8s":
        if not args.no_build:
            build_docker_image(args.tag, True)  # Push for k8s
        deploy_kubernetes()
        
    elif args.target == "streamlit":
        deploy_streamlit_cloud()
    
    print("\n🎉 Deployment completed successfully!")
    
    # Print access information
    if args.target in ["docker", "compose"]:
        print("🌐 Application URL: http://localhost:8501")
    elif args.target == "k8s":
        print("☸️  Check kubectl get services for access information")
    elif args.target == "streamlit":
        print("☁️  Check Streamlit Cloud dashboard for deployment status")


if __name__ == "__main__":
    main()