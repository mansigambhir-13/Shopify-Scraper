"""
Data processing utilities for cleaning and structuring extracted data
"""

import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import html
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Utility class for processing and cleaning extracted data"""
    
    def __init__(self):
        # Common words to filter out from product titles/descriptions
        self.stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        try:
            # Decode HTML entities
            text = html.unescape(text)
            
            # Remove HTML tags if any
            soup = BeautifulSoup(text, 'html.parser')
            text = soup.get_text()
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove extra newlines
            text = re.sub(r'\n+', '\n', text)
            
            # Strip leading/trailing whitespace
            text = text.strip()
            
            return text
            
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return text
    
    def extract_emails(self, text: str) -> List[str]:
        """
        Extract email addresses from text
        
        Args:
            text: Text to extract emails from
            
        Returns:
            List of unique email addresses
        """
        if not text:
            return []
        
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            
            # Filter out common false positives
            filtered_emails = []
            for email in emails:
                if not any(ext in email.lower() for ext in ['.jpg', '.png', '.gif', '.pdf']):
                    filtered_emails.append(email.lower())
            
            return list(set(filtered_emails))
            
        except Exception as e:
            logger.error(f"Error extracting emails: {e}")
            return []
    
    def extract_phone_numbers(self, text: str) -> List[str]:
        """
        Extract phone numbers from text
        
        Args:
            text: Text to extract phone numbers from
            
        Returns:
            List of unique phone numbers
        """
        if not text:
            return []
        
        try:
            phone_patterns = [
                r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
                r'\+[0-9]{1,3}[-.\s]?[0-9]{1,14}',
                r'\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
            ]
            
            phones = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if isinstance(match, tuple):
                        phone = ''.join(match)
                    else:
                        phone = match
                    
                    # Basic validation - should have at least 10 digits
                    if len(re.sub(r'\D', '', phone)) >= 10:
                        phones.append(phone)
            
            return list(set(phones))
            
        except Exception as e:
            logger.error(f"Error extracting phone numbers: {e}")
            return []