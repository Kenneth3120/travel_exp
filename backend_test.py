#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for AAP Administration Application
Tests JWT-based authentication system and protected endpoints
"""

import requests
import sys
import json
from datetime import datetime

class AAPBackendTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.access_token = None
        self.refresh_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.user_info = None

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

    def test_login_valid_credentials(self):
        """Test login with valid admin credentials"""
        url = f"{self.api_base}/login/"
        data = {"username": "admin", "password": "admin123"}
        
        try:
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                response_data = response.json()
                if 'access' in response_data and 'refresh' in response_data and 'user' in response_data:
                    self.access_token = response_data['access']
                    self.refresh_token = response_data['refresh']
                    self.user_info = response_data['user']
                    self.log_test("Login with valid credentials", True, 
                                f"User: {self.user_info['username']}, Role: {self.user_info['role']}")
                    return True
                else:
                    self.log_test("Login with valid credentials", False, 
                                "Missing required fields in response")
                    return False
            else:
                self.log_test("Login with valid credentials", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Login with valid credentials", False, f"Exception: {str(e)}")
            return False

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = f"{self.api_base}/login/"
        data = {"username": "admin", "password": "wrongpassword"}
        
        try:
            response = requests.post(url, json=data)
            
            if response.status_code == 401:
                response_data = response.json()
                if 'error' in response_data:
                    self.log_test("Login with invalid credentials", True, 
                                f"Correctly rejected with: {response_data['error']}")
                    return True
                else:
                    self.log_test("Login with invalid credentials", False, 
                                "Missing error message in response")
                    return False
            else:
                self.log_test("Login with invalid credentials", False, 
                            f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Login with invalid credentials", False, f"Exception: {str(e)}")
            return False

    def test_login_missing_fields(self):
        """Test login with missing username/password"""
        url = f"{self.api_base}/login/"
        
        # Test missing username
        try:
            response = requests.post(url, json={"password": "admin123"})
            if response.status_code == 400:
                self.log_test("Login with missing username", True, "Correctly rejected missing username")
            else:
                self.log_test("Login with missing username", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Login with missing username", False, f"Exception: {str(e)}")
        
        # Test missing password
        try:
            response = requests.post(url, json={"username": "admin"})
            if response.status_code == 400:
                self.log_test("Login with missing password", True, "Correctly rejected missing password")
            else:
                self.log_test("Login with missing password", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_test("Login with missing password", False, f"Exception: {str(e)}")

    def test_user_info_with_token(self):
        """Test user-info endpoint with valid token"""
        if not self.access_token:
            self.log_test("User info with valid token", False, "No access token available")
            return False
            
        url = f"{self.api_base}/user-info/"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                required_fields = ['id', 'username', 'email', 'role']
                if all(field in response_data for field in required_fields):
                    self.log_test("User info with valid token", True, 
                                f"Retrieved user info for {response_data['username']}")
                    return True
                else:
                    self.log_test("User info with valid token", False, 
                                "Missing required fields in user info")
                    return False
            else:
                self.log_test("User info with valid token", False, 
                            f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User info with valid token", False, f"Exception: {str(e)}")
            return False

    def test_user_info_without_token(self):
        """Test user-info endpoint without token"""
        url = f"{self.api_base}/user-info/"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 401:
                self.log_test("User info without token", True, "Correctly rejected unauthorized request")
                return True
            else:
                self.log_test("User info without token", False, 
                            f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User info without token", False, f"Exception: {str(e)}")
            return False

    def test_user_info_invalid_token(self):
        """Test user-info endpoint with invalid token"""
        url = f"{self.api_base}/user-info/"
        headers = {"Authorization": "Bearer invalid_token_here"}
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 401:
                self.log_test("User info with invalid token", True, "Correctly rejected invalid token")
                return True
            else:
                self.log_test("User info with invalid token", False, 
                            f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("User info with invalid token", False, f"Exception: {str(e)}")
            return False

    def test_logout_with_token(self):
        """Test logout endpoint with valid refresh token"""
        if not self.refresh_token:
            self.log_test("Logout with valid token", False, "No refresh token available")
            return False
            
        url = f"{self.api_base}/logout/"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"refresh": self.refresh_token}
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                if 'message' in response_data:
                    self.log_test("Logout with valid token", True, 
                                f"Successfully logged out: {response_data['message']}")
                    return True
                else:
                    self.log_test("Logout with valid token", False, 
                                "Missing success message")
                    return False
            else:
                self.log_test("Logout with valid token", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Logout with valid token", False, f"Exception: {str(e)}")
            return False

    def test_logout_without_token(self):
        """Test logout endpoint without authentication"""
        url = f"{self.api_base}/logout/"
        data = {"refresh": "some_token"}
        
        try:
            response = requests.post(url, json=data)
            
            if response.status_code == 401:
                self.log_test("Logout without token", True, "Correctly rejected unauthorized logout")
                return True
            else:
                self.log_test("Logout without token", False, 
                            f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Logout without token", False, f"Exception: {str(e)}")
            return False

    def test_protected_endpoints(self):
        """Test that protected endpoints require authentication"""
        protected_endpoints = [
            "/api/instances/",
            "/api/credentials/",
            "/api/environments/",
            "/api/audit-logs/",
            "/api/users/"
        ]
        
        for endpoint in protected_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                if response.status_code == 401:
                    self.log_test(f"Protected endpoint {endpoint}", True, "Correctly requires authentication")
                else:
                    self.log_test(f"Protected endpoint {endpoint}", False, 
                                f"Expected 401, got {response.status_code}")
            except Exception as e:
                self.log_test(f"Protected endpoint {endpoint}", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting AAP Administration Backend API Tests")
        print("=" * 60)
        
        # Test login functionality
        print("\n📝 Testing Authentication Endpoints:")
        self.test_login_valid_credentials()
        self.test_login_invalid_credentials()
        self.test_login_missing_fields()
        
        # Test user info endpoint
        print("\n👤 Testing User Info Endpoint:")
        self.test_user_info_with_token()
        self.test_user_info_without_token()
        self.test_user_info_invalid_token()
        
        # Test logout functionality
        print("\n🚪 Testing Logout Endpoint:")
        self.test_logout_with_token()
        self.test_logout_without_token()
        
        # Test protected endpoints
        print("\n🔒 Testing Protected Endpoints:")
        self.test_protected_endpoints()
        
        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All backend tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

def main():
    """Main test runner"""
    tester = AAPBackendTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())