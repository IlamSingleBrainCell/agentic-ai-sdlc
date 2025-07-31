# AI SDLC Wizard - Professional Edition 🚀

A comprehensive AI-powered Software Development Life Cycle (SDLC) workflow automation tool that transforms your project requirements into production-ready code with autonomous decision-making capabilities.

## ✨ Features

### 🤖 Multi-Language Support
- **Python** - Flask, FastAPI, Django applications
- **JavaScript** - Node.js, Express, React backends  
- **TypeScript** - Type-safe JavaScript development
- **Java** - Spring Boot, enterprise applications
- **Go** - High-performance microservices
- **C#** - .NET applications
- **PHP** - Web applications and APIs
- **Rust** - Systems programming and web services

### 🧠 Autonomous Intelligence
- **Manual Mode**: All decisions require human approval
- **Semi-Autonomous**: High-quality outputs auto-approved
- **Fully Autonomous**: Most decisions automated with quality checks
- **Expert Autonomous**: Advanced AI reasoning with minimal intervention

### 🎯 Complete SDLC Workflow
1. **Requirements Analysis** - AI-powered requirement validation
2. **User Story Generation** - Automatic story creation from requirements
3. **Design Document Creation** - Technical and functional specifications
4. **Multi-Language Code Generation** - Production-ready code in 8+ languages
5. **Security Review** - Language-specific vulnerability scanning
6. **Test Case Generation** - Comprehensive test suites
7. **Quality Assurance** - Automated QA with metrics
8. **Deployment Ready** - Complete project artifacts

### 📊 Advanced Analytics
- Real-time workflow monitoring
- Quality metrics and trends
- Performance optimization suggestions
- Autonomous decision tracking
- Export capabilities (PDF, Word, ZIP)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- 4GB+ RAM (recommended)
- 2GB+ available disk space
- GROQ API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ai-sdlc-wizard
   ```

2. **Run the automated setup**
   ```bash
   python setup.py
   ```

3. **Configure your API key**
   - Update `.env` file with your GROQ_API_KEY
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Start the application**
   ```bash
   # Option 1: Direct launch
   streamlit run streamlit_app.py
   
   # Option 2: Use launch script
   ./start_wizard.sh        # Linux/Mac
   start_wizard.bat         # Windows
   ```

5. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start creating your AI-powered projects! 🎉

## 📋 Usage Guide

### Step 1: Define Requirements
- Enter your project requirements in natural language
- Choose your programming language (Python, JavaScript, Java, etc.)
- Select AI model and autonomy level
- Use templates for common project types

### Step 2: Review Generated Artifacts
- **User Stories**: AI-generated user stories from requirements
- **Design Document**: Technical and functional specifications
- **Source Code**: Production-ready code in your chosen language
- **Test Cases**: Comprehensive test suites
- **Security Review**: Automated vulnerability assessment

### Step 3: Human-in-the-Loop Reviews
- Review and approve each stage
- Provide feedback for regeneration if needed
- Override autonomous decisions when necessary
- Track quality metrics throughout the process

### Step 4: Export and Deploy
- Download complete project as ZIP
- Export documentation (PDF, Word)
- Use generated deployment scripts
- Monitor workflow analytics

## 🎛️ Configuration Options

### Autonomy Levels
- **👨‍💻 Manual**: Full human control over all decisions
- **🤖 Semi-Autonomous**: Auto-approve high-quality outputs (85%+ score)
- **🚀 Fully Autonomous**: Automated workflow with quality checks (75%+ score)
- **🧠 Expert Autonomous**: Minimal human intervention (70%+ score)

### AI Models
- **Gemma 2 9B**: Fast and efficient for most tasks
- **DeepSeek R1**: Advanced reasoning and problem solving
- **Llama 3.1 70B**: Versatile and powerful for complex tasks
- **Mixtral 8x7B**: Large context window for detailed analysis

### Quality Thresholds
- Completeness, consistency, security, and best practices scoring
- Configurable quality thresholds for autonomous decisions
- Real-time quality metrics and recommendations

## 📁 Project Structure

```
ai-sdlc-wizard/
├── streamlit_app.py              # Main Streamlit application
├── sdlc_graph.py                 # Core workflow graph
├── enhanced_sdlc_graph.py        # Multi-language enhancements
├── config.py                     # Configuration settings
├── autonomous_features.py        # AI decision engine
├── advanced_features.py          # Premium functionality
├── ui_utils.py                   # UI utilities and helpers
├── setup.py                      # Setup and installation script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── artifacts/                    # Generated documents
├── generated_code/               # AI-generated source code
├── test_cases/                   # Generated test suites
├── exports/                      # Exported artifacts
├── auto_saves/                   # Automatic backups
└── logs/                         # Application logs
```

## 🔧 Advanced Features

### Code Quality Analysis
- Language-specific quality metrics
- Security vulnerability scanning
- Best practices validation
- Maintainability scoring
- Performance analysis

### Error Recovery
- Automatic error detection and recovery
- Fallback model selection
- Retry mechanisms with exponential backoff
- Error logging and analysis

### Workflow Optimization
- Performance trend analysis
- Bottleneck identification
- Autonomous decision optimization
- Workflow personalization

### Export & Integration
- **JIRA**: Export user stories and tasks
- **GitHub**: Create issues and wiki pages
- **Documentation**: Generate comprehensive docs
- **Deployment**: Create deployment scripts

## 🛠️ Development

### Adding New Languages
1. Update `config.py` with language configuration
2. Add language-specific templates in `enhanced_sdlc_graph.py`
3. Include security patterns in `autonomous_features.py`
4. Test with sample requirements

### Extending Autonomous Features
1. Modify quality metrics in `autonomous_features.py`
2. Add new decision engines for specific domains
3. Implement domain-specific validation rules
4. Update UI to show new metrics

### Custom Templates
1. Add templates to `Config.REQUIREMENT_TEMPLATES`
2. Include language-specific examples
3. Test with different project types
4. Update UI template selector

## 🔒 Security Considerations

### Language-Specific Security Checks
- **Python**: SQL injection, command injection, pickle deserialization
- **JavaScript**: XSS, prototype pollution, dependency vulnerabilities
- **Java**: XXE, deserialization, LDAP injection
- **Go**: Race conditions, memory leaks, unsafe operations
- **C#**: XML injection, insecure deserialization
- **PHP**: File inclusion, session fixation, CSRF
- **Rust**: Unsafe code blocks, integer overflow

### Best Practices
- Never commit API keys or secrets
- Review generated code before deployment
- Run security scans on generated code
- Use environment variables for configuration
- Enable autonomous mode only for trusted requirements

## 📊 Monitoring & Analytics

### Workflow Metrics
- Stage completion times
- Quality score trends
- Autonomous decision rates
- Error and retry statistics
- User feedback analysis

### Performance Optimization
- Real-time performance monitoring
- Bottleneck identification
- Model performance comparison
- Resource usage tracking

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**API Key Issues**
```bash
# Check your .env file
cat .env
# Verify GROQ_API_KEY is set correctly
```

**Streamlit Won't Start**
```bash
# Check if port is available
netstat -an | grep 8501
# Try a different port
streamlit run streamlit_app.py --server.port 8502
```

**Memory Issues**
- Reduce model size in settings
- Use manual mode instead of autonomous
- Clear auto_saves/ directory periodically

### Error Recovery
The system includes automatic error recovery:
- API failures: Automatic retry with exponential backoff
- Model failures: Fallback to alternative models
- Validation errors: Enhanced prompts and suggestions
- Timeout errors: Increased timeout and retry

### Logs and Debugging
- Check `logs/` directory for detailed logs
- Enable debug mode in `.env`: `DEBUG=True`
- Use health check: `python setup.py --health-check`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black .

# Linting
flake8 .

# Security scan
bandit -r .
```

## 📜 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **LangGraph**: Workflow orchestration framework
- **Streamlit**: Beautiful web application framework
- **GROQ**: Fast and efficient AI model inference
- **Plotly**: Interactive visualization library

## 📞 Support

### Getting Help
- 📖 **Documentation**: Check this README and inline comments
- 🐛 **Issues**: Report bugs and feature requests
- 💬 **Discussions**: Community support and questions
- 📧 **Contact**: Professional support available

### System Requirements
- **Minimum**: Python 3.8, 2GB RAM, 1GB disk
- **Recommended**: Python 3.9+, 4GB+ RAM, 2GB+ disk
- **Optimal**: Python 3.10+, 8GB+ RAM, 5GB+ disk

---

**Built with ❤️ by the AI SDLC Wizard Team**

*Transform your ideas into production-ready software with the power of AI*