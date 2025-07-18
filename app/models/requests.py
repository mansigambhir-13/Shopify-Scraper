"""
Request models for the Shopify Store Insights API
"""

from pydantic import BaseModel, validator, Field
from typing import Optional
import validators

class ShopifyStoreRequest(BaseModel):
    """Request model for extracting Shopify store insights"""
    
    website_url: str = Field(
        ...,
        description="The Shopify store URL to extract insights from",
        example="https://memy.co.in"
    )
    
    @validator('website_url')
    def validate_url(cls, v):
        """Validate that the URL is properly formatted"""
        if not validators.url(v):
            raise ValueError('Invalid URL format')
        
        # Ensure URL has proper scheme
        if not v.startswith(('http://', 'https://')):
            v = f"https://{v}"
        
        return v.lower().strip()

class CompetitorAnalysisRequest(BaseModel):
    """Request model for competitor analysis"""
    
    website_url: str = Field(
        ...,
        description="The main brand's Shopify store URL",
        example="https://memy.co.in"
    )
    
    industry_context: Optional[str] = Field(
        None,
        description="Additional context about the industry/niche",
        example="sustainable fashion, eco-friendly clothing"
    )
    
    max_competitors: Optional[int] = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of competitors to analyze"
    )
    
    @validator('website_url')
    def validate_url(cls, v):
        """Validate that the URL is properly formatted"""
        if not validators.url(v):
            raise ValueError('Invalid URL format')
        
        if not v.startswith(('http://', 'https://')):
            v = f"https://{v}"
        
        return v.lower().strip()