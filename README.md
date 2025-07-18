# 🛍️ Shopify Store Insights Fetcher

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)](https://www.sqlite.org/)

A comprehensive Python application that extracts detailed insights from Shopify stores using web scraping techniques. Built with FastAPI, this application provides automated data extraction and structured storage across multiple database tables for comprehensive e-commerce analysis.

## 🎯 **Overview**

This application automatically extracts key business information from Shopify stores including product catalogs, brand details, social media handles, contact information, policies, and important links. All data is organized and stored in a sophisticated SQLite database with 7 specialized tables for efficient analysis and retrieval.

## ✅ **Implemented Features**

- **📦 Product Catalog Extraction** - Extracts products from `/products.json` endpoint
- **🏪 Brand Information** - Captures brand name and domain details  
- **📱 Social Media Discovery** - Finds Instagram, Facebook, Twitter, TikTok links
- **📞 Contact Information** - Extracts email addresses and phone numbers
- **🏷️ Product Tags** - Captures product categories and tags
- **📋 Store Policies** - Extracts privacy policies and terms of service
- **🔗 Important Links** - Discovers key navigation and support links
- **💾 Structured Database Storage** - Stores data across 7 specialized tables with 8 indexes
- **🔍 Health Monitoring** - Health check endpoint for system status
- **📖 API Documentation** - Interactive Swagger/OpenAPI documentation
- **⚡ RESTful API** - Clean POST endpoint for data extraction
- **🛡️ Error Handling** - Graceful handling of failed extractions
- **📝 Logging** - Application logging for debugging
- **🗄️ Performance Optimization** - Database indexes for fast queries

## 🏗️ **Project Structure**

```
shopify-insights-fetcher/
├── main.py                 # FastAPI application (main file)
├── requirements.txt        # Python dependencies  
├── .env                   # Environment configuration
├── shopify_insights.db    # SQLite database (created on first run)
├── logs/                  # Application logs (created automatically)
└── README.md              # This file
```

## 🛠️ **Installation & Setup**

### **Prerequisites**
- Python 3.8 or higher
- Virtual environment (recommended)

### **Quick Start**

1. **Clone/Download the project**
```bash
cd shopify-insights-fetcher
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install fastapi uvicorn pydantic requests beautifulsoup4 lxml python-dotenv sqlalchemy
```

4. **Start Application**
```bash
python main.py
```

5. **Verify Installation**
```bash
# Health check
curl http://localhost:8000/health

# API documentation
# Visit: http://localhost:8000/docs
```

## 📖 **Usage**

### **API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Application health check |
| `/docs` | GET | Interactive API documentation |
| `/` | GET | Basic application info |
| `/api/v1/extract-insights` | POST | Extract insights from Shopify store |
| `/api/v1/status` | GET | Application status |

### **Extract Insights**

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/extract-insights" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://allbirds.com"}'
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/extract-insights" -Method POST -ContentType "application/json" -Body '{"website_url": "https://allbirds.com"}'
```

**Response Example:**
```json
{
  "success": true,
  "message": "Insights extracted successfully",
  "data": {
    "brand_name": "Allbirds",
    "domain": "allbirds.com",
    "website_url": "https://allbirds.com",
    "total_products": 156,
    "product_catalog": [
      {
        "id": 123456789,
        "title": "Tree Runners",
        "handle": "tree-runners",
        "vendor": "Allbirds",
        "product_type": "Shoes",
        "variants": [
          {
            "price": "98.00",
            "title": "Allbirds Tree Runners"
          }
        ]
      }
    ],
    "social_handles": [
      {
        "platform": "instagram",
        "url": "https://instagram.com/allbirds",
        "username": "allbirds"
      }
    ],
    "contact_info": {
      "emails": ["help@allbirds.com"]
    },
    "extraction_timestamp": "2025-07-18T21:54:05.892000",
    "extraction_success": true,
    "scraping_method": "comprehensive"
  }
}
```

## 🗄️ **Database Architecture**

### **SQLite Database Overview**
Data is automatically stored in `shopify_insights.db` with a sophisticated, normalized structure designed for efficient storage and retrieval.

**Database Statistics:**
- **SQLite Version:** 3.45.3
- **File Size:** 65.5 kB
- **Tables:** 7 specialized tables
- **Indexes:** 8 performance indexes
- **Created:** July 18, 2025 at 07:16 PM
- **Last Modified:** July 18, 2025 at 07:16 PM

### **Database Tables Structure**

| Table Name | Purpose | Key Data Stored |
|------------|---------|-----------------|
| **`brand_insights`** | Main brand information | Brand name, domain, product counts, extraction metadata |
| **`products`** | Individual product details | Product titles, prices, variants, images, SKUs |
| **`social_handles`** | Social media presence | Platform names, URLs, usernames for each social network |
| **`contact_info`** | Contact details | Email addresses, phone numbers, support contacts |
| **`tags`** | Product categorization | Product tags, categories, classification keywords |
| **`policies`** | Store policies | Privacy policies, terms of service, return policies |
| **`important_links`** | Key website navigation | Support pages, help centers, account links, blogs |

### **Main Table: `brand_insights`**
Primary table containing core extraction data:
- `id` - Primary key
- `brand_name` - Extracted brand name
- `domain` - Store domain (e.g., allbirds.com)
- `website_url` - Full store URL
- `total_products` - Number of products found
- `product_catalog` - JSON data of products
- `social_handles` - JSON data of social media links
- `contact_info` - JSON data of contact details
- `extraction_data` - Full JSON response
- `extraction_success` - Boolean success status
- `created_at` - Timestamp of extraction
- `updated_at` - Last update timestamp

### **Database Performance Features**
- **8 Optimized Indexes** - Fast queries across all tables
- **Normalized Structure** - Data properly separated into related tables
- **JSON Storage** - Complex data stored as JSON for flexibility
- **Automatic Timestamps** - Track when data was created/updated
- **Foreign Key Relationships** - Proper data integrity between tables

## 🔍 **Database Web Interface**

### **Accessing Your Data**

**SQLite Web Browser (Recommended):**
```bash
pip install sqlite-web
sqlite_web shopify_insights.db
# Visit: http://localhost:8080
```

**What You'll See:**
When you access the web interface, you'll see a comprehensive database dashboard showing:

- **Database Overview Panel:**
  - SQLite version (3.45.3)
  - Database file size (65.5 kB)
  - Creation and modification timestamps
  - Total tables (7) and indexes (8)

- **Table Navigation:**
  - `brand_insights` - Main extraction data
  - `contact_info` - Email and phone data
  - `tags` - Product categories and tags
  - `important_links` - Key website links
  - `policies` - Store policies and terms
  - `products` - Complete product catalog
  - `social_handles` - Social media accounts

- **Interactive Features:**
  - Click any table name to browse data
  - Run custom SQL queries
  - Export data in various formats
  - View table schemas and relationships

### **Sample Database Queries**

**Command Line Access:**
```bash
sqlite3 shopify_insights.db

# List all tables
.tables

# View recent extractions
SELECT brand_name, domain, total_products, created_at 
FROM brand_insights 
ORDER BY created_at DESC;

# View social media presence
SELECT platform, username, url 
FROM social_handles 
WHERE domain = 'allbirds.com';

# Count products by vendor
SELECT vendor, COUNT(*) as product_count 
FROM products 
GROUP BY vendor;

# Find contact information
SELECT emails, phones 
FROM contact_info 
WHERE domain = 'allbirds.com';
```

**Advanced Queries:**
```sql
-- Get extraction summary with social media count
SELECT 
  b.brand_name,
  b.domain,
  b.total_products,
  COUNT(s.platform) as social_platforms,
  b.extraction_success,
  b.created_at
FROM brand_insights b
LEFT JOIN social_handles s ON b.domain = s.domain
GROUP BY b.domain
ORDER BY b.created_at DESC;

-- Find stores with the most products
SELECT brand_name, domain, total_products 
FROM brand_insights 
WHERE extraction_success = 1 
ORDER BY total_products DESC 
LIMIT 10;

-- Get all available contact methods
SELECT domain, emails, phones 
FROM contact_info 
WHERE (emails IS NOT NULL AND emails != '[]') 
   OR (phones IS NOT NULL AND phones != '[]');
```

## 🧪 **Testing**

### **Manual Testing**
Test with verified Shopify stores:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test with different Shopify stores
curl -X POST "http://localhost:8000/api/v1/extract-insights" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://gymshark.com"}'

curl -X POST "http://localhost:8000/api/v1/extract-insights" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://bombas.com"}'
```

### **Expected Results**
For a successful extraction, you should see:
- ✅ `success: true`
- ✅ `total_products > 0`
- ✅ Product array with titles and prices
- ✅ At least one social media handle
- ✅ Data stored across multiple database tables
- ✅ Database file size increases after extraction

### **Verification Steps**
After running an extraction:
1. **Check API Response** - Verify JSON structure and data
2. **Check Database** - Visit http://localhost:8080 to see stored data
3. **Check Tables** - Confirm data appears in relevant tables
4. **Check Relationships** - Verify data is properly linked across tables

## ⚙️ **Configuration**

### **Environment Variables (.env file)**
```bash
DATABASE_URL=sqlite:///./shopify_insights.db
API_HOST=127.0.0.1
API_PORT=8000
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
```

### **Required Python Packages**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==6.0.0
python-dotenv==1.0.0
sqlalchemy==2.0.23
```

## 🔧 **Troubleshooting**

### **Common Issues**

**Application won't start:**
```bash
# Check if virtual environment is activated
# Should see (venv) in your prompt

# Reinstall dependencies
pip install fastapi uvicorn pydantic requests beautifulsoup4 lxml python-dotenv sqlalchemy
```

**Import errors:**
```bash
# Make sure all packages are installed
pip list | grep fastapi
pip list | grep beautifulsoup4
```

**Extraction fails:**
```bash
# Check application logs in terminal
# Try with a different Shopify store
# Ensure internet connection is working
```

**Database issues:**
```bash
# Database file will be created automatically
# Check if shopify_insights.db exists in project folder
# Verify database with: sqlite3 shopify_insights.db ".tables"
```

**Web interface not loading:**
```bash
# Make sure sqlite-web is installed
pip install sqlite-web

# Check if database file exists
ls -la shopify_insights.db

# Restart sqlite-web
sqlite_web shopify_insights.db
```

## 📊 **Data Extraction Details**

### **Product Information** (stored in `products` table)
- Product ID and title
- Product handle (URL slug)
- Vendor/brand name
- Product type/category
- Pricing information
- Product variants (size, color, etc.)
- Product images and media
- Creation/update timestamps
- Inventory tracking codes

### **Social Media Handles** (stored in `social_handles` table)
- Instagram profiles and usernames
- Facebook pages and handles
- Twitter/X accounts
- TikTok profiles
- YouTube channels
- LinkedIn company pages
- Pinterest accounts

### **Contact Information** (stored in `contact_info` table)
- Customer service emails
- Support contact emails
- Phone numbers (customer service, sales)
- Contact form URLs
- Live chat availability

### **Product Tags & Categories** (stored in `tags` table)
- Product category tags
- Style and type classifications
- Brand-specific tags
- Seasonal tags
- Collection names

### **Store Policies** (stored in `policies` table)
- Privacy policy content
- Terms of service
- Return and refund policies
- Shipping policies
- Cookie policies

### **Important Links** (stored in `important_links` table)
- Customer account pages
- Support and help centers
- FAQ pages
- Order tracking links
- Blog and content pages
- About us pages

### **Brand Details** (stored in `brand_insights` table)
- Complete brand/store name
- Domain and subdomain information
- Total product inventory count
- Extraction success metrics
- Timestamp and version tracking

## 🎯 **Use Cases**

- **Competitor Research** - Analyze competitor product catalogs, pricing, and positioning
- **Market Analysis** - Study product trends and category performance across multiple stores
- **Lead Generation** - Find contact information for business outreach and partnerships
- **Social Media Research** - Discover brand social media presence and engagement strategies
- **E-commerce Intelligence** - Gather comprehensive data for business decisions
- **Policy Analysis** - Compare terms of service and policies across competitors
- **SEO Research** - Analyze product tags and categorization strategies

## ⚠️ **Limitations & Considerations**

- **Rate Limiting** - Some stores may block rapid or repeated requests
- **Dynamic Content** - JavaScript-rendered content may not be captured completely
- **Site Structure** - Results depend on standard Shopify structure and conventions
- **Large Stores** - Very large catalogs (1000+ products) may take longer to process
- **Network Dependent** - Requires stable internet connection for reliable extraction
- **Data Privacy** - Ensure compliance with data protection regulations when storing extracted data
- **Terms of Service** - Respect individual store terms of service and robots.txt files

## 🚀 **Performance Metrics**

Based on testing with real Shopify stores:

- **Average Response Time:** 15-45 seconds per store
- **Typical Product Count:** 50-500 products extracted
- **Database Growth:** ~1-5 KB per store extraction
- **Success Rate:** 85-95% with major Shopify stores
- **Memory Usage:** 50-200 MB during extraction
- **Concurrent Capacity:** Handles 3-5 simultaneous extractions

## 📄 **License**

This project is licensed under the MIT License.

