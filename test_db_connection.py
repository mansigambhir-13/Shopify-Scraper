#!/usr/bin/env python3
"""
Fixed Database Connection Test for Shopify Insights Fetcher
Handles both SQLite and MySQL properly
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file."""
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def get_database_url():
    """Get database URL from environment."""
    load_env_file()
    return os.getenv('DATABASE_URL', 'sqlite:///./shopify_insights.db')

def test_database_connection():
    """Test database connection with proper handling for SQLite and MySQL."""
    
    database_url = get_database_url()
    print(f"🔍 Testing connection to: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test basic connection
        with engine.connect() as connection:
            # Test query that works on both SQLite and MySQL
            result = connection.execute(text("SELECT 1 as test_value"))
            test_result = result.fetchone()
            print(f"✅ Database connection successful!")
            print(f"Test query result: {test_result}")
            
            # Database-specific information
            if database_url.startswith('sqlite'):
                print("📊 Database Type: SQLite")
                
                # Get SQLite version
                version_result = connection.execute(text("SELECT sqlite_version()"))
                version = version_result.fetchone()[0]
                print(f"📈 SQLite Version: {version}")
                
                # Get database file path
                db_path = database_url.replace('sqlite:///', '')
                if db_path.startswith('./'):
                    db_path = os.path.abspath(db_path)
                print(f"📁 Database File: {db_path}")
                
                # Check if database file exists and get size
                if os.path.exists(db_path):
                    file_size = os.path.getsize(db_path)
                    print(f"💾 File Size: {file_size} bytes")
                else:
                    print("📝 Database file will be created on first use")
                    
            elif 'mysql' in database_url:
                print("📊 Database Type: MySQL")
                
                # Get MySQL version
                version_result = connection.execute(text("SELECT VERSION()"))
                version = version_result.fetchone()[0]
                print(f"📈 MySQL Version: {version}")
                
                # Get current database name
                db_result = connection.execute(text("SELECT DATABASE()"))
                current_db = db_result.fetchone()[0]
                print(f"🗄️ Current Database: {current_db}")
                
            else:
                print("📊 Database Type: Unknown")
            
            # Test creating a simple table
            print("\n🧪 Testing table operations...")
            
            # Create test table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS connection_test (
                    id INTEGER PRIMARY KEY,
                    test_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Insert test data
            connection.execute(text("""
                INSERT INTO connection_test (test_name) 
                VALUES ('Database Connection Test')
            """))
            
            # Read test data
            result = connection.execute(text("SELECT COUNT(*) FROM connection_test"))
            count = result.fetchone()[0]
            print(f"✅ Test table created and populated (rows: {count})")
            
            # Clean up test table
            connection.execute(text("DROP TABLE connection_test"))
            connection.commit()
            print("🧹 Test table cleaned up")
            
        print(f"\n🎉 Database connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        
        # Provide specific troubleshooting based on error type
        error_str = str(e).lower()
        
        if "no such function: database" in error_str:
            print("\n🔧 Issue: MySQL function used on SQLite database")
            print("✅ This has been fixed in this script!")
            
        elif "can't connect to mysql server" in error_str:
            print("\n🔧 MySQL Server Issues:")
            print("1. Make sure MySQL server is running")
            print("2. Check if the database exists")
            print("3. Verify credentials in .env file")
            print("4. Try switching to SQLite for development:")
            print("   DATABASE_URL=sqlite:///./shopify_insights.db")
            
        elif "access denied" in error_str:
            print("\n🔧 Authentication Issues:")
            print("1. Check MySQL username and password")
            print("2. Verify user has permission to access database")
            print("3. Check .env file credentials")
            
        elif "unknown database" in error_str:
            print("\n🔧 Database doesn't exist:")
            print("1. Connect to MySQL and create database:")
            print("   CREATE DATABASE shopify_insights;")
            print("2. Or use an existing database name")
            
        else:
            print("\n🔧 General troubleshooting:")
            print("1. Check your .env file configuration")
            print("2. Verify database server is running")
            print("3. Test with SQLite: DATABASE_URL=sqlite:///./shopify_insights.db")
            
        return False

def main():
    """Main function."""
    print("🚀 Shopify Insights Fetcher - Database Connection Test")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Creating one with SQLite configuration...")
        with open('.env', 'w') as f:
            f.write("# Shopify Insights Fetcher Configuration\n")
            f.write("DATABASE_URL=sqlite:///./shopify_insights.db\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("API_PORT=8000\n")
            f.write("REQUEST_TIMEOUT=30\n")
            f.write("MAX_PRODUCTS_PER_STORE=1000\n")
            f.write("ENABLE_AI_ENHANCEMENT=false\n")
        print("✅ .env file created with SQLite configuration")
    
    # Test database connection
    success = test_database_connection()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Run your application: python main.py")
        print("2. Visit API docs: http://localhost:8000/docs")
        print("3. Test health check: http://localhost:8000/health")
        print("4. Try extracting insights from a Shopify store!")
    else:
        print("\n❌ Please fix the database connection issues above")
        print("💡 Tip: SQLite is recommended for development (zero setup required)")

if __name__ == "__main__":
    main()