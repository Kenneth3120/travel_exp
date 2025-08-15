#!/usr/bin/env python3
"""
Frontend Integration Test - Test the complete login flow and data loading
"""

import requests
import sys
import json
import time

class FrontendIntegrationTester:
    def __init__(self):
        self.backend_url = "http://localhost:8001/api"
        self.frontend_url = "http://127.0.0.1:4208"
        self.access_token = None
        self.tests_run = 0
        self.tests_passed = 0
    
    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        if details:
            print(f"   Details: {details}")
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                content = response.text
                if "AAP Administration" in content and "ng-app" in content:
                    self.log_test("Frontend Accessibility", True, "Frontend is serving AngularJS app")
                    return True
                else:
                    self.log_test("Frontend Accessibility", False, "Frontend not serving expected content")
                    return False
            else:
                self.log_test("Frontend Accessibility", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Accessibility", False, f"Exception: {str(e)}")
            return False
    
    def test_backend_login_flow(self):
        """Test the complete login flow that frontend would use"""
        try:
            # Test login endpoint
            login_data = {"username": "admin", "password": "admin123"}
            response = requests.post(f"{self.backend_url}/login/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                self.log_test("Backend Login Flow", True, f"User: {data['user']['username']}")
                return True
            else:
                self.log_test("Backend Login Flow", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Login Flow", False, f"Exception: {str(e)}")
            return False
    
    def test_authenticated_endpoints(self):
        """Test endpoints that the frontend dashboard would call"""
        if not self.access_token:
            self.log_test("Authenticated Endpoints", False, "No access token available")
            return False
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        endpoints = [
            ("User Info", "/user-info/"),
            ("Tower Instances", "/instances/"),
            ("Credentials", "/credentials/"),
            ("Execution Environments", "/environments/"),
            ("Audit Logs", "/audit-logs/"),
        ]
        
        all_passed = True
        for name, endpoint in endpoints:
            try:
                response = requests.get(f"{self.backend_url}{endpoint}", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    count = len(data) if isinstance(data, list) else 1
                    self.log_test(f"{name} Endpoint", True, f"Retrieved {count} items")
                else:
                    self.log_test(f"{name} Endpoint", False, f"Status: {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"{name} Endpoint", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_cors_headers(self):
        """Test CORS headers for frontend-backend communication"""
        try:
            # Test preflight request
            headers = {
                "Origin": self.frontend_url,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type,Authorization"
            }
            response = requests.options(f"{self.backend_url}/login/", headers=headers)
            
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
            }
            
            if cors_headers["Access-Control-Allow-Origin"]:
                self.log_test("CORS Configuration", True, "CORS headers present")
                return True
            else:
                self.log_test("CORS Configuration", False, "Missing CORS headers")
                return False
        except Exception as e:
            self.log_test("CORS Configuration", False, f"Exception: {str(e)}")
            return False
    
    def test_static_files(self):
        """Test if static files are accessible"""
        static_files = [
            "/app/app.js",
            "/app/controllers/loginController.js",
            "/app/services/authUserService.js",
            "/style.css"
        ]
        
        all_passed = True
        for file_path in static_files:
            try:
                response = requests.get(f"{self.frontend_url}{file_path}")
                if response.status_code == 200:
                    self.log_test(f"Static File {file_path}", True, "File accessible")
                else:
                    self.log_test(f"Static File {file_path}", False, f"Status: {response.status_code}")
                    all_passed = False
            except Exception as e:
                self.log_test(f"Static File {file_path}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Frontend Integration Tests")
        print("=" * 60)
        
        print("\n🌐 Testing Frontend Accessibility:")
        self.test_frontend_accessibility()
        
        print("\n🔐 Testing Backend Login Flow:")
        self.test_backend_login_flow()
        
        print("\n📊 Testing Authenticated Endpoints:")
        self.test_authenticated_endpoints()
        
        print("\n🔗 Testing CORS Configuration:")
        self.test_cors_headers()
        
        print("\n📁 Testing Static Files:")
        self.test_static_files()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All integration tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

def main():
    """Main test runner"""
    tester = FrontendIntegrationTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())