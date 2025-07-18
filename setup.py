#!/usr/bin/env python3
"""
Automated Testing Script for Shopify Insights Fetcher
Run this to test all core functionality automatically
"""

import requests
import json
import time
from datetime import datetime
import sqlite3
import os

class ShopifyInsightsTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log(self, message, level="INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_health_check(self):
        """Test 1: Health Check"""
        self.log("🔍 Testing health check endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log("✅ Health check PASSED", "SUCCESS")
                    return True
                else:
                    self.log("❌ Health check failed - invalid response", "ERROR")
                    return False
            else:
                self.log(f"❌ Health check failed - status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Health check failed - {e}", "ERROR")
            return False
    
    def test_api_docs(self):
        """Test 2: API Documentation"""
        self.log("📖 Testing API documentation endpoint...")
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=10)
            if response.status_code == 200:
                self.log("✅ API docs accessible", "SUCCESS")
                return True
            else:
                self.log(f"❌ API docs failed - status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ API docs failed - {e}", "ERROR")
            return False
    
    def test_shopify_extraction(self, store_url, store_name):
        """Test Shopify store extraction."""
        self.log(f"🏪 Testing {store_name} extraction...")
        
        try:
            payload = {"website_url": store_url}
            
            # Make API request
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/v1/extract-insights",
                json=payload,
                timeout=120  # 2 minutes timeout
            )
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            if response.status_code != 200:
                self.log(f"❌ {store_name} failed - HTTP {response.status_code}", "ERROR")
                self.log(f"   Response: {response.text[:200]}", "ERROR")
                return self.create_test_result(store_name, False, 0, 0, response_time, f"HTTP {response.status_code}")
            
            # Parse response
            data = response.json()
            
            # Validate response structure
            if not data.get('success', False):
                self.log(f"❌ {store_name} failed - success=false", "ERROR")
                return self.create_test_result(store_name, False, 0, 0, response_time, "success=false")
            
            # Extract key metrics
            insights = data.get('data', {})
            brand_name = insights.get('brand_name', 'Unknown')
            total_products = insights.get('total_products', 0)
            product_catalog = insights.get('product_catalog', [])
            social_handles = insights.get('social_handles', [])
            extraction_success = insights.get('extraction_success', False)
            
            # Validate data quality
            issues = []
            if total_products == 0:
                issues.append("No products found")
            if len(product_catalog) == 0:
                issues.append("Empty product catalog")
            if not extraction_success:
                issues.append("Extraction marked as failed")
            
            # Log results
            if issues:
                self.log(f"⚠️  {store_name} partial success - {', '.join(issues)}", "WARNING")
            else:
                self.log(f"✅ {store_name} extraction PASSED", "SUCCESS")
            
            self.log(f"   Brand: {brand_name}")
            self.log(f"   Products: {total_products}")
            self.log(f"   Social Handles: {len(social_handles)}")
            self.log(f"   Response Time: {response_time}s")
            
            # Display sample products
            if product_catalog:
                self.log(f"   Sample Products:")
                for i, product in enumerate(product_catalog[:3]):
                    title = product.get('title', 'Unknown')
                    price = ""
                    if 'variants' in product and product['variants']:
                        price = product['variants'][0].get('price', 'N/A')
                    self.log(f"     {i+1}. {title} ${price}")
            
            # Display social handles
            if social_handles:
                self.log(f"   Social Media:")
                for handle in social_handles[:3]:
                    platform = handle.get('platform', 'unknown')
                    username = handle.get('username', 'N/A')
                    self.log(f"     {platform}: @{username}")
            
            success = len(issues) == 0
            return self.create_test_result(
                store_name, success, total_products, 
                len(social_handles), response_time, 
                ', '.join(issues) if issues else "Success"
            )
            
        except requests.exceptions.Timeout:
            self.log(f"❌ {store_name} failed - Timeout after 2 minutes", "ERROR")
            return self.create_test_result(store_name, False, 0, 0, 120, "Timeout")
        except Exception as e:
            self.log(f"❌ {store_name} failed - {e}", "ERROR")
            return self.create_test_result(store_name, False, 0, 0, 0, str(e))
    
    def create_test_result(self, store_name, success, products, social_handles, response_time, notes):
        """Create a test result object."""
        return {
            'store': store_name,
            'success': success,
            'products': products,
            'social_handles': social_handles,
            'response_time': response_time,
            'notes': notes
        }
    
    def test_database_storage(self):
        """Test database storage."""
        self.log("🗄️  Testing database storage...")
        
        try:
            db_path = "shopify_insights.db"
            if not os.path.exists(db_path):
                self.log("❌ Database file not found", "ERROR")
                return False
            
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if brand_insights table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='brand_insights'")
            if not cursor.fetchone():
                self.log("❌ brand_insights table not found", "ERROR")
                conn.close()
                return False
            
            # Count records
            cursor.execute("SELECT COUNT(*) FROM brand_insights")
            count = cursor.fetchone()[0]
            
            # Get sample record
            cursor.execute("SELECT brand_name, domain, total_products FROM brand_insights LIMIT 1")
            sample = cursor.fetchone()
            
            conn.close()
            
            if count > 0:
                self.log(f"✅ Database storage PASSED", "SUCCESS")
                self.log(f"   Records found: {count}")
                if sample:
                    self.log(f"   Sample: {sample[0]} ({sample[1]}) - {sample[2]} products")
                return True
            else:
                self.log("⚠️  Database table exists but no records found", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"❌ Database test failed - {e}", "ERROR")
            return False
    
    def test_error_handling(self):
        """Test error handling."""
        self.log("🚨 Testing error handling...")
        
        test_cases = [
            {"url": "invalid-url", "name": "Invalid URL"},
            {"url": "https://google.com", "name": "Non-Shopify Site"},
            {"url": "https://this-site-does-not-exist-12345.com", "name": "Non-existent Site"}
        ]
        
        passed = 0
        for test_case in test_cases:
            try:
                response = requests.post(
                    f"{self.base_url}/api/v1/extract-insights",
                    json={"website_url": test_case["url"]},
                    timeout=30
                )
                
                # Should either return an error status or handle gracefully
                if response.status_code in [400, 422, 500]:
                    self.log(f"✅ {test_case['name']} handled correctly (HTTP {response.status_code})")
                    passed += 1
                elif response.status_code == 200:
                    data = response.json()
                    if not data.get('success', True):
                        self.log(f"✅ {test_case['name']} handled gracefully (success=false)")
                        passed += 1
                    else:
                        self.log(f"⚠️  {test_case['name']} unexpected success")
                else:
                    self.log(f"⚠️  {test_case['name']} unexpected status: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                self.log(f"⚠️  {test_case['name']} timeout (acceptable)")
                passed += 1
            except Exception as e:
                self.log(f"❌ {test_case['name']} failed: {e}")
        
        success_rate = passed / len(test_cases)
        if success_rate >= 0.5:
            self.log(f"✅ Error handling PASSED ({passed}/{len(test_cases)})", "SUCCESS")
            return True
        else:
            self.log(f"❌ Error handling FAILED ({passed}/{len(test_cases)})", "ERROR")
            return False
    
    def run_full_test_suite(self):
        """Run the complete test suite."""
        self.log("🚀 Starting Shopify Insights Fetcher Test Suite")
        self.log("=" * 60)
        
        # Test stores
        test_stores = [
            ("https://allbirds.com", "Allbirds"),
            ("https://gymshark.com", "Gymshark"),
            ("https://bombas.com", "Bombas")
        ]
        
        # Run tests
        tests = []
        
        # Infrastructure tests
        tests.append(("Health Check", self.test_health_check()))
        tests.append(("API Documentation", self.test_api_docs()))
        
        # Core functionality tests
        for store_url, store_name in test_stores:
            result = self.test_shopify_extraction(store_url, store_name)
            tests.append((f"{store_name} Extraction", result.get('success', False) if isinstance(result, dict) else result))
            if isinstance(result, dict):
                self.results.append(result)
        
        # Storage and error handling
        tests.append(("Database Storage", self.test_database_storage()))
        tests.append(("Error Handling", self.test_error_handling()))
        
        # Calculate results
        self.total_tests = len(tests)
        self.passed_tests = sum(1 for _, passed in tests if passed)
        
        # Print summary
        self.print_summary(tests)
        
        return self.passed_tests / self.total_tests >= 0.8  # 80% pass rate required
    
    def print_summary(self, tests):
        """Print test summary."""
        self.log("=" * 60)
        self.log("📊 TEST SUMMARY")
        self.log("=" * 60)
        
        for test_name, passed in tests:
            status = "✅ PASS" if passed else "❌ FAIL"
            self.log(f"{status} {test_name}")
        
        pass_rate = (self.passed_tests / self.total_tests) * 100
        self.log("")
        self.log(f"Total Tests: {self.total_tests}")
        self.log(f"Passed: {self.passed_tests}")
        self.log(f"Failed: {self.total_tests - self.passed_tests}")
        self.log(f"Pass Rate: {pass_rate:.1f}%")
        
        # Shopify extraction results
        if self.results:
            self.log("")
            self.log("🏪 SHOPIFY EXTRACTION RESULTS:")
            for result in self.results:
                status = "✅" if result['success'] else "❌"
                self.log(f"{status} {result['store']}: {result['products']} products, "
                        f"{result['social_handles']} social handles, {result['response_time']}s")
        
        self.log("")
        if pass_rate >= 80:
            self.log("🎉 SUBMISSION READY! Your project passed the tests.", "SUCCESS")
        elif pass_rate >= 60:
            self.log("⚠️  MOSTLY READY - Fix failing tests before submission.", "WARNING")
        else:
            self.log("❌ NOT READY - Critical issues need to be resolved.", "ERROR")
        
        self.log("")
        self.log("📖 API Documentation: http://localhost:8000/docs")
        self.log("🗄️  Database Browser: http://localhost:8080 (if running)")

def main():
    """Main testing function."""
    print("🧪 Shopify Insights Fetcher - Automated Testing")
    print("Make sure your application is running on http://localhost:8000")
    print("")
    
    # Wait for user confirmation
    input("Press Enter when your application is running...")
    
    # Run tests
    tester = ShopifyInsightsTester()
    ready_for_submission = tester.run_full_test_suite()
    
    # Final recommendation
    print("")
    if ready_for_submission:
        print("🎯 RECOMMENDATION: Your project is ready for submission!")
    else:
        print("🔧 RECOMMENDATION: Fix the failing tests before submitting.")
    
    return ready_for_submission

if __name__ == "__main__":
    main()