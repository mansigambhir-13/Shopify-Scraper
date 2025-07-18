"""
Response models for the Shopify Store Insights API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProductModel(BaseModel):
    """Model for individual product information"""
    
    id: Optional[str] = None
    title: str
    handle: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    compare_at_price: Optional[str] = None
    availability: Optional[bool] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    vendor: Optional[str] = None
    product_type: Optional[str] = None
    tags: List[str] = []

class SocialHandleModel(BaseModel):
    """Model for social media handles"""
    
    platform: str
    url: str
    username: Optional[str] = None

class ContactInfoModel(BaseModel):
    """Model for contact information"""
    
    emails: List[str] = []
    phone_numbers: List[str] = []
    addresses: List[str] = []

class PolicyModel(BaseModel):
    """Model for store policies"""
    
    title: str
    content: str
    url: Optional[str] = None

class FAQModel(BaseModel):
    """Model for FAQ items"""
    
    question: str
    answer: str
    category: Optional[str] = None

class ImportantLinkModel(BaseModel):
    """Model for important links"""
    
    title: str
    url: str
    category: Optional[str] = None

class BrandInsightsModel(BaseModel):
    """Comprehensive brand insights model"""
    
    # Basic brand information
    brand_name: Optional[str] = None
    domain: str
    brand_description: Optional[str] = None
    
    # Product information
    product_catalog: List[ProductModel] = []
    hero_products: List[ProductModel] = []
    total_products: int = 0
    
    # Policies and information
    privacy_policy: Optional[PolicyModel] = None
    return_refund_policy: Optional[PolicyModel] = None
    terms_of_service: Optional[PolicyModel] = None
    
    # FAQ and support
    faqs: List[FAQModel] = []
    
    # Social and contact
    social_handles: List[SocialHandleModel] = []
    contact_info: ContactInfoModel = ContactInfoModel()
    
    # Important links
    important_links: List[ImportantLinkModel] = []
    
    # Additional insights
    brand_story: Optional[str] = None
    shipping_info: Optional[str] = None
    payment_methods: List[str] = []
    
    # Metadata
    extraction_timestamp: datetime = Field(default_factory=datetime.now)
    extraction_success: bool = True
    errors_encountered: List[str] = []

class BrandInsightsResponse(BaseModel):
    """API response model for brand insights"""
    
    success: bool
    message: str
    data: Optional[BrandInsightsModel] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    
    success: bool = False
    error: str
    status_code: int
    details: Optional[Dict[str, Any]] = None