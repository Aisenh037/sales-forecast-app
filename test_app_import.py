#!/usr/bin/env python3
"""
Test script to verify app.py imports and basic functionality
"""

import sys
import traceback

def test_imports():
    """Test if all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import streamlit as st
        print("✓ Streamlit imported successfully")
        
        import pandas as pd
        print("✓ Pandas imported successfully")
        
        import plotly.express as px
        print("✓ Plotly imported successfully")
        
        import numpy as np
        print("✓ NumPy imported successfully")
        
        # Test auth integrations import
        from auth_integrations import AuthManager
        print("✓ AuthManager imported successfully")
        
        # Test auth manager initialization
        auth_manager = AuthManager()
        print("✓ AuthManager initialized successfully")
        
        # Test integration status
        status = auth_manager.get_integration_status()
        print(f"✓ Integration status: {status}")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        traceback.print_exc()
        return False

def test_demo_data():
    """Test demo data generation."""
    try:
        print("\nTesting demo data generation...")
        
        # Import the demo data function
        sys.path.append('.')
        from app import generate_demo_data
        
        demo_data = generate_demo_data()
        print(f"✓ Demo data generated with {len(demo_data['datasets'])} datasets")
        print(f"✓ Demo data generated with {len(demo_data['models'])} models")
        print(f"✓ Demo data generated with {len(demo_data['dashboards'])} dashboards")
        
        return True
        
    except Exception as e:
        print(f"✗ Demo data error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("AstralytiQ App Test Suite")
    print("=" * 40)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test demo data
    if not test_demo_data():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed! App should work correctly.")
    else:
        print("✗ Some tests failed. Check the errors above.")
    
    sys.exit(0 if success else 1)