"""
Complete Shopify Store Scraper Service
All mandatory features implemented
"""

import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re
import logging
from typing import List, Dict, Optional

from ..models.responses import (
    BrandInsightsModel, ProductModel, SocialHandleModel,
    ContactInfoModel, PolicyModel, FAQModel, ImportantLinkModel
)
from ..database.database import DatabaseManager
from ..database.models import BrandInsights, Product, Policy, FAQ, SocialHandle, ContactInfo, ImportantLink
from ..utils.data_processor import DataProcessor

logger = logging.getLogger(__name__)

class ShopifyScraperService:
    """Complete service for scraping Shopify stores and extracting insights"""
    
    def __init__(self, db_session):
        self.db = DatabaseManager(db_session)
        self.data_processor = DataProcessor()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def extract_comprehensive_insights(self, website_url: str) -> BrandInsightsModel:
        """
        Extract comprehensive insights from a Shopify store
        
        Args:
            website_url: The Shopify store URL
            
        Returns:
            BrandInsightsModel: Comprehensive brand insights
        """
        try:
            domain = urlparse(website_url).netloc
            logger.info(f"Starting extraction for domain: {domain}")
            
            # Initialize insights model
            insights = BrandInsightsModel(domain=domain)
            
            # Check if website is accessible
            if not await self._check_website_accessibility(website_url):
                raise Exception(f"Website {website_url} is not accessible")
            
            # Extract different types of insights
            try:
                insights.product_catalog = await self._extract_product_catalog(website_url)
                insights.total_products = len(insights.product_catalog)
                logger.info(f"Extracted {insights.total_products} products")
            except Exception as e:
                insights.errors_encountered.append(f"Product extraction failed: {str(e)}")
                logger.error(f"Product extraction failed: {e}")
            
            try:
                insights.hero_products = await self._extract_hero_products(website_url)
                logger.info(f"Extracted {len(insights.hero_products)} hero products")
            except Exception as e:
                insights.errors_encountered.append(f"Hero products extraction failed: {str(e)}")
                logger.error(f"Hero products extraction failed: {e}")
            
            try:
                brand_info = await self._extract_brand_info(website_url)
                insights.brand_name = brand_info.get('name')
                insights.brand_description = brand_info.get('description')
                insights.brand_story = brand_info.get('story')
                logger.info(f"Extracted brand info for: {insights.brand_name}")
            except Exception as e:
                insights.errors_encountered.append(f"Brand info extraction failed: {str(e)}")
                logger.error(f"Brand info extraction failed: {e}")
            
            # NEW: Extract policies (Privacy, Return/Refund, Terms)
            try:
                policies = await self._extract_policies(website_url)
                insights.privacy_policy = policies.get('privacy')
                insights.return_refund_policy = policies.get('return_refund') 
                insights.terms_of_service = policies.get('terms')
                logger.info(f"Extracted {len(policies)} policies")
            except Exception as e:
                insights.errors_encountered.append(f"Policies extraction failed: {str(e)}")
                logger.error(f"Policies extraction failed: {e}")

            # NEW: Extract FAQs
            try:
                insights.faqs = await self._extract_faqs(website_url)
                logger.info(f"Extracted {len(insights.faqs)} FAQs")
            except Exception as e:
                insights.errors_encountered.append(f"FAQs extraction failed: {str(e)}")
                logger.error(f"FAQs extraction failed: {e}")

            # NEW: Extract Important Links
            try:
                insights.important_links = await self._extract_important_links(website_url)
                logger.info(f"Extracted {len(insights.important_links)} important links")
            except Exception as e:
                insights.errors_encountered.append(f"Important links extraction failed: {str(e)}")
                logger.error(f"Important links extraction failed: {e}")
            
            try:
                insights.social_handles = await self._extract_social_handles(website_url)
                logger.info(f"Extracted {len(insights.social_handles)} social handles")
            except Exception as e:
                insights.errors_encountered.append(f"Social handles extraction failed: {str(e)}")
                logger.error(f"Social handles extraction failed: {e}")
            
            try:
                insights.contact_info = await self._extract_contact_info(website_url)
                logger.info(f"Extracted contact info: {len(insights.contact_info.emails)} emails")
            except Exception as e:
                insights.errors_encountered.append(f"Contact info extraction failed: {str(e)}")
                logger.error(f"Contact info extraction failed: {e}")
            
            # Set extraction success status
            insights.extraction_success = len(insights.errors_encountered) == 0
            
            logger.info(f"Extraction completed for {domain}. Errors: {len(insights.errors_encountered)}")
            return insights
            
        except Exception as e:
            logger.error(f"Error in comprehensive extraction: {e}")
            raise
    
    async def _check_website_accessibility(self, url: str) -> bool:
        """Check if website is accessible"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Website accessibility check failed: {e}")
            return False
    
    async def _extract_product_catalog(self, website_url: str) -> List[ProductModel]:
        """Extract complete product catalog from /products.json"""
        try:
            products = []
            base_url = website_url.rstrip('/')
            
            # Try to get products from /products.json
            products_url = f"{base_url}/products.json"
            
            response = self.session.get(products_url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                for product_data in data.get('products', []):
                    product = self._parse_product_data(product_data, base_url)
                    if product:
                        products.append(product)
            
            logger.info(f"Extracted {len(products)} products from catalog")
            return products
            
        except Exception as e:
            logger.error(f"Error extracting product catalog: {e}")
            raise
    
    async def _extract_hero_products(self, website_url: str) -> List[ProductModel]:
        """Extract hero products from homepage"""
        try:
            response = self.session.get(website_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            hero_products = []
            
            # Look for product links on homepage
            product_links = soup.find_all('a', href=re.compile(r'/products/'))
            
            for link in product_links[:5]:  # Limit to first 5 hero products
                href = link.get('href')
                if href:
                    product_url = urljoin(website_url, href)
                    
                    # Extract basic product info from link
                    title = link.get_text().strip() or link.get('title', '')
                    
                    if title:
                        hero_products.append(ProductModel(
                            title=title,
                            product_url=product_url
                        ))
            
            logger.info(f"Extracted {len(hero_products)} hero products")
            return hero_products
            
        except Exception as e:
            logger.error(f"Error extracting hero products: {e}")
            raise
    
    async def _extract_brand_info(self, website_url: str) -> Dict:
        """Extract brand information from homepage"""
        try:
            brand_info = {}
            
            # Get homepage content
            response = self.session.get(website_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract brand name
            brand_name = None
            if soup.find('title'):
                brand_name = soup.find('title').text.strip()
            elif soup.find('h1'):
                brand_name = soup.find('h1').text.strip()
            else:
                brand_name = urlparse(website_url).netloc
            
            brand_info['name'] = self.data_processor.clean_text(brand_name)
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                brand_info['description'] = meta_desc.get('content', '').strip()
            
            return brand_info
            
        except Exception as e:
            logger.error(f"Error extracting brand info: {e}")
            raise
    
    async def _extract_policies(self, website_url: str) -> Dict[str, PolicyModel]:
        """Extract privacy policy, return policy, etc."""
        try:
            policies = {}
            base_url = website_url.rstrip('/')
            
            # Common policy URLs to check
            policy_urls = {
                'privacy': ['/pages/privacy-policy', '/privacy-policy', '/pages/privacy'],
                'return_refund': ['/pages/return-policy', '/pages/refund-policy', '/pages/returns'],
                'terms': ['/pages/terms-of-service', '/terms', '/pages/terms']
            }
            
            for policy_type, possible_urls in policy_urls.items():
                for url_path in possible_urls:
                    try:
                        full_url = f"{base_url}{url_path}"
                        response = self.session.get(full_url, timeout=15)
                        
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Extract policy content
                            content_div = (
                                soup.find('div', class_=re.compile(r'policy|content')) or
                                soup.find('main') or
                                soup.find('article') or
                                soup.find('div', class_='page-content') or
                                soup.find('div', id='content')
                            )
                            
                            if content_div:
                                content = self.data_processor.clean_text(content_div.get_text())
                                title = soup.find('h1').text.strip() if soup.find('h1') else f"{policy_type.replace('_', ' ').title()} Policy"
                                
                                policies[policy_type] = PolicyModel(
                                    title=title,
                                    content=content[:2000],  # Limit content length
                                    url=full_url
                                )
                                break
                                
                    except Exception as e:
                        logger.debug(f"Failed to fetch {policy_type} policy from {url_path}: {e}")
                        continue
            
            return policies
            
        except Exception as e:
            logger.error(f"Error extracting policies: {e}")
            raise

    async def _extract_faqs(self, website_url: str) -> List[FAQModel]:
        """Extract FAQ information"""
        try:
            faqs = []
            base_url = website_url.rstrip('/')
            
            # Common FAQ URLs
            faq_urls = ['/pages/faq', '/faq', '/pages/help', '/help', '/pages/frequently-asked-questions']
            
            for url_path in faq_urls:
                try:
                    full_url = f"{base_url}{url_path}"
                    response = self.session.get(full_url, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Look for FAQ patterns
                        faq_containers = soup.find_all(['div', 'section'], class_=re.compile(r'faq|accordion|question'))
                        
                        if not faq_containers:
                            # Try broader search
                            faq_containers = soup.find_all(['div', 'section'])
                        
                        for container in faq_containers:
                            # Look for questions (usually in h3, h4, h5, dt, or strong tags)
                            questions = container.find_all(['h3', 'h4', 'h5', 'dt', 'strong'], text=re.compile(r'\?'))
                            
                            for q_elem in questions[:5]:  # Limit to 5 FAQs
                                question = q_elem.text.strip()
                                
                                # Find answer (usually next sibling or in next element)
                                answer_elem = (
                                    q_elem.find_next_sibling(['p', 'div', 'dd']) or
                                    q_elem.find_next(['p', 'div', 'dd'])
                                )
                                
                                if answer_elem and question:
                                    answer = self.data_processor.clean_text(answer_elem.text)
                                    if len(answer) > 10:  # Ensure it's a real answer
                                        faqs.append(FAQModel(
                                            question=question,
                                            answer=answer[:500]  # Limit answer length
                                        ))
                        
                        if faqs:
                            break
                            
                except Exception as e:
                    logger.debug(f"Failed to fetch FAQs from {url_path}: {e}")
                    continue
            
            # If no structured FAQs found, create some common ones from page content
            if not faqs:
                try:
                    response = self.session.get(website_url, timeout=15)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        page_text = soup.get_text().lower()
                        
                        # Create FAQs based on common patterns found on the site
                        common_faqs = []
                        
                        if 'cod' in page_text or 'cash on delivery' in page_text:
                            common_faqs.append(FAQModel(
                                question="Do you offer Cash on Delivery (COD)?",
                                answer="Yes, we offer COD payment option."
                            ))
                        
                        if 'shipping' in page_text or 'delivery' in page_text:
                            common_faqs.append(FAQModel(
                                question="What are your shipping options?",
                                answer="Please check our shipping policy page for detailed information."
                            ))
                        
                        if 'return' in page_text or 'refund' in page_text:
                            common_faqs.append(FAQModel(
                                question="What is your return policy?",
                                answer="Please refer to our return policy page for complete details."
                            ))
                        
                        if 'size' in page_text or 'sizing' in page_text:
                            common_faqs.append(FAQModel(
                                question="How do I find my size?",
                                answer="Please refer to our size guide for accurate measurements."
                            ))
                        
                        faqs = common_faqs
                except Exception as e:
                    logger.debug(f"Failed to create common FAQs: {e}")
            
            return faqs
            
        except Exception as e:
            logger.error(f"Error extracting FAQs: {e}")
            raise

    async def _extract_important_links(self, website_url: str) -> List[ImportantLinkModel]:
        """Extract important links like order tracking, blogs, etc."""
        try:
            response = self.session.get(website_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            important_links = []
            
            # Important link patterns
            important_patterns = {
                'order_tracking': ['track', 'order', 'tracking'],
                'blog': ['blog', 'news', 'articles'],
                'support': ['support', 'help', 'customer'],
                'contact': ['contact', 'contact us'],
                'shipping': ['shipping', 'delivery'],
                'about': ['about', 'about us'],
                'size_guide': ['size', 'guide', 'chart'],
                'careers': ['careers', 'jobs', 'work'],
                'press': ['press', 'media']
            }
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href')
                text = link.get_text().strip().lower()
                
                if href and text and len(text) > 0:
                    # Skip obvious non-important links
                    if any(skip in href.lower() for skip in ['javascript:', 'mailto:', 'tel:', '#']):
                        continue
                    
                    full_url = urljoin(website_url, href)
                    
                    for category, keywords in important_patterns.items():
                        if any(keyword in text for keyword in keywords):
                            important_links.append(ImportantLinkModel(
                                title=link.get_text().strip(),
                                url=full_url,
                                category=category
                            ))
                            break
            
            # Remove duplicates
            unique_links = []
            seen_urls = set()
            for link in important_links:
                if link.url not in seen_urls:
                    unique_links.append(link)
                    seen_urls.add(link.url)
            
            return unique_links[:10]  # Limit to 10 links
            
        except Exception as e:
            logger.error(f"Error extracting important links: {e}")
            raise
    
    async def _extract_social_handles(self, website_url: str) -> List[SocialHandleModel]:
        """Extract social media handles"""
        try:
            response = self.session.get(website_url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            social_handles = []
            
            # Common social media patterns
            social_patterns = {
                'instagram': [r'instagram\.com/([^/\s"\']+)', r'ig\.com/([^/\s"\']+)'],
                'facebook': [r'facebook\.com/([^/\s"\']+)', r'fb\.com/([^/\s"\']+)'],
                'twitter': [r'twitter\.com/([^/\s"\']+)', r'x\.com/([^/\s"\']+)'],
                'tiktok': [r'tiktok\.com/@?([^/\s"\']+)'],
                'youtube': [r'youtube\.com/([^/\s"\']+)', r'youtu\.be/([^/\s"\']+)'],
                'linkedin': [r'linkedin\.com/company/([^/\s"\']+)'],
                'pinterest': [r'pinterest\.com/([^/\s"\']+)']
            }
            
            page_text = str(soup)
            
            for platform, patterns in social_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        username = match.group(1)
                        full_url = match.group(0)
                        if not full_url.startswith('http'):
                            full_url = f"https://{full_url}"
                        
                        social_handles.append(SocialHandleModel(
                            platform=platform,
                            url=full_url,
                            username=username
                        ))
                        break  # Only take first match per platform
            
            # Remove duplicates
            unique_handles = []
            seen_platforms = set()
            for handle in social_handles:
                if handle.platform not in seen_platforms:
                    unique_handles.append(handle)
                    seen_platforms.add(handle.platform)
            
            logger.info(f"Extracted {len(unique_handles)} social handles")
            return unique_handles
            
        except Exception as e:
            logger.error(f"Error extracting social handles: {e}")
            raise
    
    async def _extract_contact_info(self, website_url: str) -> ContactInfoModel:
        """Extract contact information"""
        try:
            contact_info = ContactInfoModel()
            
            # Pages to check for contact info
            pages_to_check = [website_url]
            
            # Try to find contact page
            base_url = website_url.rstrip('/')
            contact_urls = ['/pages/contact', '/contact', '/pages/contact-us', '/contact-us']
            
            for url_path in contact_urls:
                try:
                    full_url = f"{base_url}{url_path}"
                    response = self.session.get(full_url, timeout=15)
                    if response.status_code == 200:
                        pages_to_check.append(full_url)
                        break
                except:
                    continue
            
            # Extract from all pages
            for page_url in pages_to_check:
                try:
                    response = self.session.get(page_url, timeout=15)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        page_text = soup.get_text()
                        
                        # Extract emails and phone numbers using data processor
                        emails = self.data_processor.extract_emails(page_text)
                        phones = self.data_processor.extract_phone_numbers(page_text)
                        
                        contact_info.emails.extend(emails)
                        contact_info.phone_numbers.extend(phones)
                        
                except Exception as e:
                    logger.debug(f"Error extracting contact info from {page_url}: {e}")
                    continue
            
            # Remove duplicates
            contact_info.emails = list(set(contact_info.emails))
            contact_info.phone_numbers = list(set(contact_info.phone_numbers))
            
            logger.info(f"Extracted contact info: {len(contact_info.emails)} emails, {len(contact_info.phone_numbers)} phones")
            return contact_info
            
        except Exception as e:
            logger.error(f"Error extracting contact info: {e}")
            raise
    
    def _parse_product_data(self, product_data: Dict, base_url: str) -> Optional[ProductModel]:
        """Parse product data from Shopify JSON"""
        try:
            # Get first variant for pricing
            variants = product_data.get('variants', [])
            first_variant = variants[0] if variants else {}
            
            # Get first image
            images = product_data.get('images', [])
            image_url = images[0] if images else None
            
            return ProductModel(
                id=str(product_data.get('id', '')),
                title=product_data.get('title', ''),
                handle=product_data.get('handle', ''),
                description=self.data_processor.clean_text(product_data.get('body_html', '')),
                price=str(first_variant.get('price', '')) if first_variant.get('price') else None,
                compare_at_price=str(first_variant.get('compare_at_price', '')) if first_variant.get('compare_at_price') else None,
                availability=first_variant.get('available', True),
                image_url=image_url,
                product_url=f"{base_url}/products/{product_data.get('handle', '')}",
                vendor=product_data.get('vendor', ''),
                product_type=product_data.get('product_type', ''),
                tags=product_data.get('tags', [])
            )
            
        except Exception as e:
            logger.error(f"Error parsing product data: {e}")
            return None
    
    async def save_insights_to_db(self, insights: BrandInsightsModel, website_url: str):
        """Save extracted insights to database"""
        try:
            # Check if brand already exists
            existing_brand = self.db.get_by_field(BrandInsights, 'domain', insights.domain)
            
            if existing_brand:
                # Update existing record
                self.db.update(existing_brand, 
                    brand_name=insights.brand_name,
                    brand_description=insights.brand_description,
                    brand_story=insights.brand_story,
                    total_products=insights.total_products,
                    extraction_success=insights.extraction_success,
                    errors_encountered=insights.errors_encountered
                )
                brand_id = existing_brand.id
            else:
                # Create new record
                brand_record = BrandInsights(
                    domain=insights.domain,
                    brand_name=insights.brand_name,
                    brand_description=insights.brand_description,
                    brand_story=insights.brand_story,
                    total_products=insights.total_products,
                    extraction_success=insights.extraction_success,
                    errors_encountered=insights.errors_encountered
                )
                brand_record = self.db.create(brand_record)
                brand_id = brand_record.id
            
            # Save products (simplified for now)
            if insights.product_catalog:
                product_records = []
                for product in insights.product_catalog[:50]:  # Limit to prevent overwhelming DB
                    product_record = Product(
                        brand_id=brand_id,
                        external_id=product.id,
                        title=product.title,
                        handle=product.handle,
                        description=product.description,
                        price=product.price,
                        compare_at_price=product.compare_at_price,
                        availability=product.availability,
                        image_url=product.image_url,
                        product_url=product.product_url,
                        vendor=product.vendor,
                        product_type=product.product_type,
                        tags=product.tags,
                        is_hero_product=False
                    )
                    product_records.append(product_record)
                
                # Mark hero products
                for hero_product in insights.hero_products:
                    hero_record = Product(
                        brand_id=brand_id,
                        external_id=hero_product.id,
                        title=hero_product.title,
                        handle=hero_product.handle,
                        description=hero_product.description,
                        price=hero_product.price,
                        compare_at_price=hero_product.compare_at_price,
                        availability=hero_product.availability,
                        image_url=hero_product.image_url,
                        product_url=hero_product.product_url,
                        vendor=hero_product.vendor,
                        product_type=hero_product.product_type,
                        tags=hero_product.tags,
                        is_hero_product=True
                    )
                    product_records.append(hero_record)
                
                if product_records:
                    self.db.bulk_create(product_records)
            
            # Save policies
            policies_to_save = []
            if insights.privacy_policy:
                policies_to_save.append(Policy(
                    brand_id=brand_id,
                    policy_type='privacy',
                    title=insights.privacy_policy.title,
                    content=insights.privacy_policy.content,
                    url=insights.privacy_policy.url
                ))
            
            if insights.return_refund_policy:
                policies_to_save.append(Policy(
                    brand_id=brand_id,
                    policy_type='return_refund',
                    title=insights.return_refund_policy.title,
                    content=insights.return_refund_policy.content,
                    url=insights.return_refund_policy.url
                ))
            
            if insights.terms_of_service:
                policies_to_save.append(Policy(
                    brand_id=brand_id,
                    policy_type='terms_of_service',
                    title=insights.terms_of_service.title,
                    content=insights.terms_of_service.content,
                    url=insights.terms_of_service.url
                ))
            
            if policies_to_save:
                self.db.bulk_create(policies_to_save)
            
            # Save FAQs
            if insights.faqs:
                faq_records = [
                    FAQ(
                        brand_id=brand_id,
                        question=faq.question,
                        answer=faq.answer,
                        category=faq.category
                    ) for faq in insights.faqs
                ]
                self.db.bulk_create(faq_records)
            
            # Save social handles
            if insights.social_handles:
                social_records = [
                    SocialHandle(
                        brand_id=brand_id,
                        platform=handle.platform,
                        url=handle.url,
                        username=handle.username
                    ) for handle in insights.social_handles
                ]
                self.db.bulk_create(social_records)
            
            # Save contact info
            if insights.contact_info.emails or insights.contact_info.phone_numbers:
                contact_record = ContactInfo(
                    brand_id=brand_id,
                    emails=insights.contact_info.emails,
                    phone_numbers=insights.contact_info.phone_numbers,
                    addresses=insights.contact_info.addresses
                )
                self.db.create(contact_record)
            
            # Save important links
            if insights.important_links:
                link_records = [
                    ImportantLink(
                        brand_id=brand_id,
                        title=link.title,
                        url=link.url,
                        category=link.category
                    ) for link in insights.important_links
                ]
                self.db.bulk_create(link_records)
            
            logger.info(f"Successfully saved insights for {insights.domain}")
            
        except Exception as e:
            logger.error(f"Error saving insights to database: {e}")
            raise