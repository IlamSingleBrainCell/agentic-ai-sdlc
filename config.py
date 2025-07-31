# config.py
"""
Configuration settings for the AI SDLC Wizard MVP
"""

import os
from typing import Dict, List, Any

class Config:
    """Application configuration"""
    
    # App Settings
    APP_NAME = "AI SDLC Wizard - Enterprise Edition"
    APP_VERSION = "2.0.0"
    APP_ICON = "🚀"
    
    # UI Configuration
    THEME_COLORS = {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
    }
    
    # Programming Languages Configuration
    SUPPORTED_LANGUAGES = {
        "python": {
            "name": "Python",
            "extensions": [".py"],
            "comment_style": "#",
            "test_framework": "pytest",
            "package_manager": "pip",
            "entry_point": "main.py",
            "config_file": "config.py",
            "requirements_file": "requirements.txt"
        },
        "javascript": {
            "name": "JavaScript",
            "extensions": [".js", ".mjs"],
            "comment_style": "//",
            "test_framework": "jest",
            "package_manager": "npm",
            "entry_point": "index.js",
            "config_file": "config.js",
            "requirements_file": "package.json"
        },
        "typescript": {
            "name": "TypeScript",
            "extensions": [".ts", ".tsx"],
            "comment_style": "//",
            "test_framework": "jest",
            "package_manager": "npm",
            "entry_point": "index.ts",
            "config_file": "config.ts",
            "requirements_file": "package.json"
        },
        "java": {
            "name": "Java",
            "extensions": [".java"],
            "comment_style": "//",
            "test_framework": "junit",
            "package_manager": "maven",
            "entry_point": "Main.java",
            "config_file": "Config.java",
            "requirements_file": "pom.xml"
        },
        "go": {
            "name": "Go",
            "extensions": [".go"],
            "comment_style": "//",
            "test_framework": "testing",
            "package_manager": "go mod",
            "entry_point": "main.go",
            "config_file": "config.go",
            "requirements_file": "go.mod"
        },
        "csharp": {
            "name": "C#",
            "extensions": [".cs"],
            "comment_style": "//",
            "test_framework": "nunit",
            "package_manager": "nuget",
            "entry_point": "Program.cs",
            "config_file": "Config.cs",
            "requirements_file": "project.csproj"
        },
        "php": {
            "name": "PHP",
            "extensions": [".php"],
            "comment_style": "//",
            "test_framework": "phpunit",
            "package_manager": "composer",
            "entry_point": "index.php",
            "config_file": "config.php",
            "requirements_file": "composer.json"
        },
        "rust": {
            "name": "Rust",
            "extensions": [".rs"],
            "comment_style": "//",
            "test_framework": "cargo test",
            "package_manager": "cargo",
            "entry_point": "main.rs",
            "config_file": "config.rs",
            "requirements_file": "Cargo.toml"
        }
    }
    
    # LLM Model Configuration
    AVAILABLE_MODELS = {
        "gemma2-9b-it": {
            "name": "Gemma 2 9B Instruct",
            "description": "Fast and efficient for most tasks",
            "max_tokens": 8192,
            "best_for": ["code generation", "general tasks"],
            "speed": "fast"
        },
        "deepseek-r1-distill-llama-70b": {
            "name": "DeepSeek R1 Distill",
            "description": "Advanced reasoning and problem solving",
            "max_tokens": 8192,
            "best_for": ["complex reasoning", "architecture design"],
            "speed": "medium"
        },
        "llama-3.1-70b-versatile": {
            "name": "Llama 3.1 70B",
            "description": "Versatile and powerful for all tasks",
            "max_tokens": 8192,
            "best_for": ["comprehensive analysis", "complex code"],
            "speed": "medium"
        },
        "mixtral-8x7b-32768": {
            "name": "Mixtral 8x7B",
            "description": "Large context window for complex projects",
            "max_tokens": 32768,
            "best_for": ["large codebases", "detailed analysis"],
            "speed": "medium"
        },
        "qwen-qwq-32b": {
            "name": "Qwen QwQ 32B",
            "description": "Advanced reasoning and mathematical tasks",
            "max_tokens": 8192,
            "best_for": ["complex logic", "algorithmic problems"],
            "speed": "medium"
        }
    }
    
    # Autonomy Levels Configuration
    AUTONOMY_LEVELS = {
        "manual": {
            "name": "Manual",
            "icon": "👨‍💻",
            "description": "All decisions require human approval",
            "auto_approve_threshold": 1.0,  # Never auto-approve
            "quality_threshold": 1.0
        },
        "semi_auto": {
            "name": "Semi-Autonomous",
            "icon": "🤖",
            "description": "High-quality outputs auto-approved, others need review",
            "auto_approve_threshold": 0.85,
            "quality_threshold": 0.85
        },
        "full_auto": {
            "name": "Fully Autonomous",
            "icon": "🚀",
            "description": "Most decisions automated with quality checks",
            "auto_approve_threshold": 0.75,
            "quality_threshold": 0.75
        },
        "expert_auto": {
            "name": "Expert Autonomous",
            "icon": "🧠",
            "description": "Advanced AI reasoning with minimal human intervention",
            "auto_approve_threshold": 0.70,
            "quality_threshold": 0.70
        }
    }
    
    # Workflow Configuration
    WORKFLOW_STAGES = [
        {
            "name": "User Requirements",
            "icon": "📋",
            "description": "Define project requirements",
            "type": "input",
            "autonomous": False
        },
        {
            "name": "Auto-generate User Stories",
            "icon": "🤖",
            "description": "AI generates user stories",
            "type": "ai",
            "autonomous": True
        },
        {
            "name": "Human User Story Approval",
            "icon": "👥",
            "description": "Review and approve stories",
            "type": "human",
            "autonomous": False
        },
        {
            "name": "Create Design Document",
            "icon": "📐",
            "description": "Generate technical design",
            "type": "ai",
            "autonomous": True
        },
        {
            "name": "Human Design Document Review",
            "icon": "🔍",
            "description": "Review design document",
            "type": "human",
            "autonomous": False
        },
        {
            "name": "Generate Code",
            "icon": "💻",
            "description": "AI writes the code",
            "type": "ai",
            "autonomous": True
        },
        {
            "name": "Human Code Review",
            "icon": "👨‍💻",
            "description": "Review generated code",
            "type": "human",
            "autonomous": False
        },
        {
            "name": "Security Review",
            "icon": "🔒",
            "description": "Automated security check",
            "type": "ai",
            "autonomous": True
        },
        {
            "name": "Human Security Review",
            "icon": "🛡️",
            "description": "Manual security review",
            "type": "human",
            "autonomous": False
        },
        {
            "name": "Write Test Cases",
            "icon": "🧪",
            "description": "Generate test cases",
            "type": "ai",
            "autonomous": True
        },
        {
            "name": "Human Test Cases Review",
            "icon": "✔️",
            "description": "Review test cases",
            "type": "human",
            "autonomous": False
        },
        {
            "name": "QA Testing",
            "icon": "🎯",
            "description": "Run quality assurance",
            "type": "ai",
            "autonomous": True
        },
        {
            "name": "Human QA Review",
            "icon": "✅",
            "description": "Final QA approval",
            "type": "human",
            "autonomous": False
        },
        {
            "name": "Deployment",
            "icon": "🚀",
            "description": "Deploy to production",
            "type": "deployment",
            "autonomous": True
        }
    ]
    
    # File Paths
    ARTIFACTS_DIR = "artifacts"
    CODE_OUTPUT_DIR = "generated_code"
    TEST_CASES_DIR = "test_cases"
    EXPORTS_DIR = "exports"
    AUTO_SAVES_DIR = "auto_saves"
    LOGS_DIR = "logs"
    
    # LLM Settings
    DEFAULT_LLM_MODEL = "gemma2-9b-it"
    
    # Validation Settings
    MIN_REQUIREMENT_WORDS = 10
    RECOMMENDED_REQUIREMENT_WORDS = 50
    MAX_REQUIREMENT_WORDS = 1000
    
    # Export Settings
    EXPORT_FORMATS = ["PDF", "Word", "ZIP", "JSON"]
    PDF_PAGE_SIZE = "letter"  # or "A4"
    
    # Notification Settings
    NOTIFICATION_DURATION = 3  # seconds
    MAX_NOTIFICATIONS = 10
    
    # Analytics Settings
    ENABLE_ANALYTICS = True
    TRACK_TIMING = True
    TRACK_ERRORS = True
    
    # Security Settings
    ENABLE_SECURITY_SCAN = True
    SECURITY_RULES = [
        "no_hardcoded_secrets",
        "input_validation",
        "sql_injection_prevention",
        "xss_prevention",
        "authentication_required",
        "authorization_checks",
        "encryption_for_sensitive_data"
    ]
    
    # Performance Settings
    CACHE_ENABLED = True
    CACHE_TTL = 3600  # 1 hour
    MAX_CONCURRENT_REQUESTS = 5
    
    # Feature Flags
    FEATURES = {
        "dark_mode": True,
        "export_analytics": True,
        "advanced_code_analysis": True,
        "auto_save": True,
        "collaboration": False,  # Future feature
        "version_control": False,  # Future feature
        "ci_cd_integration": False,  # Future feature
        "custom_templates": True,
        "ai_suggestions": True,
        "real_time_updates": True,
        "autonomous_mode": True,
        "multi_language": True,
        "quality_metrics": True,
        "error_recovery": True
    }
    
    # Code Generation Templates
    CODE_TEMPLATES = {
        "python": {
            "web_app": """
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Routes
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the API'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
""",
            "api": """
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Generated API", version="1.0.0")

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return []

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    return item
"""
        },
        "javascript": {
            "web_app": """
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
    res.json({ message: 'Welcome to the API' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
""",
            "api": """
const express = require('express');
const router = express.Router();

// GET /api/items
router.get('/items', async (req, res) => {
    try {
        // Implementation here
        res.json({ items: [] });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// POST /api/items
router.post('/items', async (req, res) => {
    try {
        const item = req.body;
        // Implementation here
        res.status(201).json(item);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
"""
        }
    }
    
    # Templates
    REQUIREMENT_TEMPLATES = {
        "E-commerce Platform": {
            "description": "Online shopping platform with full e-commerce capabilities",
            "template": """Create an e-commerce platform with the following features:
- User authentication and profile management
- Product catalog with categories and search
- Shopping cart and wishlist functionality
- Secure payment processing with multiple payment methods
- Order management and tracking
- Admin dashboard for inventory and sales management
- Email notifications for order updates
- Mobile-responsive design
- Product reviews and ratings
- Recommendation engine"""
        },
        "SaaS Dashboard": {
            "description": "Analytics dashboard for Software-as-a-Service applications",
            "template": """Build a SaaS analytics dashboard with:
- Multi-tenant architecture with organization management
- User roles and permissions (Admin, Manager, Viewer)
- Real-time data visualization with charts and graphs
- Custom dashboard creation and widget management
- Data export in multiple formats (CSV, Excel, PDF)
- API integration for data ingestion
- Automated reporting and alerts
- Audit logs and activity tracking
- Billing and subscription management
- Two-factor authentication"""
        },
        "Mobile App Backend": {
            "description": "RESTful API backend for mobile applications",
            "template": """Develop a REST API backend for a mobile app with:
- JWT-based authentication and token refresh
- User profile management with avatar upload
- Push notification service integration
- Real-time chat/messaging functionality
- Social media integration (login and sharing)
- Geolocation services and mapping
- File upload and media management
- Offline data synchronization
- Rate limiting and API throttling
- Comprehensive API documentation"""
        },
        "API Service": {
            "description": "Microservice API with enterprise features",
            "template": """Create a microservice API with:
- RESTful endpoints following OpenAPI specification
- CRUD operations for core entities
- Advanced filtering, sorting, and pagination
- API key authentication and OAuth2 support
- Rate limiting per user/API key
- Request/response validation
- Error handling with proper HTTP status codes
- API versioning support
- Webhook functionality for event notifications
- Health check and monitoring endpoints"""
        },
        "Data Processing Pipeline": {
            "description": "Data processing and analytics pipeline",
            "template": """Build a data processing pipeline with:
- Data ingestion from multiple sources (APIs, files, databases)
- Data validation and cleansing
- ETL (Extract, Transform, Load) operations
- Real-time and batch processing capabilities
- Data quality monitoring and alerts
- Scalable architecture with queue management
- Error handling and retry mechanisms
- Data lineage tracking
- Integration with data warehouses
- Automated reporting and dashboards"""
        },
        "Machine Learning Platform": {
            "description": "ML model training and deployment platform",
            "template": """Create a machine learning platform with:
- Model training pipeline with experiment tracking
- Feature engineering and data preprocessing
- Model versioning and artifact management
- Automated model validation and testing
- REST API for model inference
- A/B testing framework for model comparison
- Real-time monitoring and alerting
- Scalable inference serving
- Integration with MLOps tools
- Model performance analytics and drift detection"""
        }
    }
    
    # Quality Thresholds for different autonomy levels
    QUALITY_THRESHOLDS = {
        "manual": 1.0,          # Never auto-approve
        "semi_auto": 0.85,      # High threshold for auto-approval
        "full_auto": 0.75,      # Medium threshold
        "expert_auto": 0.70     # Lower threshold for expert mode
    }
    
    # Error Recovery Configuration
    ERROR_RECOVERY = {
        "max_retries": 3,
        "retry_delay": 2,  # seconds
        "fallback_models": ["gemma2-9b-it", "llama-3.1-70b-versatile"],
        "timeout": 120,  # seconds
        "enable_auto_recovery": True
    }
    
    # Performance Monitoring
    PERFORMANCE_CONFIG = {
        "track_stage_duration": True,
        "track_quality_scores": True,
        "track_user_feedback": True,
        "track_autonomous_decisions": True,
        "optimization_enabled": True
    }
    
    @classmethod
    def get_stage_by_name(cls, name: str) -> Dict[str, Any]:
        """Get workflow stage configuration by name"""
        for stage in cls.WORKFLOW_STAGES:
            if stage["name"] == name:
                return stage
        return None
    
    @classmethod
    def is_feature_enabled(cls, feature: str) -> bool:
        """Check if a feature is enabled"""
        return cls.FEATURES.get(feature, False)
    
    @classmethod
    def get_theme_color(cls, color_type: str) -> str:
        """Get theme color by type"""
        return cls.THEME_COLORS.get(color_type, "#000000")
    
    @classmethod
    def get_language_config(cls, language: str) -> Dict[str, Any]:
        """Get configuration for a specific programming language"""
        return cls.SUPPORTED_LANGUAGES.get(language, cls.SUPPORTED_LANGUAGES["python"])
    
    @classmethod
    def get_model_config(cls, model: str) -> Dict[str, Any]:
        """Get configuration for a specific LLM model"""
        return cls.AVAILABLE_MODELS.get(model, cls.AVAILABLE_MODELS[cls.DEFAULT_LLM_MODEL])
    
    @classmethod
    def get_autonomy_config(cls, level: str) -> Dict[str, Any]:
        """Get configuration for a specific autonomy level"""
        return cls.AUTONOMY_LEVELS.get(level, cls.AUTONOMY_LEVELS["manual"])
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        directories = [
            cls.ARTIFACTS_DIR,
            cls.CODE_OUTPUT_DIR,
            cls.TEST_CASES_DIR,
            cls.EXPORTS_DIR,
            cls.AUTO_SAVES_DIR,
            cls.LOGS_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def get_code_template(cls, language: str, project_type: str = "web_app") -> str:
        """Get code template for specific language and project type"""
        return cls.CODE_TEMPLATES.get(language, {}).get(project_type, "")


# Environment-specific overrides
class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    CACHE_ENABLED = False
    TRACK_ERRORS = True
    ENABLE_AUTO_RECOVERY = True


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    CACHE_ENABLED = True
    TRACK_ERRORS = True
    MAX_CONCURRENT_REQUESTS = 20
    ENABLE_AUTO_RECOVERY = True


# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv("APP_ENV", "development")
    
    if env == "production":
        return ProductionConfig
    else:
        return DevelopmentConfig


# Export the active configuration
ActiveConfig = get_config()