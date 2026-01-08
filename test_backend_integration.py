#!/usr/bin/env python3
"""
🧪 Backend Integration Test Suite
Tests the FastAPI backend integration with comprehensive validation

Demonstrates:
- API endpoint testing
- Authentication flow validation
- Database operations testing
- Error handling verification
- Performance benchmarking
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class BackendTester:
    """Comprehensive backend testing suite."""
    
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = "", duration: float = 0):
        """Log test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        duration_str = f" ({duration:.2f}s)" if duration > 0 else ""
        print(f"{status} {test_name}{duration_str}")
        if message:
            print(f"    {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_health_check(self) -> bool:
        """Test basic health check endpoint."""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True, f"Service healthy", duration)
                    return True
                else:
                    self.log_test("Health Check", False, f"Unhealthy status: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Connection failed: {str(e)}")
            return False
    
    def test_detailed_health_check(self) -> bool:
        """Test detailed health check endpoint."""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/health/detailed", timeout=5)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                components = data.get("components", {})
                
                # Check database status
                db_status = components.get("database", "unknown")
                if "healthy" in db_status:
                    self.log_test("Detailed Health Check", True, 
                                f"All components healthy, DB: {db_status}", duration)
                    return True
                else:
                    self.log_test("Detailed Health Check", False, 
                                f"Database unhealthy: {db_status}")
                    return False
            else:
                self.log_test("Detailed Health Check", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Detailed Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_authentication(self) -> bool:
        """Test user authentication flow."""
        try:
            # Test login
            start_time = time.time()
            login_data = {
                "email": "admin@astralytiq.com",
                "password": "admin123"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                json=login_data,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["access_token", "token_type", "expires_in", "user"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Authentication", False, 
                                f"Missing fields: {missing_fields}")
                    return False
                
                # Store token for subsequent tests
                self.access_token = data["access_token"]
                user = data["user"]
                
                self.log_test("Authentication", True, 
                            f"Login successful for {user['name']}", duration)
                return True
            else:
                self.log_test("Authentication", False, 
                            f"Login failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_protected_endpoint(self) -> bool:
        """Test protected endpoint with JWT token."""
        if not self.access_token:
            self.log_test("Protected Endpoint", False, "No access token available")
            return False
        
        try:
            start_time = time.time()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = self.session.get(
                f"{self.base_url}/api/v1/auth/me",
                headers=headers,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate user data
                required_fields = ["id", "email", "name", "role"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Protected Endpoint", False, 
                                f"Missing user fields: {missing_fields}")
                    return False
                
                self.log_test("Protected Endpoint", True, 
                            f"User data retrieved for {data['name']}", duration)
                return True
            else:
                self.log_test("Protected Endpoint", False, 
                            f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Protected Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_datasets_endpoint(self) -> bool:
        """Test datasets API endpoint."""
        if not self.access_token:
            self.log_test("Datasets API", False, "No access token available")
            return False
        
        try:
            start_time = time.time()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = self.session.get(
                f"{self.base_url}/api/v1/datasets",
                headers=headers,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Datasets API", True, 
                                f"Retrieved {len(data)} datasets", duration)
                    return True
                else:
                    self.log_test("Datasets API", False, 
                                f"Expected list, got {type(data)}")
                    return False
            else:
                self.log_test("Datasets API", False, 
                            f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Datasets API", False, f"Error: {str(e)}")
            return False
    
    def test_models_endpoint(self) -> bool:
        """Test ML models API endpoint."""
        if not self.access_token:
            self.log_test("Models API", False, "No access token available")
            return False
        
        try:
            start_time = time.time()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = self.session.get(
                f"{self.base_url}/api/v1/models",
                headers=headers,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Models API", True, 
                                f"Retrieved {len(data)} models", duration)
                    return True
                else:
                    self.log_test("Models API", False, 
                                f"Expected list, got {type(data)}")
                    return False
            else:
                self.log_test("Models API", False, 
                            f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Models API", False, f"Error: {str(e)}")
            return False
    
    def test_metrics_endpoint(self) -> bool:
        """Test metrics API endpoint."""
        if not self.access_token:
            self.log_test("Metrics API", False, "No access token available")
            return False
        
        try:
            start_time = time.time()
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            response = self.session.get(
                f"{self.base_url}/api/v1/metrics",
                headers=headers,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate metrics structure
                required_fields = [
                    "total_datasets", "active_models", "total_dashboards",
                    "api_calls_today", "uptime_percentage"
                ]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Metrics API", False, 
                                f"Missing metrics: {missing_fields}")
                    return False
                
                self.log_test("Metrics API", True, 
                            f"All metrics available", duration)
                return True
            else:
                self.log_test("Metrics API", False, 
                            f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Metrics API", False, f"Error: {str(e)}")
            return False
    
    def test_invalid_authentication(self) -> bool:
        """Test invalid authentication handling."""
        try:
            start_time = time.time()
            login_data = {
                "email": "invalid@example.com",
                "password": "wrongpassword"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                json=login_data,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 401:
                self.log_test("Invalid Authentication", True, 
                            "Correctly rejected invalid credentials", duration)
                return True
            else:
                self.log_test("Invalid Authentication", False, 
                            f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Invalid Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_unauthorized_access(self) -> bool:
        """Test unauthorized access to protected endpoints."""
        try:
            start_time = time.time()
            
            # Try to access protected endpoint without token
            response = self.session.get(
                f"{self.base_url}/api/v1/datasets",
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 403:
                self.log_test("Unauthorized Access", True, 
                            "Correctly blocked unauthorized access", duration)
                return True
            else:
                self.log_test("Unauthorized Access", False, 
                            f"Expected 403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Unauthorized Access", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return summary."""
        print("🧪 Starting Backend Integration Tests...")
        print("=" * 50)
        
        # Core functionality tests
        tests = [
            self.test_health_check,
            self.test_detailed_health_check,
            self.test_authentication,
            self.test_protected_endpoint,
            self.test_datasets_endpoint,
            self.test_models_endpoint,
            self.test_metrics_endpoint,
            self.test_invalid_authentication,
            self.test_unauthorized_access
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed += 1
        
        # Generate summary
        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT! Backend is production-ready!")
        elif success_rate >= 70:
            print("👍 GOOD! Minor issues to address")
        else:
            print("⚠️  NEEDS WORK! Major issues detected")
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "success_rate": success_rate,
            "results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Main test execution."""
    print("""
    🚀 AstralytiQ Backend Integration Test Suite
    ==========================================
    
    Testing FastAPI backend for campus placement demo
    """)
    
    # Check if backend is running
    tester = BackendTester()
    
    print("🔍 Checking if backend is running...")
    if not tester.test_health_check():
        print("""
        ❌ Backend is not running!
        
        To start the backend:
        1. cd backend
        2. python main.py
        
        Or use the full-stack starter:
        python start_full_stack.py
        """)
        sys.exit(1)
    
    # Run all tests
    summary = tester.run_all_tests()
    
    # Save results
    with open("test_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Test results saved to: test_results.json")
    
    # Exit with appropriate code
    if summary["success_rate"] >= 90:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()