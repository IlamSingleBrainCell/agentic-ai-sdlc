# launcher.py
"""
Simple launcher script for AI SDLC Wizard
Handles environment setup and application startup
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           🚀 AI SDLC Wizard - Professional Edition           ║
    ║                                                              ║
    ║        Transform Ideas → Production-Ready Software           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_environment():
    """Check if environment is properly set up"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required (current: {sys.version_info.major}.{sys.version_info.minor})")
    
    # Check for required files
    required_files = ["streamlit_app.py", "sdlc_graph.py", "config.py"]
    for file in required_files:
        if not Path(file).exists():
            issues.append(f"Missing required file: {file}")
    
    # Check for .env file
    if not Path(".env").exists():
        issues.append("Missing .env file (copy from .env.example and update GROQ_API_KEY)")
    
    # Check for GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "your_groq_api_key_here":
        issues.append("GROQ_API_KEY not configured in .env file")
    
    return issues

def install_missing_dependencies():
    """Install missing dependencies"""
    print("🔧 Checking dependencies...")
    
    try:
        import streamlit
        print("✅ Streamlit available")
    except ImportError:
        print("📦 Installing Streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    try:
        import plotly
        print("✅ Plotly available")
    except ImportError:
        print("📦 Installing Plotly...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
    
    # Install from requirements.txt if available
    if Path("requirements.txt").exists():
        print("📦 Installing from requirements.txt...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], stdout=subprocess.DEVNULL)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError:
            print("⚠️  Some dependencies may have failed to install")

def start_application():
    """Start the Streamlit application"""
    print("🚀 Starting AI SDLC Wizard...")
    print("📱 Opening in your default browser...")
    print("🌐 URL: http://localhost:8501")
    print("\n" + "="*50)
    print("💡 Tips:")
    print("   • Press Ctrl+C to stop the application")
    print("   • Use 'r' to reload if you make changes")
    print("   • Check the browser tab for the interface")
    print("="*50 + "\n")
    
    # Give user a moment to read the tips
    time.sleep(2)
    
    try:
        # Try to use the professional app first, fallback to basic
        if Path("streamlit_app_professional.py").exists():
            app_file = "streamlit_app_professional.py"
        else:
            app_file = "streamlit_app.py"
        
        subprocess.run([
            "streamlit", "run", app_file,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed. Please run the launcher again.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False
    
    return True

def show_help():
    """Show help information"""
    help_text = """
🆘 AI SDLC Wizard - Help

Usage:
    python launcher.py [options]

Options:
    --help, -h          Show this help message
    --setup, -s         Run setup and dependency installation
    --check, -c         Check environment and configuration
    --port PORT         Use custom port (default: 8501)
    --no-browser        Don't open browser automatically

Environment Setup:
    1. Copy .env.example to .env
    2. Add your GROQ_API_KEY to .env
    3. Run: python launcher.py --setup

Troubleshooting:
    • Import errors: Run 'python launcher.py --setup'
    • Port conflicts: Use '--port 8502'
    • API errors: Check your GROQ_API_KEY in .env
    • Permission errors: Run as administrator/sudo

For more help, see README.md or visit the documentation.
    """
    print(help_text)

def run_setup():
    """Run the setup process"""
    print("🔧 Running setup process...")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("📦 Installing python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        from dotenv import load_dotenv
        load_dotenv()
    
    # Run main setup
    if Path("setup.py").exists():
        try:
            subprocess.check_call([sys.executable, "setup.py"])
        except subprocess.CalledProcessError:
            print("⚠️  Setup script encountered issues")
    else:
        # Basic setup
        install_missing_dependencies()
        
        # Create directories
        directories = ["artifacts", "generated_code", "test_cases", "exports", "auto_saves", "logs"]
        for dir_name in directories:
            Path(dir_name).mkdir(exist_ok=True)
            print(f"✅ Created {dir_name}/")

def main():
    """Main launcher function"""
    # Parse command line arguments
    args = sys.argv[1:]
    port = "8501"
    open_browser = True
    
    if "--help" in args or "-h" in args:
        show_help()
        return
    
    if "--setup" in args or "-s" in args:
        run_setup()
        return
    
    if "--port" in args:
        try:
            port_index = args.index("--port") + 1
            port = args[port_index]
        except (ValueError, IndexError):
            print("❌ Invalid port specification")
            return
    
    if "--no-browser" in args:
        open_browser = False
    
    if "--check" in args or "-c" in args:
        print("🔍 Checking environment...")
        issues = check_environment()
        if issues:
            print("❌ Environment issues found:")
            for issue in issues:
                print(f"   • {issue}")
            print("\n💡 Run 'python launcher.py --setup' to fix issues")
        else:
            print("✅ Environment looks good!")
        return
    
    # Main application flow
    print_banner()
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("📦 Installing python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    
    # Check environment
    issues = check_environment()
    if issues:
        print("⚠️  Environment issues detected:")
        for issue in issues:
            print(f"   • {issue}")
        
        response = input("\n🔧 Would you like to run setup automatically? (y/n): ")
        if response.lower() in ['y', 'yes']:
            run_setup()
        else:
            print("💡 Please run 'python launcher.py --setup' manually")
            return
    
    # Install dependencies if needed
    try:
        import streamlit
    except ImportError:
        print("📦 Installing missing dependencies...")
        install_missing_dependencies()
    
    # Start the application
    success = start_application()
    
    if success:
        print("👋 Thank you for using AI SDLC Wizard!")
    else:
        print("❌ Application failed to start properly")
        print("💡 Try running 'python launcher.py --setup' to fix issues")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please check the error above and try again")