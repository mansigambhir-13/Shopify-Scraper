# 🛍️ Shopify Store Insights Fetcher

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive Python application that extracts detailed insights from Shopify stores without using official APIs. Built with FastAPI, this application provides robust scraping capabilities, AI-powered analysis, and structured data storage.

## 🎯 **Features**

### **Mandatory Features ✅**
- **📦 Product Catalog** - Complete product extraction from `/products.json`
- **⭐ Hero Products** - Featured products from homepage
- **🔒 Privacy Policy** - Automated policy content extraction
- **↩️ Return/Refund Policies** - Return policy discovery and extraction
- **❓ Brand FAQs** - Structured FAQ extraction with AI enhancement
- **📱 Social Media Handles** - Instagram, Facebook, TikTok, Twitter discovery
- **📞 Contact Information** - Email and phone number extraction
- **🏢 Brand Context** - Brand story, description, and company information
- **🔗 Important Links** - Order tracking, blogs, support, and key pages

### **Bonus Features 🚀**
- **🤖 AI-Powered Analysis** - OpenAI integration for enhanced data structuring
- **🗄️ Database Persistence** - SQLite/MySQL with proper relationships
- **📊 RESTful API** - Clean, documented endpoints with OpenAPI/Swagger
- **🔄 Background Processing** - Non-blocking database operations
- **📝 Comprehensive Logging** - Structured logging with rotation
- **🐳 Docker Support** - Easy deployment and development setup
- **✅ Input Validation** - Robust data validation with Pydantic
- **🚀 Health Monitoring** - Health check and monitoring endpoints

## 🏗️ **Architecture**

```
shopify-insights-fetcher/
├── app/
│   ├── __init__.py                 # Application package
│   ├── models/                     # Data models
│   │   ├── __init__.py
│   │   ├── requests.py            # Request validation models
│   │   └── responses.py           # Response models
│   ├── database/                   # Database layer
│   │   ├── __init__.py
│   │   ├── database.py            # SQLAlchemy configuration
│   │   └── models.py              # Database models
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   └── shopify_scraper.py     # Core scraping service
│   └── utils/                      # Utilities
│       ├── __init__.py
│       ├── data_processor.py      # Data cleaning utilities
│       ├── validators.py          # Validation functions
│       └── logger.py              # Logging configuration
├── tests/                          # Test suite
├── logs/                          # Application logs
├── main.py                        # FastAPI application
├── requirements.txt               # Python dependencies
├── .env                          # Environment configuration
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8 or higher
- Git
- Optional: Docker for database setup

### **1. Clone Repository**
```bash
git clone <repository-url>
cd shopify-insights-fetcher
```

### **2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux  
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Setup**

**Option A: Automated Setup (Recommended)**
```bash
python setup_env.py
```

**Option B: Manual Setup**
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your settings
# DATABASE_URL=sqlite:///./shopify_insights.db
```

### **5. Validate Configuration**
```bash
python validate_env.py
```

### **6. Test Database**
```bash
python test_simple_sqlite.py
```

### **7. Start Application**
```bash
python main.py
```

### **8. Access Application**
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📖 **API Usage**

### **Extract Store Insights**

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/extract-insights" \
     -H "Content-Type: application/json" \
     -d '{
       "website_url": "https://gymshark.com"
     }'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/extract-insights",
    json={"website_url": "https://gymshark.com"}
)
print(response.json())
```

### **Response Example**
```json
{
  "success": true,
  "message": "Insights extracted successfully",
  "data": {
    "brand_name": "Gymshark",
    "domain": "gymshark.com",
    "total_products": 150,
    "product_catalog": [
      {
        "title": "Vital Seamless Leggings",
        "price": "50.00",
        "vendor": "Gymshark",
        "product_url": "https://gymshark.com/products/vital-seamless-leggings"
      }
    ],
    "privacy_policy": {
      "title": "Privacy Policy",
      "content": "Gymshark values your privacy...",
      "url": "https://gymshark.com/pages/privacy-policy"
    },
    "faqs": [
      {
        "question": "What is your return policy?",
        "answer": "We offer 30-day returns..."
      }
    ],
    "social_handles": [
      {
        "platform": "instagram", 
        "url": "https://instagram.com/gymshark",
        "username": "gymshark"
      }
    ],
    "extraction_success": true
  }
}
```

## 🗄️ **Database**

### **SQLite (Default)**
- **File-based**: `shopify_insights.db`
- **Zero setup**: Works out of the box
- **Perfect for**: Development, testing, demos

### **MySQL (Optional)**
```bash
# Update .env file
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/shopify_insights

# Or use Docker
docker-compose up -d mysql
```

### **View Data**

**SQLite Browser:**
```bash
pip install sqlite-web
sqlite_web shopify_insights.db
# Visit: http://localhost:8080
```

**Command Line:**
```bash
sqlite3 shopify_insights.db
.tables
SELECT * FROM brand_insights;
```

## 🧪 **Testing**

### **Run Tests**
```bash
# All tests
python -m pytest

# Specific test file
python -m pytest tests/test_basic.py -v

# With coverage
python -m pytest --cov=app tests/
```

### **Manual Testing**
```bash
# Health check
curl http://localhost:8000/health

# Test with known Shopify stores
curl -X POST "http://localhost:8000/api/v1/extract-insights" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://allbirds.com"}'
```

## 🎯 **Use Cases**

### **E-commerce Research**
- Analyze competitor product catalogs
- Compare pricing strategies  
- Study customer service approaches
- Monitor policy changes

### **Market Analysis**
- Identify market gaps and opportunities
- Analyze payment method adoption
- Study social media strategies
- Track industry trends

### **Business Intelligence**
- Competitive benchmarking
- Customer FAQ pattern analysis
- Brand positioning research
- Market entry research

## ⚙️ **Configuration**

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./shopify_insights.db` |
| `OPENAI_API_KEY` | OpenAI API key for AI features | `your_openai_api_key_here` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `API_PORT` | API server port | `8000` |
| `REQUEST_TIMEOUT` | HTTP request timeout | `30` |
| `MAX_PRODUCTS_PER_STORE` | Product extraction limit | `1000` |
| `ENABLE_AI_ENHANCEMENT` | Enable AI features | `false` |

### **Feature Flags**
```bash
# Enable/disable features in .env
ENABLE_COMPETITOR_ANALYSIS=true
ENABLE_AI_ENHANCEMENT=false
ENABLE_CACHING=false
```

## 🚀 **Deployment**

### **Docker Deployment**
```bash
# Build and run
docker build -t shopify-insights .
docker run -p 8000:8000 shopify-insights

# Or use docker-compose
docker-compose up --build
```

### **Production Deployment**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or with systemd service
sudo systemctl start shopify-insights
```

## 🔧 **Development**

### **Project Setup**
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run linting
flake8 app/
black app/
```

### **Adding New Features**
1. **Create models** in `app/models/`
2. **Add business logic** in `app/services/`
3. **Update database models** if needed
4. **Add API endpoints** in `main.py`
5. **Write tests** in `tests/`

### **Code Quality**
- **Type hints** throughout codebase
- **Comprehensive error handling**
- **Structured logging**
- **Clean architecture** principles
- **SOLID design** patterns

## 📊 **Performance**

### **Optimization Features**
- **Background processing** for database operations
- **Connection pooling** for database efficiency
- **Request rate limiting** to prevent overload
- **Efficient batch operations** for bulk data
- **Asynchronous processing** where applicable

### **Monitoring**
- **Health check endpoints** for uptime monitoring
- **Structured logging** for debugging
- **Request/response metrics** 
- **Error tracking** and reporting

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Development Guidelines**
- Follow **PEP 8** style guidelines
- Add **type hints** for all functions
- Include **docstrings** for public methods
- Write **tests** for new features
- Update **documentation** as needed

## 🐛 **Troubleshooting**

### **Common Issues**

**Database Connection Error**
```bash
# Check if database file exists
ls -la shopify_insights.db

# Test connection
python test_simple_sqlite.py
```

**Import Errors**
```bash
# Ensure you're in the right directory
pwd

# Reinstall dependencies
pip install -r requirements.txt
```

**Port Already in Use**
```bash
# Change port in .env
API_PORT=8001

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

**Website Not Accessible**
```bash
# Try with different Shopify stores
curl -X POST "http://localhost:8000/api/v1/extract-insights" \
     -d '{"website_url": "https://allbirds.com"}'
```

### **Debug Mode**
```bash
# Enable debug logging
LOG_LEVEL=DEBUG

# Enable SQL debugging  
SQL_DEBUG=true
```

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **FastAPI** for the excellent web framework
- **Beautiful Soup** for HTML parsing capabilities
- **SQLAlchemy** for robust database operations  
- **OpenAI** for AI-powered enhancements
- **Pydantic** for data validation
- **Shopify** ecosystem for inspiration

## 📞 **Support**

- **Documentation**: Check this README and API docs
- **Issues**: Open a GitHub issue for bugs
- **Questions**: Use GitHub discussions for questions
- **Email**: [Contact team for urgent issues]

---

**Happy Scraping! 🕷️✨**

*Built with ❤️ for e-commerce intelligence and competitive analysis*