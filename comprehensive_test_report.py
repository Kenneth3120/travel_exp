#!/usr/bin/env python3
"""
Comprehensive Test Report for AAP Administration Application
"""

import requests
import sys
import json
from datetime import datetime

class ComprehensiveTestReport:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000/api"
        self.frontend_url = "http://127.0.0.1:4208"
        self.access_token = None
        self.results = {
            "backend_tests": [],
            "frontend_tests": [],
            "integration_tests": [],
            "data_validation": []
        }
    
    def login_and_get_token(self):
        """Login and get access token for authenticated tests"""
        try:
            response = requests.post(f"{self.backend_url}/login/", 
                                   json={"username": "admin", "password": "admin123"})
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                return True
            return False
        except:
            return False
    
    def test_authentication_flow(self):
        """Test complete authentication flow"""
        print("🔐 Testing Authentication Flow...")
        
        # Test 1: Valid login
        try:
            response = requests.post(f"{self.backend_url}/login/", 
                                   json={"username": "admin", "password": "admin123"})
            if response.status_code == 200:
                data = response.json()
                self.results["backend_tests"].append({
                    "test": "Valid Login",
                    "status": "PASS",
                    "details": f"User: {data['user']['username']}, Role: {data['user']['role']}"
                })
                self.access_token = data.get('access')
            else:
                self.results["backend_tests"].append({
                    "test": "Valid Login",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["backend_tests"].append({
                "test": "Valid Login",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
        
        # Test 2: Invalid login
        try:
            response = requests.post(f"{self.backend_url}/login/", 
                                   json={"username": "admin", "password": "wrong"})
            if response.status_code == 401:
                self.results["backend_tests"].append({
                    "test": "Invalid Login Rejection",
                    "status": "PASS",
                    "details": "Correctly rejected invalid credentials"
                })
            else:
                self.results["backend_tests"].append({
                    "test": "Invalid Login Rejection",
                    "status": "FAIL",
                    "details": f"Expected 401, got {response.status_code}"
                })
        except Exception as e:
            self.results["backend_tests"].append({
                "test": "Invalid Login Rejection",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
    
    def test_dashboard_data(self):
        """Test dashboard data endpoints"""
        print("📊 Testing Dashboard Data...")
        
        if not self.access_token:
            self.results["data_validation"].append({
                "test": "Dashboard Data",
                "status": "SKIP",
                "details": "No access token available"
            })
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test instances count (should be 4)
        try:
            response = requests.get(f"{self.backend_url}/instances/", headers=headers)
            if response.status_code == 200:
                instances = response.json()
                count = len(instances)
                expected = 4
                if count == expected:
                    self.results["data_validation"].append({
                        "test": "Tower Instances Count",
                        "status": "PASS",
                        "details": f"Found {count} instances as expected"
                    })
                else:
                    self.results["data_validation"].append({
                        "test": "Tower Instances Count",
                        "status": "FAIL",
                        "details": f"Expected {expected}, found {count}"
                    })
            else:
                self.results["data_validation"].append({
                    "test": "Tower Instances Count",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["data_validation"].append({
                "test": "Tower Instances Count",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
        
        # Test credentials count (should be 10)
        try:
            response = requests.get(f"{self.backend_url}/credentials/", headers=headers)
            if response.status_code == 200:
                credentials = response.json()
                count = len(credentials)
                expected = 10
                if count == expected:
                    self.results["data_validation"].append({
                        "test": "Credentials Count",
                        "status": "PASS",
                        "details": f"Found {count} credentials as expected"
                    })
                else:
                    self.results["data_validation"].append({
                        "test": "Credentials Count",
                        "status": "FAIL",
                        "details": f"Expected {expected}, found {count}"
                    })
            else:
                self.results["data_validation"].append({
                    "test": "Credentials Count",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["data_validation"].append({
                "test": "Credentials Count",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
        
        # Test environments count (should be 12)
        try:
            response = requests.get(f"{self.backend_url}/environments/", headers=headers)
            if response.status_code == 200:
                environments = response.json()
                count = len(environments)
                expected = 12
                if count == expected:
                    self.results["data_validation"].append({
                        "test": "Execution Environments Count",
                        "status": "PASS",
                        "details": f"Found {count} environments as expected"
                    })
                else:
                    self.results["data_validation"].append({
                        "test": "Execution Environments Count",
                        "status": "FAIL",
                        "details": f"Expected {expected}, found {count}"
                    })
            else:
                self.results["data_validation"].append({
                    "test": "Execution Environments Count",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["data_validation"].append({
                "test": "Execution Environments Count",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
        
        # Test audit logs count (should be 5)
        try:
            response = requests.get(f"{self.backend_url}/audit-logs/", headers=headers)
            if response.status_code == 200:
                logs = response.json()
                count = len(logs)
                expected = 5
                if count == expected:
                    self.results["data_validation"].append({
                        "test": "Audit Logs Count",
                        "status": "PASS",
                        "details": f"Found {count} audit logs as expected"
                    })
                else:
                    self.results["data_validation"].append({
                        "test": "Audit Logs Count",
                        "status": "FAIL",
                        "details": f"Expected {expected}, found {count}"
                    })
            else:
                self.results["data_validation"].append({
                    "test": "Audit Logs Count",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["data_validation"].append({
                "test": "Audit Logs Count",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
    
    def test_frontend_accessibility(self):
        """Test frontend accessibility and structure"""
        print("🌐 Testing Frontend Accessibility...")
        
        # Test 1: Frontend serves HTML
        try:
            response = requests.get(self.frontend_url)
            if response.status_code == 200:
                content = response.text
                if "AAP Administration" in content and "ng-app" in content:
                    self.results["frontend_tests"].append({
                        "test": "Frontend HTML Serving",
                        "status": "PASS",
                        "details": "Frontend serves AngularJS application"
                    })
                else:
                    self.results["frontend_tests"].append({
                        "test": "Frontend HTML Serving",
                        "status": "FAIL",
                        "details": "Frontend not serving expected AngularJS content"
                    })
            else:
                self.results["frontend_tests"].append({
                    "test": "Frontend HTML Serving",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["frontend_tests"].append({
                "test": "Frontend HTML Serving",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
        
        # Test 2: Static files accessibility
        static_files = [
            "/app/app.js",
            "/app/controllers/loginController.js",
            "/app/services/authUserService.js",
            "/style.css"
        ]
        
        for file_path in static_files:
            try:
                response = requests.get(f"{self.frontend_url}{file_path}")
                if response.status_code == 200:
                    self.results["frontend_tests"].append({
                        "test": f"Static File: {file_path}",
                        "status": "PASS",
                        "details": "File accessible"
                    })
                else:
                    self.results["frontend_tests"].append({
                        "test": f"Static File: {file_path}",
                        "status": "FAIL",
                        "details": f"Status: {response.status_code}"
                    })
            except Exception as e:
                self.results["frontend_tests"].append({
                    "test": f"Static File: {file_path}",
                    "status": "FAIL",
                    "details": f"Exception: {str(e)}"
                })
    
    def test_cors_configuration(self):
        """Test CORS configuration"""
        print("🔗 Testing CORS Configuration...")
        
        try:
            headers = {
                "Origin": self.frontend_url,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type,Authorization"
            }
            response = requests.options(f"{self.backend_url}/login/", headers=headers)
            
            if "Access-Control-Allow-Origin" in response.headers:
                self.results["integration_tests"].append({
                    "test": "CORS Configuration",
                    "status": "PASS",
                    "details": "CORS headers present for frontend-backend communication"
                })
            else:
                self.results["integration_tests"].append({
                    "test": "CORS Configuration",
                    "status": "FAIL",
                    "details": "Missing CORS headers"
                })
        except Exception as e:
            self.results["integration_tests"].append({
                "test": "CORS Configuration",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
    
    def test_instance_management(self):
        """Test instance management functionality"""
        print("🏗️ Testing Instance Management...")
        
        if not self.access_token:
            return
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        # Test filtering by region and environment
        try:
            response = requests.get(f"{self.backend_url}/instances/", headers=headers)
            if response.status_code == 200:
                instances = response.json()
                regions = set(instance.get('region', '') for instance in instances)
                environments = set(instance.get('environment', '') for instance in instances)
                
                self.results["data_validation"].append({
                    "test": "Instance Filtering Data",
                    "status": "PASS",
                    "details": f"Regions: {list(regions)}, Environments: {list(environments)}"
                })
            else:
                self.results["data_validation"].append({
                    "test": "Instance Filtering Data",
                    "status": "FAIL",
                    "details": f"Status: {response.status_code}"
                })
        except Exception as e:
            self.results["data_validation"].append({
                "test": "Instance Filtering Data",
                "status": "FAIL",
                "details": f"Exception: {str(e)}"
            })
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📋 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Backend URL: {self.backend_url}")
        print(f"Frontend URL: {self.frontend_url}")
        
        # Backend Tests
        print(f"\n🔧 BACKEND TESTS ({len(self.results['backend_tests'])} tests)")
        print("-" * 40)
        for test in self.results['backend_tests']:
            status_icon = "✅" if test['status'] == "PASS" else "❌"
            print(f"{status_icon} {test['test']}: {test['status']}")
            if test['details']:
                print(f"   {test['details']}")
        
        # Frontend Tests
        print(f"\n🌐 FRONTEND TESTS ({len(self.results['frontend_tests'])} tests)")
        print("-" * 40)
        for test in self.results['frontend_tests']:
            status_icon = "✅" if test['status'] == "PASS" else "❌"
            print(f"{status_icon} {test['test']}: {test['status']}")
            if test['details']:
                print(f"   {test['details']}")
        
        # Integration Tests
        print(f"\n🔗 INTEGRATION TESTS ({len(self.results['integration_tests'])} tests)")
        print("-" * 40)
        for test in self.results['integration_tests']:
            status_icon = "✅" if test['status'] == "PASS" else "❌"
            print(f"{status_icon} {test['test']}: {test['status']}")
            if test['details']:
                print(f"   {test['details']}")
        
        # Data Validation
        print(f"\n📊 DATA VALIDATION ({len(self.results['data_validation'])} tests)")
        print("-" * 40)
        for test in self.results['data_validation']:
            status_icon = "✅" if test['status'] == "PASS" else "❌" if test['status'] == "FAIL" else "⏭️"
            print(f"{status_icon} {test['test']}: {test['status']}")
            if test['details']:
                print(f"   {test['details']}")
        
        # Summary
        all_tests = (self.results['backend_tests'] + 
                    self.results['frontend_tests'] + 
                    self.results['integration_tests'] + 
                    self.results['data_validation'])
        
        passed = sum(1 for test in all_tests if test['status'] == "PASS")
        failed = sum(1 for test in all_tests if test['status'] == "FAIL")
        skipped = sum(1 for test in all_tests if test['status'] == "SKIP")
        total = len(all_tests)
        
        print(f"\n📈 SUMMARY")
        print("-" * 40)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Skipped: {skipped} ⏭️")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        return failed == 0
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Comprehensive AAP Administration Tests")
        
        # Login first
        if not self.login_and_get_token():
            print("❌ Failed to login - some tests will be skipped")
        
        # Run all test categories
        self.test_authentication_flow()
        self.test_dashboard_data()
        self.test_frontend_accessibility()
        self.test_cors_configuration()
        self.test_instance_management()
        
        # Generate report
        success = self.generate_report()
        
        return 0 if success else 1

def main():
    """Main test runner"""
    tester = ComprehensiveTestReport()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())