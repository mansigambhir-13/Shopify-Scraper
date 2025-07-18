"""
Shopify Store Insights Fetcher Application
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback
from contextlib import asynccontextmanager

from app.models.responses import BrandInsightsResponse, ErrorResponse
from app.models.requests import ShopifyStoreRequest
from app.services.shopify_scraper import ShopifyScraperService
from app.database.database import init_db, get_db
from app.utils.validators import validate_shopify_url
from app.utils.logger import setup_logger

# Setup logging
setup_logger()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    yield

# Initialize FastAPI app
app = FastAPI(
    title="Shopify Store Insights Fetcher",
    description="Extract comprehensive insights from Shopify stores without using official APIs",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Shopify Store Insights Fetcher API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Shopify Store Insights Fetcher",
        "version": "1.0.0"
    }

@app.post("/api/v1/extract-insights", response_model=BrandInsightsResponse)
async def extract_shopify_insights(
    request: ShopifyStoreRequest,
    background_tasks: BackgroundTasks,
    db=Depends(get_db)
):
    """
    Extract comprehensive insights from a Shopify store
    
    Args:
        request: ShopifyStoreRequest containing the website URL
        background_tasks: FastAPI background tasks
        db: Database session
    
    Returns:
        BrandInsightsResponse: Structured brand insights
    
    Raises:
        HTTPException: 401 if website not found, 500 for internal errors
    """
    try:
        # Validate URL
        if not validate_shopify_url(request.website_url):
            raise HTTPException(
                status_code=400,
                detail="Invalid Shopify store URL provided"
            )
        
        # Initialize scraper service
        scraper_service = ShopifyScraperService(db)
        
        # Extract insights
        logger.info(f"Starting insights extraction for: {request.website_url}")
        insights = await scraper_service.extract_comprehensive_insights(
            request.website_url
        )
        
        # Save to database in background
        background_tasks.add_task(
            scraper_service.save_insights_to_db,
            insights,
            request.website_url
        )
        
        logger.info(f"Successfully extracted insights for: {request.website_url}")
        return BrandInsightsResponse(
            success=True,
            message="Insights extracted successfully",
            data=insights
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting insights: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Check if it's a website not found error
        if "not accessible" in str(e).lower():
            raise HTTPException(
                status_code=401,
                detail="Website not found or not accessible"
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=exc.detail,
            status_code=exc.status_code
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal server error occurred",
            status_code=500
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )