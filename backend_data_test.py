#!/usr/bin/env python3
"""
Test data endpoints to verify sample data is available
"""

import requests
import sys
import json

class DataTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.access_token = None
        
    def login(self):
        """Login and get access token"""
        url = f"{self.api_base}/login/"
        data = {"username": "admin", "password": "admin123"}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                response_data = response.json()
                self.access_token = response_data['access']
                print("✅ Login successful")
                return True
            else:
                print(f"❌ Login failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            return False
    
    def test_endpoint(self, endpoint_name, endpoint_url):
        """Test a data endpoint"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(f"{self.api_base}{endpoint_url}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else len(data.get('results', []))
                print(f"✅ {endpoint_name}: {count} items found")
                if count > 0:
                    print(f"   Sample: {json.dumps(data[0] if isinstance(data, list) else data['results'][0], indent=2)[:200]}...")
                return True
            else:
                print(f"❌ {endpoint_name}: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {endpoint_name}: Error {str(e)}")
            return False
    
    def run_tests(self):
        """Run all data tests"""
        print("🔍 Testing Data Endpoints")
        print("=" * 50)
        
        if not self.login():
            return 1
            
        endpoints = [
            ("Tower Instances", "/instances/"),
            ("Credentials", "/credentials/"),
            ("Execution Environments", "/environments/"),
            ("Audit Logs", "/audit-logs/"),
            ("Users", "/users/"),
        ]
        
        for name, url in endpoints:
            self.test_endpoint(name, url)
        
        return 0

if __name__ == "__main__":
    tester = DataTester()
    sys.exit(tester.run_tests())