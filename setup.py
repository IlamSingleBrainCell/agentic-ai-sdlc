# setup.py
"""
Comprehensive setup script for AI SDLC Wizard - Professional Edition
Handles installation, configuration, and environment setup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
import platform
from datetime import datetime
from typing import List, Dict, Any

class Colors:
    """Terminal colors for better output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SetupManager:
    """Main setup manager for the AI SDLC Wizard"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.requirements_met = True
        self.setup_log = []
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "architecture": platform.architecture()[0],
            "processor": platform.processor() or "Unknown"
        }
    
    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}  {text}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")
        self.setup_log.append(f"SUCCESS: {text}")
    
    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")
        self.setup_log.append(f"WARNING: {text}")
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")
        self.setup_log.append(f"ERROR: {text}")
        self.requirements_met = False
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")
        self.setup_log.append(f"INFO: {text}")
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        self.print_info("Checking Python version...")
        
        version = sys.version_info
        min_version = (3, 8)
        
        if version[:2] >= min_version:
            self.print_success(f"Python {version.major}.{version.minor}.{version.micro} is supported")
            return True
        else:
            self.print_error(f"Python {version.major}.{version.minor} is not supported. Please use Python {min_version[0]}.{min_version[1]}+")
            return False
    
    def check_system_requirements(self) -> bool:
        """Check system requirements"""
        self.print_info("Checking system requirements...")
        
        # Check available memory (recommended 4GB+)
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb >= 4:
                self.print_success(f"System memory: {memory_gb:.1f}GB (sufficient)")
            else:
                self.print_warning(f"System memory: {memory_gb:.1f}GB (4GB+ recommended)")
        except ImportError:
            self.print_info("Cannot check memory (psutil not installed)")
        
        # Check disk space (recommended 2GB+)
        try:
            disk_usage = shutil.disk_usage(".")
            free_gb = disk_usage.free / (1024**3)
            if free_gb >= 2:
                self.print_success(f"Available disk space: {free_gb:.1f}GB (sufficient)")
            else:
                self.print_warning(f"Available disk space: {free_gb:.1f}GB (2GB+ recommended)")
        except Exception:
            self.print_info("Cannot check disk space")
        
        return True
    
    def create_directories(self) -> bool:
        """Create necessary directories"""
        self.print_info("Creating project directories...")
        
        directories = [
            "artifacts",
            "generated_code",
            "test_cases", 
            "exports",
            "auto_saves",
            "logs",
            "backups",
            "temp"
        ]
        
        try:
            for directory in directories:
                Path(directory).mkdir(exist_ok=True)
                self.print_success(f"Created {directory}/")
            return True
        except Exception as e:
            self.print_error(f"Failed to create directories: {e}")
            return False
    
    def check_env_file(self) -> bool:
        """Check and create environment file"""
        self.print_info("Checking environment configuration...")
        
        env_file = Path(".env")
        env_example = Path(".env.example")
        
        # Create .env.example if it doesn't exist
        if not env_example.exists():
            env_example_content = """# AI SDLC Wizard Configuration
# Copy this file to .env and update the values

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Application Settings
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# Feature Flags
ENABLE_AUTO_SAVE=True
ENABLE_ANALYTICS=True
ENABLE_ERROR_RECOVERY=True

# Performance Settings
MAX_CONCURRENT_REQUESTS=5
CACHE_TTL=3600

# Security Settings
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT=3600

# Optional: Database Configuration
# DATABASE_URL=sqlite:///sdlc_wizard.db

# Optional: Cloud Storage (for enterprise features)
# AWS_ACCESS_KEY_ID=your_aws_key
# AWS_SECRET_ACCESS_KEY=your_aws_secret
# AWS_BUCKET_NAME=your_bucket_name
"""
            with open(env_example, 'w') as f:
                f.write(env_example_content)
            self.print_success("Created .env.example template")
        
        # Check .env file
        if env_file.exists():
            self.print_success(".env file found")
            
            # Check for required keys
            with open(env_file, 'r') as f:
                content = f.read()
                
            required_keys = ["GROQ_API_KEY"]
            missing_keys = []
            
            for key in required_keys:
                if key not in content or f"{key}=your_" in content:
                    missing_keys.append(key)
            
            if missing_keys:
                self.print_warning(f"Missing or incomplete environment variables: {', '.join(missing_keys)}")
                return False
            else:
                self.print_success("Environment variables are configured")
                return True
        else:
            # Copy from example
            if env_example.exists():
                shutil.copy(env_example, env_file)
                self.print_warning("Created .env from template. Please update GROQ_API_KEY and other values")
            else:
                self.print_error(".env file not found and cannot create from template")
            return False
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies"""
        self.print_info("Installing Python dependencies...")
        
        try:
            # Upgrade pip first
            self.print_info("Upgrading pip...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], stdout=subprocess.DEVNULL)
            
            # Install from requirements.txt
            if Path("requirements.txt").exists():
                self.print_info("Installing from requirements.txt...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.print_success("Dependencies installed successfully")
                    return True
                else:
                    self.print_error(f"Failed to install dependencies: {result.stderr}")
                    return False
            else:
                # Install core dependencies manually
                core_deps = [
                    "streamlit>=1.45.0",
                    "plotly>=5.22.0",
                    "pandas>=2.2.0",
                    "python-dotenv>=1.0.0",
                    "langchain>=0.3.0",
                    "langchain-groq>=0.2.0",
                    "langgraph>=0.3.0"
                ]
                
                for dep in core_deps:
                    self.print_info(f"Installing {dep}...")
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", dep
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.print_success(f"Installed {dep}")
                    else:
                        self.print_error(f"Failed to install {dep}: {result.stderr}")
                        return False
                
                return True
                
        except Exception as e:
            self.print_error(f"Exception during installation: {e}")
            return False
    
    def verify_imports(self) -> bool:
        """Verify that all critical imports work"""
        self.print_info("Verifying critical imports...")
        
        critical_imports = [
            ("streamlit", "Streamlit framework"),
            ("plotly", "Plotly visualization"),
            ("pandas", "Pandas data processing"),
            ("langchain", "LangChain framework"),
            ("langgraph", "LangGraph workflow"),
            ("dotenv", "Environment variables"),
        ]
        
        optional_imports = [
            ("docx", "Document generation"),
            ("reportlab", "PDF generation"),
            ("openpyxl", "Excel processing"),
            ("psutil", "System monitoring"),
        ]
        
        success = True
        
        # Check critical imports
        for module, description in critical_imports:
            try:
                __import__(module)
                self.print_success(f"{description} available")
            except ImportError as e:
                self.print_error(f"{description} not available: {e}")
                success = False
        
        # Check optional imports
        for module, description in optional_imports:
            try:
                __import__(module)
                self.print_success(f"{description} available (optional)")
            except ImportError:
                self.print_warning(f"{description} not available (optional)")
        
        return success
    
    def create_config_files(self) -> bool:
        """Create default configuration files"""
        self.print_info("Creating configuration files...")
        
        try:
            # Create basic config if it doesn't exist
            if not Path("config.py").exists():
                config_content = '''# config.py
"""Basic configuration for AI SDLC Wizard"""

import os

class Config:
    APP_NAME = "AI SDLC Wizard"
    APP_VERSION = "3.0.0"
    DEFAULT_LLM_MODEL = "gemma2-9b-it"
    
    SUPPORTED_LANGUAGES = {
        "python": {"name": "Python", "extensions": [".py"]},
        "javascript": {"name": "JavaScript", "extensions": [".js"]},
        "java": {"name": "Java", "extensions": [".java"]},
    }
    
    AUTONOMY_LEVELS = {
        "manual": {"name": "Manual", "icon": "👨‍💻"},
        "semi_auto": {"name": "Semi-Autonomous", "icon": "🤖"},
        "full_auto": {"name": "Fully Autonomous", "icon": "🚀"},
    }
'''
                with open("config.py", 'w') as f:
                    f.write(config_content)
                self.print_success("Created basic config.py")
            
            # Create launch script
            self._create_launch_script()
            
            return True
            
        except Exception as e:
            self.print_error(f"Failed to create config files: {e}")
            return False
    
    def _create_launch_script(self):
        """Create platform-specific launch scripts"""
        # Windows batch script
        windows_script = """@echo off
echo Starting AI SDLC Wizard...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist venv\\Scripts\\activate.bat (
    echo Activating virtual environment...
    call venv\\Scripts\\activate.bat
)

REM Start the application
echo Starting Streamlit application...
streamlit run streamlit_app.py --server.port 8501 --server.address localhost

pause
"""
        
        # Unix shell script
        unix_script = """#!/bin/bash
echo "Starting AI SDLC Wizard..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Start the application
echo "Starting Streamlit application..."
echo "Open your browser to: http://localhost:8501"
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
"""
        
        # Create scripts
        with open("start_wizard.bat", 'w') as f:
            f.write(windows_script)
        
        with open("start_wizard.sh", 'w') as f:
            f.write(unix_script)
        
        # Make Unix script executable
        if os.name != 'nt':
            os.chmod("start_wizard.sh", 0o755)
        
        self.print_success("Created launch scripts (start_wizard.bat / start_wizard.sh)")
    
    def check_optional_tools(self) -> Dict[str, bool]:
        """Check for optional development tools"""
        self.print_info("Checking optional development tools...")
        
        tools = {
            "git": "Git version control",
            "node": "Node.js (for JavaScript projects)",
            "java": "Java runtime (for Java projects)",
            "go": "Go compiler (for Go projects)",
            "docker": "Docker (for containerization)",
        }
        
        available = {}
        
        for tool, description in tools.items():
            try:
                result = subprocess.run([tool, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    available[tool] = True
                    self.print_success(f"{description} available")
                else:
                    available[tool] = False
                    self.print_info(f"{description} not available (optional)")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                available[tool] = False
                self.print_info(f"{description} not available (optional)")
        
        return available
    
    def create_virtual_environment(self) -> bool:
        """Create Python virtual environment"""
        self.print_info("Setting up Python virtual environment...")
        
        venv_path = Path("venv")
        
        if venv_path.exists():
            self.print_success("Virtual environment already exists")
            return True
        
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            self.print_success("Created virtual environment")
            
            # Provide activation instructions
            if os.name == 'nt':
                activate_cmd = "venv\\Scripts\\activate.bat"
            else:
                activate_cmd = "source venv/bin/activate"
            
            self.print_info(f"To activate: {activate_cmd}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            return False
    
    def run_health_check(self) -> bool:
        """Run a comprehensive health check"""
        self.print_info("Running health check...")
        
        checks = [
            ("Python version", self.check_python_version),
            ("System requirements", self.check_system_requirements),
            ("Dependencies", self.verify_imports),
            ("Environment file", self.check_env_file),
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            try:
                if not check_func():
                    all_passed = False
                    self.print_error(f"Health check failed: {check_name}")
            except Exception as e:
                self.print_error(f"Health check error ({check_name}): {e}")
                all_passed = False
        
        return all_passed
    
    def generate_system_report(self) -> str:
        """Generate a system report"""
        report = {
            "timestamp": str(datetime.now()),
            "system_info": self.system_info,
            "setup_log": self.setup_log,
            "requirements_met": self.requirements_met,
            "optional_tools": self.check_optional_tools()
        }
        
        report_file = f"setup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report_file
    
    def run_full_setup(self) -> bool:
        """Run the complete setup process"""
        self.print_header("AI SDLC Wizard - Professional Edition Setup")
        
        print(f"{Colors.OKBLUE}System Information:{Colors.ENDC}")
        print(f"  Platform: {self.system_info['platform']}")
        print(f"  Python: {self.system_info['python_version']}")
        print(f"  Architecture: {self.system_info['architecture']}")
        
        # Run setup steps
        steps = [
            ("Python Version", self.check_python_version),
            ("System Requirements", self.check_system_requirements),
            ("Directories", self.create_directories),
            ("Virtual Environment", self.create_virtual_environment),
            ("Dependencies", self.install_dependencies),
            ("Environment Config", self.check_env_file),
            ("Import Verification", self.verify_imports),
            ("Configuration Files", self.create_config_files),
        ]
        
        for step_name, step_func in steps:
            self.print_header(f"Step: {step_name}")
            
            try:
                if not step_func():
                    self.print_error(f"Setup step failed: {step_name}")
                    self.requirements_met = False
            except Exception as e:
                self.print_error(f"Setup step error ({step_name}): {e}")
                self.requirements_met = False
        
        # Final report
        self.print_header("Setup Summary")
        
        if self.requirements_met:
            self.print_success("Setup completed successfully! 🎉")
            self.print_info("Next steps:")
            print(f"  1. Update your GROQ_API_KEY in .env file")
            print(f"  2. Run: {Colors.BOLD}streamlit run streamlit_app.py{Colors.ENDC}")
            print(f"  3. Or use the launch script: {Colors.BOLD}./start_wizard.sh{Colors.ENDC} (Unix) or {Colors.BOLD}start_wizard.bat{Colors.ENDC} (Windows)")
        else:
            self.print_error("Setup completed with errors")
            self.print_info("Please check the errors above and retry")
        
        # Generate report
        report_file = self.generate_system_report()
        self.print_info(f"System report saved to: {report_file}")
        
        return self.requirements_met


def main():
    """Main setup function"""
    import datetime
    
    # Check if we're running in the right directory
    if not Path("sdlc_graph.py").exists():
        print(f"{Colors.FAIL}❌ Error: sdlc_graph.py not found. Please run setup from the project root directory.{Colors.ENDC}")
        sys.exit(1)
    
    # Run setup
    setup_manager = SetupManager()
    success = setup_manager.run_full_setup()
    
    if success:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🚀 AI SDLC Wizard is ready to use!{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Visit: http://localhost:8501 after starting the application{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}⚠️  Setup incomplete. Please resolve the issues above.{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()