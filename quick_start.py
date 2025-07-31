# quick_start.py
"""
Quick Start Launcher for AI SDLC Wizard
Run this script to get started quickly with minimal setup
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🚀 AI SDLC Wizard - Quick Start                    ║
║                                                              ║
║        Get Started in Under 2 Minutes!                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        print("💡 Please install Python 3.8+ from https://python.org")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_streamlit():
    """Install Streamlit if not available"""
    try:
        import streamlit
        print("✅ Streamlit already installed")
        return True
    except ImportError:
        print("📦 Installing Streamlit...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
            print("✅ Streamlit installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Streamlit")
            return False

def install_essential_deps():
    """Install only essential dependencies"""
    print("📦 Installing essential dependencies...")
    
    essential_deps = [
        "plotly",
        "pandas", 
        "python-dotenv",
        "langchain",
        "langchain-groq",
        "langgraph",
        "groq",
        "pydantic",
        "python-docx"
    ]
    
    failed_deps = []
    
    for dep in essential_deps:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {dep}")
        except subprocess.CalledProcessError:
            print(f"⚠️  {dep} (will try to continue)")
            failed_deps.append(dep)
    
    if failed_deps:
        print(f"\n⚠️  Some dependencies failed to install: {', '.join(failed_deps)}")
        print("💡 Try running: pip install -r requirements.txt")
    
    return len(failed_deps) < len(essential_deps) // 2  # Allow some failures

def create_basic_env():
    """Create basic .env file"""
    if not Path(".env").exists():
        print("📝 Creating .env file...")
        env_content = """# AI SDLC Wizard Configuration
GROQ_API_KEY=your_groq_api_key_here
APP_ENV=development
DEBUG=True
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("💡 Please edit .env and add your GROQ_API_KEY")
        return False
    else:
        # Check if API key is configured
        with open(".env", "r") as f:
            content = f.read()
            if "your_groq_api_key_here" in content:
                print("⚠️  Please configure your GROQ_API_KEY in .env file")
                return False
        print("✅ .env file configured")
        return True

def create_basic_dirs():
    """Create basic directories"""
    dirs = ["artifacts", "generated_code", "test_cases", "exports"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Created basic directories")

def check_core_files():
    """Check if core files exist"""
    core_files = ["streamlit_app.py", "sdlc_graph.py", "config.py"]
    missing_files = []
    
    for file in core_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing core files: {', '.join(missing_files)}")
        print("💡 Please ensure all Python files are in the current directory")
        return False
    
    print("✅ All core files present")
    return True

def get_groq_api_key():
    """Help user get GROQ API key"""
    print("\n🔑 Getting GROQ API Key:")
    print("1. Visit: https://console.groq.com/")
    print("2. Sign up for a free account")
    print("3. Click 'Create API Key'")
    print("4. Copy the key (starts with 'gsk_')")
    print("5. Paste it in your .env file")
    print("\nExample .env file:")
    print("GROQ_API_KEY=gsk_your_actual_key_here")

def start_application():
    """Start the Streamlit application"""
    print("\n🚀 Starting AI SDLC Wizard...")
    
    # Determine which app to run
    if Path("streamlit_app_professional.py").exists():
        app_file = "streamlit_app_professional.py"
        print("🎯 Using Professional Edition")
    else:
        app_file = "streamlit_app.py"
        print("🎯 Using Standard Edition")
    
    print("🌐 Opening browser to http://localhost:8501")
    print("💡 Press Ctrl+C to stop the application\n")
    
    try:
        subprocess.run([
            "streamlit", "run", app_file,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped")
    except FileNotFoundError:
        print("❌ Streamlit command not found")
        print("💡 Try: python -m streamlit run " + app_file)

def main():
    """Main quick start function"""
    print_banner()
    
    # Check prerequisites
    if not check_python():
        input("Press Enter to exit...")
        return
    
    # Install Streamlit
    if not install_streamlit():
        input("Press Enter to exit...")
        return
    
    # Check core files
    if not check_core_files():
        input("Press Enter to exit...")
        return
    
    # Create basic setup
    create_basic_dirs()
    
    # Check/create environment
    env_ready = create_basic_env()
    
    if not env_ready:
        print("\n" + "="*50)
        get_groq_api_key()
        print("\n💡 After configuring your API key, run this script again!")
        input("Press Enter to exit...")
        return
    
    # Install essential dependencies
    print("\n📦 Installing dependencies (this may take a minute)...")
    deps_ok = install_essential_deps()
    
    if not deps_ok:
        print("\n⚠️  Some dependencies failed. Trying to continue...")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Everything ready - start the app
    print("\n" + "="*50)
    print("🎉 Setup complete! Starting the application...")
    print("="*50)
    
    start_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        print("💡 Try running the full installer: python install.py")