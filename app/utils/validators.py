"""
Validation utilities for URLs and data
"""

import re
import requests
from urllib.parse import urlparse
import validators
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def validate_shopify_url(url: str) -> bool:
    """
    Validate if URL is a valid Shopify store
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Shopify URL, False otherwise
    """
    try:
        # Basic URL validation
        if not validators.url(url):
            return False
        
        # Parse URL
        parsed = urlparse(url)
        if not parsed.netloc:
            return False
        
        # Check if URL is accessible
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code >= 400:
                return False
        except requests.RequestException:
            return False
        
        # For basic validation, if it's accessible, consider it valid
        # We'll do more detailed Shopify checking in the scraper
        return True
    
    except Exception as e:
        logger.error(f"Error validating Shopify URL {url}: {e}")
        return False

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid email, False otherwise
    """
    try:
        return validators.email(email)
    except:
        return False

def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid phone number, False otherwise
    """
    try:
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it has reasonable length (7-15 digits)
        if len(digits_only) < 7 or len(digits_only) > 15:
            return False
        
        return True
        
    except:
        return False

def sanitize_url(url: str) -> Optional[str]:
    """
    Sanitize and normalize URL
    
    Args:
        url: URL to sanitize
        
    Returns:
        Sanitized URL or None if invalid
    """
    try:
        if not url:
            return None
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        # Parse and reconstruct URL
        parsed = urlparse(url)
        
        if not parsed.netloc:
            return None
        
        # Reconstruct with normalized components
        scheme = parsed.scheme or 'https'
        netloc = parsed.netloc.lower()
        path = parsed.path or '/'
        
        sanitized = f"{scheme}://{netloc}{path}"
        
        # Remove trailing slash unless it's the root
        if sanitized.endswith('/') and len(sanitized) > 1 and parsed.path != '/':
            sanitized = sanitized[:-1]
        
        return sanitized
        
    except Exception as e:
        logger.error(f"Error sanitizing URL {url}: {e}")
        return None