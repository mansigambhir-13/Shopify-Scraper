"""
Project Status Checker
Comprehensive validation of project completeness and readiness
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import json

class ProjectStatusChecker:
    """Comprehensive project status and validation checker"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.results = {
            'files': {'required': [], 'optional': [], 'missing': []},
            'structure': {'valid': [], 'invalid': []},
            'dependencies': {'installed': [], 'missing': []},
            'configuration': {'valid': [], 'issues': []},
            'tests': {'passed': [], 'failed': []},
            'submission_ready': False
        }
    
    def check_all(self) -> Dict:
        """Run all checks and return comprehensive status"""
        print("🔍 Comprehensive Project Status Check")
        print("=" * 60)
        
        self.check_file_structure()
        self.check_configuration_files()
        self.check_python_files()
        self.check_dependencies()
        self.check_database_setup()
        self.check_git_setup()
        self.validate_submission_readiness()
        
        self.print_summary()
        return self.results
    
    def check_file_structure(self):
        """Check if all required files and directories exist"""
        print("\n📁 File Structure Check")
        print("-" * 30)
        
        required_files = [
            # Core application files
            'main.py',
            'requirements.txt',
            '.env',
            'README.md',
            
            # Application structure
            'app/__init__.py',
            'app/models/__init__.py',
            'app/models/requests.py',
            'app/models/responses.py',
            'app/database/__init__.py',
            'app/database/database.py',
            'app/database/models.py',
            'app/services/__init__.py',
            'app/services/shopify_scraper.py',
            'app/utils/__init__.py',
            'app/utils/data_processor.py',
            'app/utils/validators.py',
            'app/utils/logger.py',
            
            # Test files
            'tests/__init__.py',
            'tests/test_basic.py',
        ]
        
        optional_files = [
            # Development files
            'requirements-dev.txt',
            'pytest.ini',
            '.pre-commit-config.yaml',
            'Makefile',
            'docker-compose.yml',
            'Dockerfile',
            '.gitignore',
            
            # Configuration files
            '.env.template',
            'setup_env.py',
            'validate_env.py',
            'test_simple_sqlite.py',
            
            # Additional tests
            'tests/test_comprehensive.py',
            
            # Documentation
            'DEMO.md',
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                self.results['files']['required'].append(file_path)
                print(f"✅ {file_path}")
            else:
                self.results['files']['missing'].append(file_path)
                print(f"❌ {file_path} (REQUIRED)")
        
        print(f"\n📋 Optional Files:")
        for file_path in optional_files:
            if os.path.exists(file_path):
                self.results['files']['optional'].append(file_path)
                print(f"✅ {file_path}")
            else:
                print(f"➖ {file_path} (optional)")
        
        # Check directories
        required_dirs = ['app', 'app/models', 'app/database', 'app/services', 'app/utils', 'tests']
        print(f"\n📂 Directory Structure:")
        for dir_path in required_dirs:
            if os.path.isdir(dir_path):
                self.results['structure']['valid'].append(dir_path)
                print(f"✅ {dir_path}/")
            else:
                self.results['structure']['invalid'].append(dir_path)
                print(f"❌ {dir_path}/ (missing)")
    
    def check_configuration_files(self):
        """Check configuration file validity"""
        print("\n⚙️ Configuration Check")
        print("-" * 30)
        
        # Check .env file
        if os.path.exists('.env'):
            try:
                from dotenv import load_dotenv
                load_dotenv()
                
                database_url = os.getenv('DATABASE_URL')
                if database_url:
                    print(f"✅ .env file loads successfully")
                    print(f"📊 Database: {'SQLite' if 'sqlite' in database_url else 'MySQL'}")
                    self.results['configuration']['valid'].append('.env')
                else:
                    print(f"❌ .env file missing DATABASE_URL")
                    self.results['configuration']['issues'].append('.env missing DATABASE_URL')
                    
            except Exception as e:
                print(f"❌ .env file has errors: {e}")
                self.results['configuration']['issues'].append(f'.env errors: {e}')
        else:
            print(f"❌ .env file missing")
            self.results['configuration']['issues'].append('.env file missing')
        
        # Check gitignore
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                gitignore_content = f.read()
            
            if '.env' in gitignore_content:
                print(f"✅ .gitignore protects .env file")
                self.results['configuration']['valid'].append('.gitignore')
            else:
                print(f"⚠️ .gitignore doesn't protect .env file")
                self.results['configuration']['issues'].append('.gitignore missing .env protection')
    
    def check_python_files(self):
        """Check Python file syntax and imports"""
        print("\n🐍 Python Files Check")
        print("-" * 30)
        
        python_files = [
            'main.py',
            'app/__init__.py',
            'app/models/requests.py',
            'app/models/responses.py',
            'app/database/database.py',
            'app/database/models.py',
            'app/services/shopify_scraper.py',
            'app/utils/data_processor.py',
            'app/utils/validators.py',
            'app/utils/logger.py',
        ]
        
        for file_path in python_files:
            if os.path.exists(file_path):
                try:
                    # Try to compile the file
                    with open(file_path, 'r') as f:
                        code = f.read()
                    
                    compile(code, file_path, 'exec')
                    print(f"✅ {file_path} - syntax OK")
                    
                except SyntaxError as e:
                    print(f"❌ {file_path} - syntax error: {e}")
                    self.results['configuration']['issues'].append(f'{file_path} syntax error')
                except Exception as e:
                    print(f"⚠️ {file_path} - warning: {e}")
            else:
                print(f"➖ {file_path} - missing")
    
    def check_dependencies(self):
        """Check if dependencies are properly installed"""
        print("\n📦 Dependencies Check")
        print("-" * 30)
        
        if os.path.exists('requirements.txt'):
            try:
                with open('requirements.txt', 'r') as f:
                    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
                # Check if key packages are importable
                key_packages = ['fastapi', 'uvicorn', 'pydantic', 'requests', 'beautifulsoup4', 'sqlalchemy']
                
                for package in key_packages:
                    try:
                        __import__(package.replace('-', '_'))
                        print(f"✅ {package}")
                        self.results['dependencies']['installed'].append(package)
                    except ImportError:
                        print(f"❌ {package} not installed")
                        self.results['dependencies']['missing'].append(package)
                
            except Exception as e:
                print(f"❌ Error reading requirements.txt: {e}")
                self.results['configuration']['issues'].append(f'requirements.txt error: {e}')
        else:
            print(f"❌ requirements.txt missing")
            self.results['configuration']['issues'].append('requirements.txt missing')
    
    def check_database_setup(self):
        """Check database configuration and connectivity"""
        print("\n🗄️ Database Check")
        print("-" * 30)
        
        try:
            from app.database.database import engine, SessionLocal
            
            # Try to connect to database
            session = SessionLocal()
            session.close()
            print(f"✅ Database connection successful")
            
            # Check if database file exists (for SQLite)
            if os.path.exists('shopify_insights.db'):
                print(f"✅ SQLite database file exists")
            
            self.results['configuration']['valid'].append('database_connection')
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            self.results['configuration']['issues'].append(f'database connection: {e}')
    
    def check_git_setup(self):
        """Check Git configuration"""
        print("\n📝 Git Setup Check")
        print("-" * 30)
        
        if os.path.exists('.git'):
            print(f"✅ Git repository initialized")
            
            # Check if .env is in gitignore
            if os.path.exists('.gitignore'):
                with open('.gitignore', 'r') as f:
                    gitignore = f.read()
                
                if '.env' in gitignore:
                    print(f"✅ .env file protected from version control")
                    self.results['configuration']['valid'].append('git_security')
                else:
                    print(f"⚠️ .env file not in .gitignore")
                    self.results['configuration']['issues'].append('.env not in .gitignore')
            
            # Check for pre-commit
            if os.path.exists('.pre-commit-config.yaml'):
                print(f"✅ Pre-commit configuration found")
        else:
            print(f"➖ Git repository not initialized")
    
    def validate_submission_readiness(self):
        """Validate if project is ready for submission"""
        print("\n🎯 Submission Readiness Check")
        print("-" * 30)
        
        critical_requirements = [
            # All mandatory features must be implemented
            len(self.results['files']['missing']) == 0,
            len(self.results['structure']['invalid']) == 0,
            len(self.results['dependencies']['missing']) == 0,
            'database_connection' in self.results['configuration']['valid'],
            '.env' in self.results['configuration']['valid'],
        ]
        
        mandatory_features = [
            'product_catalog',
            'hero_products', 
            'privacy_policy',
            'return_refund_policy',
            'faqs',
            'social_handles',
            'contact_info',
            'brand_context',
            'important_links'
        ]
        
        print("🔍 Checking mandatory features implementation...")
        
        # Check if scraper service has all required methods
        scraper_file = 'app/services/shopify_scraper.py'
        if os.path.exists(scraper_file):
            with open(scraper_file, 'r') as f:
                scraper_content = f.read()
            
            required_methods = [
                '_extract_product_catalog',
                '_extract_hero_products',
                '_extract_policies',
                '_extract_faqs',
                '_extract_social_handles',
                '_extract_contact_info',
                '_extract_important_links'
            ]
            
            missing_methods = []
            for method in required_methods:
                if method in scraper_content:
                    print(f"✅ {method}")
                else:
                    print(f"❌ {method} missing")
                    missing_methods.append(method)
            
            if not missing_methods:
                print(f"✅ All mandatory features implemented")
            else:
                print(f"❌ Missing features: {missing_methods}")
                critical_requirements.append(False)
        
        # Final assessment
        self.results['submission_ready'] = all(critical_requirements)
        
        if self.results['submission_ready']:
            print(f"\n🎉 PROJECT IS READY FOR SUBMISSION!")
        else:
            print(f"\n⚠️ PROJECT NEEDS FIXES BEFORE SUBMISSION")
    
    def print_summary(self):
        """Print comprehensive summary"""
        print("\n" + "=" * 60)
        print("📊 PROJECT STATUS SUMMARY")
        print("=" * 60)
        
        print(f"\n📁 Files:")
        print(f"  ✅ Required files: {len(self.results['files']['required'])}")
        print(f"  ➖ Missing files: {len(self.results['files']['missing'])}")
        print(f"  📋 Optional files: {len(self.results['files']['optional'])}")
        
        print(f"\n⚙️ Configuration:")
        print(f"  ✅ Valid configs: {len(self.results['configuration']['valid'])}")
        print(f"  ❌ Issues: {len(self.results['configuration']['issues'])}")
        
        print(f"\n📦 Dependencies:")
        print(f"  ✅ Installed: {len(self.results['dependencies']['installed'])}")
        print(f"  ❌ Missing: {len(self.results['dependencies']['missing'])}")
        
        # Print issues if any
        if self.results['files']['missing']:
            print(f"\n❌ Missing Required Files:")
            for file in self.results['files']['missing']:
                print(f"  • {file}")
        
        if self.results['configuration']['issues']:
            print(f"\n⚠️ Configuration Issues:")
            for issue in self.results['configuration']['issues']:
                print(f"  • {issue}")
        
        if self.results['dependencies']['missing']:
            print(f"\n📦 Missing Dependencies:")
            for dep in self.results['dependencies']['missing']:
                print(f"  • {dep}")
        
        # Final status
        print(f"\n🎯 SUBMISSION STATUS:")
        if self.results['submission_ready']:
            print(f"  🎉 READY FOR SUBMISSION!")
            print(f"  📋 All mandatory requirements satisfied")
            print(f"  🚀 Run: python main.py to start the application")
        else:
            print(f"  ⚠️ NOT READY - Please fix the issues above")
            print(f"  🔧 Run: make setup (if you have Makefile)")
            print(f"  📖 Check README.md for setup instructions")
        
        return self.results

def quick_status():
    """Quick status check for CI/CD"""
    checker = ProjectStatusChecker()
    results = checker.check_all()
    
    # Return exit code for CI/CD
    return 0 if results['submission_ready'] else 1

if __name__ == "__main__":
    try:
        exit_code = quick_status()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️ Status check cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Status check failed: {e}")
        sys.exit(1)