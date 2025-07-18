"""
SQLAlchemy database models for storing insights
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class BrandInsights(Base):
    """Main table for storing brand insights"""
    
    __tablename__ = "brand_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, index=True)
    brand_name = Column(String(255), nullable=True)
    brand_description = Column(Text, nullable=True)
    brand_story = Column(Text, nullable=True)
    
    total_products = Column(Integer, default=0)
    shipping_info = Column(Text, nullable=True)
    payment_methods = Column(JSON, nullable=True)
    
    extraction_timestamp = Column(DateTime, default=datetime.utcnow)
    extraction_success = Column(Boolean, default=True)
    errors_encountered = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = relationship("Product", back_populates="brand", cascade="all, delete-orphan")
    policies = relationship("Policy", back_populates="brand", cascade="all, delete-orphan")
    faqs = relationship("FAQ", back_populates="brand", cascade="all, delete-orphan")
    social_handles = relationship("SocialHandle", back_populates="brand", cascade="all, delete-orphan")
    contact_info = relationship("ContactInfo", back_populates="brand", cascade="all, delete-orphan")
    important_links = relationship("ImportantLink", back_populates="brand", cascade="all, delete-orphan")

class Product(Base):
    """Table for storing product information"""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    
    external_id = Column(String(255), nullable=True)
    title = Column(String(500))
    handle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    price = Column(String(50), nullable=True)
    compare_at_price = Column(String(50), nullable=True)
    availability = Column(Boolean, nullable=True)
    image_url = Column(Text, nullable=True)
    product_url = Column(Text, nullable=True)
    vendor = Column(String(255), nullable=True)
    product_type = Column(String(255), nullable=True)
    tags = Column(JSON, nullable=True)
    is_hero_product = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    brand = relationship("BrandInsights", back_populates="products")

class Policy(Base):
    """Table for storing policies (privacy, return, etc.)"""
    
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    
    policy_type = Column(String(100))  # privacy, return_refund, terms_of_service
    title = Column(String(500))
    content = Column(Text)
    url = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    brand = relationship("BrandInsights", back_populates="policies")

class FAQ(Base):
    """Table for storing FAQ items"""
    
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    
    question = Column(Text)
    answer = Column(Text)
    category = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    brand = relationship("BrandInsights", back_populates="faqs")

class SocialHandle(Base):
    """Table for storing social media handles"""
    
    __tablename__ = "social_handles"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    
    platform = Column(String(100))
    url = Column(Text)
    username = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    brand = relationship("BrandInsights", back_populates="social_handles")

class ContactInfo(Base):
    """Table for storing contact information"""
    
    __tablename__ = "contact_info"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    
    emails = Column(JSON, nullable=True)
    phone_numbers = Column(JSON, nullable=True)
    addresses = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    brand = relationship("BrandInsights", back_populates="contact_info")

class ImportantLink(Base):
    """Table for storing important links"""
    
    __tablename__ = "important_links"
    
    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    
    title = Column(String(500))
    url = Column(Text)
    category = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    brand = relationship("BrandInsights", back_populates="important_links")