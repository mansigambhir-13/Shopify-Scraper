"""
Basic test cases for the application
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test that the root endpoint is working"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Shopify Store Insights Fetcher API is running"

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Shopify Store Insights Fetcher"
    assert data["version"] == "1.0.0"

def test_extract_insights_validation():
    """Test that URL validation works"""
    # Test with invalid URL
    response = client.post(
        "/api/v1/extract-insights",
        json={"website_url": "invalid-url"}
    )
    assert response.status_code == 422  # Validation error

def test_extract_insights_missing_url():
    """Test extraction without URL"""
    response = client.post(
        "/api/v1/extract-insights",
        json={}
    )
    assert response.status_code == 422  # Missing required field

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])