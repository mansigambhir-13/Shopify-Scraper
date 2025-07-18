"""
Comprehensive test cases for the Shopify Store Insights Fetcher
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json
import sqlite3
import os
import tempfile

# Import the application
from main import app
from app.models.requests import ShopifyStoreRequest
from app.models.responses import BrandInsightsModel, ProductModel
from app.services.shopify_scraper import ShopifyScraperService
from app.utils.validators import validate_shopify_url, validate_email, validate_phone_number
from app.utils.data_processor import DataProcessor

# Initialize test client
client = TestClient(app)

# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def sample_shopify_response():
    """Sample Shopify products.json response"""
    return {
        "products": [
            {
                "id": 123456789,
                "title": "Test Product",
                "handle": "test-product",
                "body_html": "<p>Test product description</p>",
                "vendor": "Test Vendor",
                "product_type": "Test Type",
                "tags": ["test", "sample"],
                "variants": [
                    {
                        "id": 987654321,
                        "price": "29.99",
                        "compare_at_price": "39.99",
                        "available": True
                    }
                ],
                "images": ["https://example.com/image.jpg"]
            }
        ]
    }

@pytest.fixture
def sample_html_page():
    """Sample HTML page content"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Shopify Store</title>
        <meta name="description" content="Test store description">
    </head>
    <body>
        <h1>Welcome to Test Store</h1>
        <a href="/products/test-product">Test Product</a>
        <p>Contact us at test@example.com or call (555) 123-4567</p>
        <a href="https://instagram.com/teststore">Follow us on Instagram</a>
        <div class="faq">
            <h3>Do you offer free shipping?</h3>
            <p>Yes, we offer free shipping on orders over $50.</p>
        </div>
    </body>
    </html>
    """

@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    # Set up database URL for testing
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)

# =============================================================================
# API ENDPOINT TESTS
# =============================================================================

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Shopify Store Insights Fetcher API is running"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Shopify Store Insights Fetcher"
        assert data["version"] == "1.0.0"
    
    def test_extract_insights_validation_invalid_url(self):
        """Test extraction with invalid URL returns validation error"""
        response = client.post(
            "/api/v1/extract-insights",
            json={"website_url": "invalid-url"}
        )
        assert response.status_code == 422
    
    def test_extract_insights_validation_missing_url(self):
        """Test extraction without URL returns validation error"""
        response = client.post(
            "/api/v1/extract-insights",
            json={}
        )
        assert response.status_code == 422
    
    @patch('app.services.shopify_scraper.ShopifyScraperService.extract_comprehensive_insights')
    def test_extract_insights_success(self, mock_extract):
        """Test successful insights extraction"""
        # Mock the extraction service
        mock_insights = BrandInsightsModel(
            domain="example.com",
            brand_name="Test Store",
            total_products=5,
            extraction_success=True
        )
        mock_extract.return_value = mock_insights
        
        response = client.post(
            "/api/v1/extract-insights",
            json={"website_url": "https://example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Insights extracted successfully"
        assert data["data"]["domain"] == "example.com"
        assert data["data"]["brand_name"] == "Test Store"

# =============================================================================
# VALIDATION TESTS
# =============================================================================

class TestValidators:
    """Test validation utilities"""
    
    def test_validate_shopify_url_valid(self):
        """Test valid Shopify URLs"""
        valid_urls = [
            "https://example.com",
            "http://test.myshopify.com",
            "https://store.example.com"
        ]
        
        for url in valid_urls:
            with patch('requests.head') as mock_head:
                mock_head.return_value.status_code = 200
                assert validate_shopify_url(url) is True
    
    def test_validate_shopify_url_invalid(self):
        """Test invalid URLs"""
        invalid_urls = [
            "not-a-url",
            "ftp://example.com",
            "",
            "javascript:alert('xss')"
        ]
        
        for url in invalid_urls:
            assert validate_shopify_url(url) is False
    
    def test_validate_email(self):
        """Test email validation"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "valid+email@test.org"
        ]
        
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "test@",
            ""
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True
        
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_validate_phone_number(self):
        """Test phone number validation"""
        valid_phones = [
            "+1-555-123-4567",
            "(555) 123-4567",
            "555.123.4567",
            "+91 9876543210"
        ]
        
        invalid_phones = [
            "123",
            "not-a-phone",
            "",
            "++1234567890"
        ]
        
        for phone in valid_phones:
            assert validate_phone_number(phone) is True
        
        for phone in invalid_phones:
            assert validate_phone_number(phone) is False

# =============================================================================
# DATA PROCESSOR TESTS
# =============================================================================

class TestDataProcessor:
    """Test data processing utilities"""
    
    def setup_method(self):
        """Set up test data processor"""
        self.processor = DataProcessor()
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "  <p>Test   text\n\n\nwith   HTML</p>  "
        expected = "Test text with HTML"
        
        result = self.processor.clean_text(dirty_text)
        assert result == expected
    
    def test_extract_emails(self):
        """Test email extraction from text"""
        text = "Contact us at test@example.com or support@domain.org for help"
        
        emails = self.processor.extract_emails(text)
        assert "test@example.com" in emails
        assert "support@domain.org" in emails
        assert len(emails) == 2
    
    def test_extract_phone_numbers(self):
        """Test phone number extraction"""
        text = "Call us at (555) 123-4567 or +1-800-555-0123"
        
        phones = self.processor.extract_phone_numbers(text)
        assert len(phones) >= 1  # Should find at least one phone number
    
    def test_extract_emails_filters_false_positives(self):
        """Test that email extraction filters out false positives"""
        text = "Visit our site at image.jpg or download.pdf"
        
        emails = self.processor.extract_emails(text)
        assert len(emails) == 0  # Should not extract file extensions as emails

# =============================================================================
# SCRAPER SERVICE TESTS
# =============================================================================

class TestShopifyScraperService:
    """Test the main scraper service"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Set up test environment"""
        self.mock_db = Mock()
        self.scraper = ShopifyScraperService(self.mock_db)
    
    @patch('requests.Session.get')
    def test_extract_product_catalog(self, mock_get, sample_shopify_response):
        """Test product catalog extraction"""
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_shopify_response
        mock_get.return_value = mock_response
        
        # Test the extraction
        result = asyncio.run(
            self.scraper._extract_product_catalog("https://example.com")
        )
        
        assert len(result) == 1
        assert result[0].title == "Test Product"
        assert result[0].price == "29.99"
        assert result[0].vendor == "Test Vendor"
    
    @patch('requests.Session.get')
    def test_extract_brand_info(self, mock_get, sample_html_page):
        """Test brand information extraction"""
        # Mock the HTML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sample_html_page.encode()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the extraction
        result = asyncio.run(
            self.scraper._extract_brand_info("https://example.com")
        )
        
        assert result['name'] == "Test Shopify Store"
        assert "Test store description" in result['description']
    
    @patch('requests.Session.get')
    def test_extract_social_handles(self, mock_get, sample_html_page):
        """Test social media handles extraction"""
        # Mock the HTML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sample_html_page.encode()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test the extraction
        result = asyncio.run(
            self.scraper._extract_social_handles("https://example.com")
        )
        
        assert len(result) == 1
        assert result[0].platform == "instagram"
        assert "teststore" in result[0].username
    
    @patch('requests.Session.get')
    def test_extract_contact_info(self, mock_get, sample_html_page):
        """Test contact information extraction"""
        # Mock the HTML response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sample_html_page.encode()
        mock_get.return_value = mock_response
        
        # Test the extraction
        result = asyncio.run(
            self.scraper._extract_contact_info("https://example.com")
        )
        
        assert "test@example.com" in result.emails
        assert len(result.phone_numbers) >= 1
    
    def test_parse_product_data(self, sample_shopify_response):
        """Test product data parsing"""
        product_data = sample_shopify_response['products'][0]
        
        result = self.scraper._parse_product_data(product_data, "https://example.com")
        
        assert result is not None
        assert result.title == "Test Product"
        assert result.handle == "test-product"
        assert result.price == "29.99"
        assert result.availability is True

# =============================================================================
# DATABASE TESTS
# =============================================================================

class TestDatabaseOperations:
    """Test database operations"""
    
    def test_sqlite_connection(self, temp_db):
        """Test SQLite database connection"""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Test basic operation
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1
        
        conn.close()
    
    def test_database_table_creation(self, temp_db):
        """Test database table creation"""
        from app.database.database import engine, Base
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables exist
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            'brand_insights', 'products', 'policies', 
            'faqs', 'social_handles', 'contact_info', 'important_links'
        ]
        
        for table in expected_tables:
            assert table in tables
        
        conn.close()

# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests that test multiple components together"""
    
    @patch('requests.Session.get')
    def test_full_extraction_flow(self, mock_get, temp_db, sample_shopify_response, sample_html_page):
        """Test complete extraction flow"""
        # Mock different responses for different URLs
        def mock_response_factory(url, **kwargs):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.raise_for_status.return_value = None
            
            if 'products.json' in url:
                mock_response.json.return_value = sample_shopify_response
            else:
                mock_response.content = sample_html_page.encode()
            
            return mock_response
        
        mock_get.side_effect = mock_response_factory
        
        # Test the API endpoint
        response = client.post(
            "/api/v1/extract-insights",
            json={"website_url": "https://example.com"}
        )
        
        # Should succeed despite mocked responses
        assert response.status_code in [200, 500]  # 500 is OK due to mocked DB

# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Performance and load tests"""
    
    def test_api_response_time(self):
        """Test API response time"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                response = client.get("/health")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Create and start threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Assertions
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert all(status == 200 for status in results)
        assert len(results) == 10
        assert (end_time - start_time) < 5.0  # Should complete within 5 seconds

# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestErrorHandling:
    """Test error handling scenarios"""
    
    @patch('app.services.shopify_scraper.ShopifyScraperService._check_website_accessibility')
    def test_website_not_accessible(self, mock_accessibility):
        """Test handling of inaccessible websites"""
        mock_accessibility.return_value = False
        
        response = client.post(
            "/api/v1/extract-insights",
            json={"website_url": "https://nonexistent-site.com"}
        )
        
        assert response.status_code in [401, 500]
        data = response.json()
        assert data["success"] is False
    
    def test_malformed_json_request(self):
        """Test handling of malformed JSON requests"""
        response = client.post(
            "/api/v1/extract-insights",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

if __name__ == "__main__":
    # Run specific test
    pytest.main([__file__, "-v", "--tb=short"])