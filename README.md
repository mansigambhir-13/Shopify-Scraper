# 🛍️ Shopify Store Insights Fetcher

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)](https://www.sqlite.org/)

A Python application that extracts insights from Shopify stores using web scraping techniques. Built with FastAPI, this application provides automated data extraction and storage for e-commerce analysis.

## 🎯 **Overview**

This application automatically extracts key business information from Shopify stores including product catalogs, brand details, social media handles, and contact information. All data is stored in a local SQLite database for analysis.

## ✅ **Implemented Features**

- **📦 Product Catalog Extraction** - Extracts products from `/products.json` endpoint
- **🏪 Brand Information** - Captures brand name and domain details  
- **📱 Social Media Discovery** - Finds Instagram, Facebook, Twitter, TikTok links
- **📞 Contact Information** - Extracts email addresses and phone numbers
- **💾 Database Storage** - Stores all data in SQLite database
- **🔍 Health Monitoring** - Health check endpoint for system status
- **📖 API Documentation** - Interactive Swagger/OpenAPI documentation
- **⚡ RESTful API** - Clean POST endpoint for data extraction
- **🛡️ Error Handling** - Graceful handling of failed extractions
- **📝 Logging** - Application logging for debugging

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

## 🗄️ **Database**

### **SQLite Database**
Data is automatically stored in `shopify_insights.db` with the following structure:

**Main Table: `brand_insights`**
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

### **View Database Data**

**Option 1: SQLite Web Browser**
```bash
pip install sqlite-web
sqlite_web shopify_insights.db
# Visit: http://localhost:8080
```

**Option 2: Command Line**
```bash
sqlite3 shopify_insights.db
.tables
SELECT brand_name, domain, total_products FROM brand_insights;
```

## 🧪 **Testing**

### **Manual Testing**
Test with known Shopify stores:

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
- ✅ Data stored in SQLite database

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
# Try restarting the application
```

## 📊 **What Gets Extracted**

### **Product Information**
- Product ID and title
- Product handle (URL slug)
- Vendor/brand name
- Product type/category
- Pricing information
- Product variants
- Creation/update timestamps

### **Social Media Handles**
- Instagram profiles
- Facebook pages
- Twitter accounts
- TikTok profiles
- YouTube channels
- LinkedIn pages

### **Contact Information**
- Email addresses
- Phone numbers (when available)

### **Brand Details**
- Brand/store name
- Domain information
- Total product count
- Extraction metadata

## 🎯 **Use Cases**

- **Competitor Research** - Analyze competitor product catalogs and pricing
- **Market Analysis** - Study product trends across multiple stores
- **Lead Generation** - Find contact information for business outreach
- **Social Media Research** - Discover brand social media presence
- **E-commerce Intelligence** - Gather data for business decisions

## ⚠️ **Limitations**

- **Rate Limiting** - Some stores may block rapid requests
- **Dynamic Content** - JavaScript-rendered content may not be captured
- **Site Structure** - Results depend on standard Shopify structure
- **Large Stores** - Very large catalogs may take longer to process
- **Network Dependent** - Requires stable internet connection

## 📄 **License**

This project is licensed under the MIT License.

