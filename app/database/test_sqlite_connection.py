#!/usr/bin/env python3
"""
SQLite Connection Test for Shopify Insights Fetcher
"""

import sqlite3
import os
from pathlib import Path

def test_sqlite_connection():
    """Test SQLite database connection and setup."""
    
    # Database file path
    db_path = "shopify_insights.db"
    
    print("🔍 Testing SQLite Connection")
    print(f"📁 Database file: {os.path.abspath(db_path)}")
    
    try:
        # Connect to SQLite database (creates file if doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        
        print(f"✅ SQLite connection successful!")
        print(f"📊 SQLite version: {version}")
        
        # Create a test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("Test Connection",))
        conn.commit()
        
        # Read test data
        cursor.execute("SELECT * FROM test_table")
        rows = cursor.fetchall()
        
        print(f"🎯 Test table created with {len(rows)} rows")
        
        # Clean up test table
        cursor.execute("DROP TABLE test_table")
        conn.commit()
        
        print("🧹 Test table cleaned up")
        
        conn.close()
        print("✅ SQLite test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False

def update_env_file():
    """Update .env file to use SQLite."""
    
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print("📝 Creating .env file...")
        with open(env_path, 'w') as f:
            f.write("# Shopify Insights Fetcher Configuration\n")
            f.write("DATABASE_URL=sqlite:///./shopify_insights.db\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("API_PORT=8000\n")
            f.write("REQUEST_TIMEOUT=30\n")
            f.write("MAX_PRODUCTS_PER_STORE=1000\n")
            f.write("ENABLE_AI_ENHANCEMENT=false\n")
        print("✅ .env file created with SQLite configuration")
    else:
        # Read existing .env file
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update DATABASE_URL line
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("DATABASE_URL="):
                lines[i] = "DATABASE_URL=sqlite:///./shopify_insights.db\n"
                updated = True
                break
        
        # Add DATABASE_URL if not found
        if not updated:
            lines.append("DATABASE_URL=sqlite:///./shopify_insights.db\n")
        
        # Write back to file
        with open(env_path, 'w') as f:
            f.writelines(lines)
        
        print("✅ .env file updated to use SQLite")

if __name__ == "__main__":
    print("🚀 Shopify Insights Fetcher - SQLite Setup\n")
    
    # Update .env file
    update_env_file()
    
    print()
    
    # Test connection
    success = test_sqlite_connection()
    
    print()
    
    if success:
        print("🎉 SQLite setup complete!")
        print("💡 You can now run: python main.py")
        print("📖 API docs will be at: http://localhost:8000/docs")
    else:
        print("❌ SQLite setup failed. Please check the error messages above.")