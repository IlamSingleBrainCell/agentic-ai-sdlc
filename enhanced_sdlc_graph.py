# enhanced_sdlc_graph.py
"""
Enhanced SDLC Graph with multi-language support and dynamic LLM selection
"""

import os
from dotenv import load_dotenv
import re
from typing import List, Dict, Literal, Optional
from typing_extensions import TypedDict
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from datetime import datetime

# Import config with fallback
try:
    from config import Config
except ImportError:
    # Fallback config if config.py is not available
    class Config:
        DEFAULT_LLM_MODEL = "gemma2-9b-it"
        SUPPORTED_LANGUAGES = {
            "python": {
                "name": "Python",
                "extensions": [".py"],
                "comment_style": "#",
                "test_framework": "pytest",
                "package_manager": "pip",
                "entry_point": "main.py"
            },
            "javascript": {
                "name": "JavaScript", 
                "extensions": [".js"],
                "comment_style": "//",
                "test_framework": "jest",
                "package_manager": "npm",
                "entry_point": "index.js"
            }
        }

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Enhanced State with language and model selection
class EnhancedState(TypedDict):
    """Enhanced state with language and autonomy settings"""
    requirements: str
    programming_language: str
    llm_model: str
    autonomy_level: str
    user_stories: List[str]
    user_story_status: Literal["Approve", "Denied"]
    user_story_feedback: List[str]
    design_document_review_status: Literal["Approve", "Denied"]
    design_document_review_feedback: List[str]
    design_document: Dict[str, List[str]]
    code: str
    code_review_status: str
    code_review_feedback: List[str]
    security_review_status: str
    security_review_feedback: str
    test_cases: str
    test_cases_review_status: str
    test_cases_review_feedback: List[str]
    qa_review_status: str
    qa_review_feedback: List[str]
    deployment: str
    # Quality metrics for autonomous decisions
    quality_metrics: Optional[Dict[str, float]]
    autonomous_decisions: List[Dict[str, any]]

def get_llm(model_name: str = None):
    """Get LLM instance with specified model"""
    if not model_name:
        model_name = Config.DEFAULT_LLM_MODEL
    
    return ChatGroq(
        model=model_name,
        temperature=0.7,
        max_tokens=8192
    )

def get_language_specific_prompt_addon(language: str) -> str:
    """Get language-specific instructions for prompts"""
    lang_config = Config.SUPPORTED_LANGUAGES.get(language, {})
    
    return f"""
    Programming Language: {lang_config.get('name', language)}
    File Extension: {', '.join(lang_config.get('extensions', ['.txt']))}
    Comment Style: {lang_config.get('comment_style', '#')}
    Test Framework: {lang_config.get('test_framework', 'generic')}
    Package Manager: {lang_config.get('package_manager', 'none')}
    Entry Point: {lang_config.get('entry_point', 'main')}
    
    Please generate code following {lang_config.get('name', language)} best practices and conventions.
    """

def generate_code_enhanced(state: EnhancedState):
    """Enhanced code generation with multi-language support"""
    language = state.get('programming_language', 'python')
    llm_model = state.get('llm_model', Config.DEFAULT_LLM_MODEL)
    
    # Get language-specific configuration
    lang_config = Config.SUPPORTED_LANGUAGES.get(language, Config.SUPPORTED_LANGUAGES['python'])
    language_addon = get_language_specific_prompt_addon(language)
    
    # Base prompt template with language support
    prompt_template = """
    You are a senior software architect and {language} expert responsible for building modular, production-grade systems.

    {language_instructions}

    Your task is to generate {language} code based on the following design document:

    {design_document}

    ---

    ### Output Goal:
    Split the project requirements into multiple {language} files, each with a specific responsibility.

    ---

    ### Language-Specific Rules for {language}:
    {language_specific_rules}

    ### General Rules:
    1. For **each file**, include:
    - A `Filename:` line specifying the file name with appropriate extension
    - A `Code:` block with the actual code in a fenced markdown block
    
    2. Follow {language} naming conventions and best practices
    3. Include appropriate error handling for {language}
    4. Add comments and documentation following {language} standards
    5. Use the standard library and common packages for {language}

    ---

    ### Example Output Format:
    Filename: {example_filename}
    Code:
    ```{language_lower}
    {comment_style} Full {language} code for this file
    ```

    Generate production-ready {language} code that follows all best practices.
    """
    
    # Language-specific rules
    language_rules = {
        "python": """
        - Use snake_case for files and functions
        - Include type hints where appropriate
        - Follow PEP 8 style guide
        - Use docstrings for functions and classes
        - Create requirements.txt for dependencies
        - Structure: main.py, models.py, services.py, utils.py, config.py
        """,
        "javascript": """
        - Use camelCase for variables and functions
        - Use PascalCase for classes and components
        - Follow ES6+ standards
        - Include JSDoc comments
        - Create package.json for dependencies
        - Structure: index.js, models.js, services.js, utils.js, config.js
        """,
        "typescript": """
        - Use camelCase for variables and functions
        - Use PascalCase for classes and interfaces
        - Define interfaces for all data structures
        - Use strict type checking
        - Create package.json and tsconfig.json
        - Structure: index.ts, models.ts, services.ts, utils.ts, types.ts
        """,
        "java": """
        - Use camelCase for methods and variables
        - Use PascalCase for classes
        - Follow Java naming conventions
        - Include Javadoc comments
        - Create pom.xml for Maven or build.gradle for Gradle
        - Structure: Main.java, models/, services/, utils/, config/
        """,
        "go": """
        - Use camelCase for unexported, PascalCase for exported
        - Follow Go idioms and effective Go guidelines
        - Include godoc comments
        - Create go.mod for dependencies
        - Structure: main.go, models/, services/, utils/, config/
        """,
        "csharp": """
        - Use PascalCase for public members and types
        - Use camelCase for private fields
        - Follow C# coding conventions
        - Include XML documentation comments
        - Create .csproj file
        - Structure: Program.cs, Models/, Services/, Utils/, Config/
        """,
        "php": """
        - Use camelCase for variables and functions
        - Use PascalCase for classes
        - Follow PSR standards
        - Include DocBlock comments
        - Create composer.json for dependencies
        - Structure: index.php, Models/, Services/, Utils/, Config/
        """,
        "rust": """
        - Use snake_case for functions and variables
        - Use PascalCase for types and traits
        - Follow Rust idioms and ownership principles
        - Include rustdoc comments
        - Create Cargo.toml for dependencies
        - Structure: main.rs, lib.rs, models/, services/, utils/
        """
    }
    
    # Get LLM with specified model
    llm = get_llm(llm_model)
    
    # Format the prompt
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["design_document", "language", "language_instructions", 
                        "language_specific_rules", "language_lower", "comment_style", 
                        "example_filename"]
    )
    
    # Get language-specific values
    comment_style = lang_config.get('comment_style', '#')
    example_filename = lang_config.get('entry_point', 'main.py')
    
    # Generate code
    response = prompt | llm
    code_response = response.invoke({
        "design_document": state['design_document'],
        "language": lang_config.get('name', language),
        "language_instructions": language_addon,
        "language_specific_rules": language_rules.get(language, "Follow standard best practices"),
        "language_lower": language.lower(),
        "comment_style": comment_style,
        "example_filename": example_filename
    })
    
    # Extract and save the generated code
    generated_code = code_response.content if hasattr(code_response, "content") else str(code_response)
    
    # Parse and save files with language-specific extensions
    file_blocks = parse_files_with_language(generated_code, language)
    save_files_with_language(file_blocks, f"generated_code_{language}")
    
    state['code'] = generated_code
    return state

def parse_files_with_language(response_text: str, language: str) -> List[Dict[str, str]]:
    """Parse files with language-specific extensions"""
    lang_config = Config.SUPPORTED_LANGUAGES.get(language, Config.SUPPORTED_LANGUAGES['python'])
    extensions = lang_config.get('extensions', ['.txt'])
    
    # Create pattern that matches any of the language's extensions
    ext_pattern = '|'.join(re.escape(ext) for ext in extensions)
    pattern = rf"Filename:\s*(?P<filename>[\w_/]+(?:{ext_pattern}))\s*Code:\s*```(?:\w+)?\s*(?P<code>.*?)```"
    
    matches = list(re.finditer(pattern, response_text, re.DOTALL | re.IGNORECASE))
    
    files = []
    if matches:
        for match in matches:
            files.append({
                "filename": match.group("filename").strip(),
                "code": match.group("code").strip()
            })
    else:
        # Fallback with default extension
        fallback_match = re.search(r"```(?:\w+)?\s*(.*?)```", response_text, re.DOTALL)
        if fallback_match:
            entry_point = lang_config.get('entry_point', 'main.txt')
            files.append({
                "filename": entry_point,
                "code": fallback_match.group(1).strip()
            })
    
    return files

def save_files_with_language(file_blocks: List[Dict[str, str]], output_dir: str):
    """Save files with proper directory structure for the language"""
    os.makedirs(output_dir, exist_ok=True)
    
    for file in file_blocks:
        filename = file.get("filename", "unnamed.txt")
        code = file.get("code", "")
        
        # Create subdirectories if the filename contains paths
        filepath = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        
        print(f"✅ Saved: {filename}")

def write_test_cases_enhanced(state: EnhancedState):
    """Enhanced test case generation with language-specific frameworks"""
    language = state.get('programming_language', 'python')
    llm_model = state.get('llm_model', Config.DEFAULT_LLM_MODEL)
    lang_config = Config.SUPPORTED_LANGUAGES.get(language, Config.SUPPORTED_LANGUAGES['python'])
    
    prompt_template = """
    You are a senior QA engineer and {language} testing expert.

    ### Language Information:
    - Programming Language: {language}
    - Test Framework: {test_framework}
    - Comment Style: {comment_style}

    ### Objective:
    Based on the generated {language} code and design specifications, write comprehensive test cases using {test_framework}.

    ### Code to Test:
    {generated_code}

    ### Design Document:
    {design_document}

    ### Requirements:
    1. Generate test cases appropriate for {language} and {test_framework}
    2. Include:
       - Unit tests for individual functions/methods
       - Integration tests for component interactions
       - Edge cases and error scenarios
       - Performance tests where applicable
    3. Follow {test_framework} conventions and best practices
    4. Include setup and teardown procedures
    5. Add clear test descriptions

    ### Output Format:
    For {language} with {test_framework}, generate test files with proper structure.
    
    Example for {language}:
    {test_example}

    Generate comprehensive test cases that ensure code quality and reliability.
    """
    
    # Test examples for different languages
    test_examples = {
        "python": """
    Filename: test_main.py
    Code:
    ```python
    import pytest
    from main import *

    class TestMainFunctionality:
        def setup_method(self):
            # Setup test data
            pass
        
        def test_happy_path(self):
            # Test normal operation
            assert function_under_test(valid_input) == expected_output
        
        def test_edge_case(self):
            # Test edge cases
            assert function_under_test(edge_input) == edge_output
        
        def test_error_handling(self):
            # Test error scenarios
            with pytest.raises(ExpectedException):
                function_under_test(invalid_input)
    ```
    """,
        "javascript": """
    Filename: main.test.js
    Code:
    ```javascript
    const { functionUnderTest } = require('./main');

    describe('Main Functionality', () => {
        beforeEach(() => {
            // Setup
        });
        
        test('should handle happy path', () => {
            expect(functionUnderTest(validInput)).toBe(expectedOutput);
        });
        
        test('should handle edge cases', () => {
            expect(functionUnderTest(edgeInput)).toBe(edgeOutput);
        });
        
        test('should throw error for invalid input', () => {
            expect(() => functionUnderTest(invalidInput)).toThrow();
        });
    });
    ```
    """,
        "java": """
    Filename: MainTest.java
    Code:
    ```java
    import org.junit.Test;
    import org.junit.Before;
    import static org.junit.Assert.*;

    public class MainTest {
        private Main main;
        
        @Before
        public void setUp() {
            main = new Main();
        }
        
        @Test
        public void testHappyPath() {
            assertEquals(expectedOutput, main.functionUnderTest(validInput));
        }
        
        @Test
        public void testEdgeCase() {
            assertEquals(edgeOutput, main.functionUnderTest(edgeInput));
        }
        
        @Test(expected = ExpectedException.class)
        public void testErrorHandling() {
            main.functionUnderTest(invalidInput);
        }
    }
    ```
    """,
        "go": """
    Filename: main_test.go
    Code:
    ```go
    package main

    import (
        "testing"
    )

    func TestHappyPath(t *testing.T) {
        result := functionUnderTest(validInput)
        if result != expectedOutput {
            t.Errorf("Expected %v, got %v", expectedOutput, result)
        }
    }

    func TestEdgeCase(t *testing.T) {
        result := functionUnderTest(edgeInput)
        if result != edgeOutput {
            t.Errorf("Expected %v, got %v", edgeOutput, result)
        }
    }

    func TestErrorHandling(t *testing.T) {
        defer func() {
            if r := recover(); r == nil {
                t.Error("Expected panic but didn't get one")
            }
        }()
        functionUnderTest(invalidInput)
    }
    ```
    """,
        "csharp": """
    Filename: MainTests.cs
    Code:
    ```csharp
    using NUnit.Framework;

    [TestFixture]
    public class MainTests
    {
        private Main _main;

        [SetUp]
        public void Setup()
        {
            _main = new Main();
        }

        [Test]
        public void TestHappyPath()
        {
            var result = _main.FunctionUnderTest(validInput);
            Assert.AreEqual(expectedOutput, result);
        }

        [Test]
        public void TestEdgeCase()
        {
            var result = _main.FunctionUnderTest(edgeInput);
            Assert.AreEqual(edgeOutput, result);
        }

        [Test]
        public void TestErrorHandling()
        {
            Assert.Throws<ExpectedException>(() => _main.FunctionUnderTest(invalidInput));
        }
    }
    ```
    """
    }
    
    # Get LLM
    llm = get_llm(llm_model)
    
    # Create prompt
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["language", "test_framework", "comment_style", 
                        "generated_code", "design_document", "test_example"]
    )
    
    # Generate test cases
    response = prompt | llm
    test_response = response.invoke({
        "language": lang_config.get('name', language),
        "test_framework": lang_config.get('test_framework', 'generic'),
        "comment_style": lang_config.get('comment_style', '#'),
        "generated_code": state.get('code', ''),
        "design_document": state.get('design_document', {}),
        "test_example": test_examples.get(language, test_examples['python'])
    })
    
    test_cases = test_response.content if hasattr(test_response, "content") else str(test_response)
    
    # Save test files
    test_files = parse_files_with_language(test_cases, language)
    save_files_with_language(test_files, f"test_cases_{language}")
    
    state['test_cases'] = test_cases
    return state

def security_review_enhanced(state: EnhancedState):
    """Enhanced security review with language-specific checks"""
    language = state.get('programming_language', 'python')
    llm_model = state.get('llm_model', Config.DEFAULT_LLM_MODEL)
    
    # Language-specific security concerns
    security_concerns = {
        "python": [
            "SQL injection (raw queries)",
            "Command injection (os.system, subprocess)",
            "Path traversal vulnerabilities",
            "Pickle deserialization",
            "YAML deserialization",
            "Eval/exec usage",
            "Weak cryptography"
        ],
        "javascript": [
            "XSS vulnerabilities",
            "SQL injection",
            "NoSQL injection",
            "Prototype pollution",
            "Insecure dependencies",
            "CORS misconfigurations",
            "JWT vulnerabilities"
        ],
        "java": [
            "SQL injection",
            "XXE (XML External Entity)",
            "Deserialization vulnerabilities",
            "Path traversal",
            "LDAP injection",
            "Weak cryptography",
            "Insecure random number generation"
        ],
        "php": [
            "SQL injection",
            "XSS vulnerabilities",
            "File inclusion vulnerabilities",
            "Command injection",
            "Session fixation",
            "Insecure file uploads",
            "CSRF vulnerabilities"
        ],
        "go": [
            "SQL injection",
            "Command injection",
            "Path traversal",
            "Race conditions",
            "Insecure cryptography",
            "Memory leaks",
            "Goroutine leaks"
        ],
        "csharp": [
            "SQL injection",
            "XSS vulnerabilities",
            "XML injection",
            "Path traversal",
            "Insecure deserialization",
            "Weak cryptography",
            "LDAP injection"
        ],
        "rust": [
            "Memory safety issues",
            "Integer overflow",
            "Unsafe code blocks",
            "Dependency vulnerabilities",
            "Cryptographic weaknesses",
            "Race conditions",
            "Input validation"
        ]
    }
    
    prompt_template = """
    You are a senior cybersecurity expert specializing in {language} application security.

    ### Task: Conduct a thorough security review of the following {language} code:

    **Code:**
    {generated_code}

    ### Language-Specific Security Concerns for {language}:
    {security_checklist}

    ### Security Review Requirements:
    1. Check for common {language} vulnerabilities
    2. Verify input validation and sanitization
    3. Review authentication and authorization implementation
    4. Check for secure coding practices
    5. Identify any hardcoded secrets or credentials
    6. Review error handling for information disclosure
    7. Check dependency security
    8. Analyze {language}-specific security patterns

    ### Provide structured feedback including:
    - Overall security assessment
    - Specific vulnerabilities found (if any)
    - Risk level for each issue (Critical/High/Medium/Low)
    - Remediation recommendations
    - Security best practices for {language}

    Format:
    - Status: Approve / Denied
    - Security Score: X/10
    - Critical Issues: [List any critical issues]
    - Recommendations: [List improvements]
    - Feedback: [Detailed explanation of findings]

    Focus on {language}-specific security patterns and common vulnerabilities.
    """
    
    # Get LLM
    llm = get_llm(llm_model)
    
    # Create prompt
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["language", "generated_code", "security_checklist"]
    )
    
    # Get language-specific security checklist
    checklist = security_concerns.get(language, security_concerns['python'])
    checklist_str = '\n'.join(f"- {concern}" for concern in checklist)
    
    # Run security review
    try:
        from autonomous_features import AutonomousDecisionEngine, AutonomyLevel
        
        # Check if autonomous decision should be made
        if state.get('autonomy_level') != 'manual':
            engine = AutonomousDecisionEngine(
                AutonomyLevel(state.get('autonomy_level', 'semi_auto'))
            )
            decision, metrics, feedback = engine.analyze_security(
                state.get('code', ''), 
                language
            )
            
            # Store quality metrics
            state['quality_metrics'] = state.get('quality_metrics', {})
            state['quality_metrics'].update({
                'security_score': metrics.security_score,
                'overall_score': metrics.overall_score
            })
            
            # If autonomous approval
            if decision == "Approve" and state.get('autonomy_level') in ['full_auto', 'expert_auto']:
                state['security_review_status'] = "Approve"
                state['security_review_feedback'] = f"[AUTONOMOUS] {feedback}"
                state['autonomous_decisions'] = state.get('autonomous_decisions', [])
                state['autonomous_decisions'].append({
                    'stage': 'security_review',
                    'decision': 'Approve',
                    'score': metrics.overall_score,
                    'timestamp': str(datetime.now())
                })
                return state
    except ImportError:
        pass  # Continue with manual review if autonomous features not available
    
    # Manual review or autonomous denial
    response = prompt | llm
    security_response = response.invoke({
        "language": language,
        "generated_code": state.get('code', ''),
        "security_checklist": checklist_str
    })
    
    # Parse response
    response_text = security_response.content if hasattr(security_response, "content") else str(security_response)
    
    # Extract status and feedback (simplified parsing)
    if "Status: Approve" in response_text or "Status: APPROVE" in response_text:
        state['security_review_status'] = "Approve"
    else:
        state['security_review_status'] = "Denied"
    
    state['security_review_feedback'] = response_text
    
    return state

def create_language_specific_project_structure(language: str, project_name: str = "generated_project"):
    """Create a proper project structure for the specified language"""
    lang_config = Config.SUPPORTED_LANGUAGES.get(language, Config.SUPPORTED_LANGUAGES['python'])
    
    project_structures = {
        "python": [
            f"{project_name}/",
            f"{project_name}/main.py",
            f"{project_name}/models/",
            f"{project_name}/models/__init__.py",
            f"{project_name}/services/",
            f"{project_name}/services/__init__.py",
            f"{project_name}/utils/",
            f"{project_name}/utils/__init__.py",
            f"{project_name}/config.py",
            f"{project_name}/requirements.txt",
            f"{project_name}/tests/",
            f"{project_name}/tests/__init__.py",
            f"{project_name}/README.md"
        ],
        "javascript": [
            f"{project_name}/",
            f"{project_name}/index.js",
            f"{project_name}/src/",
            f"{project_name}/src/models/",
            f"{project_name}/src/services/",
            f"{project_name}/src/utils/",
            f"{project_name}/config/",
            f"{project_name}/tests/",
            f"{project_name}/package.json",
            f"{project_name}/.gitignore",
            f"{project_name}/README.md"
        ],
        "java": [
            f"{project_name}/",
            f"{project_name}/src/",
            f"{project_name}/src/main/",
            f"{project_name}/src/main/java/",
            f"{project_name}/src/main/java/com/",
            f"{project_name}/src/main/java/com/example/",
            f"{project_name}/src/main/resources/",
            f"{project_name}/src/test/",
            f"{project_name}/src/test/java/",
            f"{project_name}/pom.xml",
            f"{project_name}/README.md"
        ],
        "go": [
            f"{project_name}/",
            f"{project_name}/main.go",
            f"{project_name}/internal/",
            f"{project_name}/internal/models/",
            f"{project_name}/internal/services/",
            f"{project_name}/internal/utils/",
            f"{project_name}/cmd/",
            f"{project_name}/pkg/",
            f"{project_name}/go.mod",
            f"{project_name}/go.sum",
            f"{project_name}/README.md"
        ],
        "csharp": [
            f"{project_name}/",
            f"{project_name}/{project_name}.csproj",
            f"{project_name}/Program.cs",
            f"{project_name}/Models/",
            f"{project_name}/Services/",
            f"{project_name}/Utils/",
            f"{project_name}/Controllers/",
            f"{project_name}/Tests/",
            f"{project_name}/appsettings.json",
            f"{project_name}/README.md"
        ]
    }
    
    structure = project_structures.get(language, project_structures["python"])
    
    # Create directories
    for path in structure:
        if path.endswith('/'):
            os.makedirs(path, exist_ok=True)
        else:
            # Create directory for file if it doesn't exist
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
    
    return structure

def generate_language_specific_config_files(language: str, project_name: str = "generated_project"):
    """Generate language-specific configuration files"""
    config_templates = {
        "python": {
            "requirements.txt": """# Core dependencies
flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0

# Development dependencies
pytest==7.4.2
black==23.7.0
flake8==6.0.0

# Optional dependencies
sqlalchemy==2.0.21
""",
            "config.py": """import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
""",
            ".env.example": """SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
DEBUG=True
"""
        },
        "javascript": {
            "package.json": f"""{{
  "name": "{project_name}",
  "version": "1.0.0",
  "description": "Generated project",
  "main": "index.js",
  "scripts": {{
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest",
    "lint": "eslint ."
  }},
  "dependencies": {{
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  }},
  "devDependencies": {{
    "jest": "^29.7.0",
    "nodemon": "^3.0.1",
    "eslint": "^8.49.0"
  }}
}}""",
            "config.js": """require('dotenv').config();

module.exports = {
    port: process.env.PORT || 3000,
    nodeEnv: process.env.NODE_ENV || 'development',
    database: {
        url: process.env.DATABASE_URL || 'mongodb://localhost:27017/app'
    },
    jwt: {
        secret: process.env.JWT_SECRET || 'your-jwt-secret'
    }
};
""",
            ".env.example": """PORT=3000
NODE_ENV=development
DATABASE_URL=mongodb://localhost:27017/app
JWT_SECRET=your-jwt-secret-here
"""
        },
        "java": {
            "pom.xml": f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>{project_name}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.1.4</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>"""
        }
    }
    
    templates = config_templates.get(language, {})
    
    for filename, content in templates.items():
        filepath = os.path.join(project_name, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created config file: {filename}")

def create_readme_file(state: EnhancedState, project_name: str = "generated_project"):
    """Create a comprehensive README file for the project"""
    language = state.get('programming_language', 'python')
    lang_config = Config.SUPPORTED_LANGUAGES.get(language, Config.SUPPORTED_LANGUAGES['python'])
    
    readme_content = f"""# {project_name.replace('_', ' ').title()}

Generated by AI SDLC Wizard - Professional Edition

## Overview

{state.get('requirements', 'AI-generated software project')}

## Technology Stack

- **Language:** {lang_config['name']}
- **Test Framework:** {lang_config['test_framework']}
- **Package Manager:** {lang_config['package_manager']}

## Project Structure

```
{project_name}/
├── {lang_config['entry_point']}           # Main application entry point
├── models/                    # Data models
├── services/                  # Business logic
├── utils/                     # Utility functions
├── tests/                     # Test files
├── {lang_config.get('requirements_file', 'requirements.txt')}            # Dependencies
└── README.md                  # This file
```

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   {_get_install_command(language)}
   ```

## Usage

Run the application:
```bash
{_get_run_command(language, lang_config['entry_point'])}
```

## Testing

Run tests:
```bash
{_get_test_command(language, lang_config['test_framework'])}
```

## User Stories

{_format_user_stories(state.get('user_stories', []))}

## Design Document

### Functional Requirements
{_format_design_section(state.get('design_document', {}).get('functional', []))}

### Technical Requirements
{_format_design_section(state.get('design_document', {}).get('technical', []))}

## Generated Files

- **Source Code:** See the main application files
- **Test Cases:** Located in the `tests/` directory
- **Documentation:** This README and inline code comments

## Development

This project was generated using AI SDLC Wizard with the following configuration:
- **LLM Model:** {state.get('llm_model', 'gemma2-9b-it')}
- **Autonomy Level:** {state.get('autonomy_level', 'manual')}
- **Generation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation as needed
4. Run security checks before committing

## License

This project is generated code. Please review and add appropriate licensing.
"""
    
    filepath = os.path.join(project_name, "README.md")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Created README.md")

def _get_install_command(language: str) -> str:
    """Get installation command for language"""
    commands = {
        "python": "pip install -r requirements.txt",
        "javascript": "npm install",
        "typescript": "npm install",
        "java": "mvn install",
        "go": "go mod download",
        "csharp": "dotnet restore",
        "php": "composer install",
        "rust": "cargo build"
    }
    return commands.get(language, "# See language-specific documentation")

def _get_run_command(language: str, entry_point: str) -> str:
    """Get run command for language"""
    commands = {
        "python": f"python {entry_point}",
        "javascript": f"node {entry_point}",
        "typescript": "npm start",
        "java": "mvn exec:java",
        "go": "go run main.go",
        "csharp": "dotnet run",
        "php": f"php {entry_point}",
        "rust": "cargo run"
    }
    return commands.get(language, f"# Run {entry_point}")

def _get_test_command(language: str, test_framework: str) -> str:
    """Get test command for language"""
    commands = {
        "python": "pytest",
        "javascript": "npm test",
        "typescript": "npm test",
        "java": "mvn test",
        "go": "go test ./...",
        "csharp": "dotnet test",
        "php": "phpunit",
        "rust": "cargo test"
    }
    return commands.get(language, f"{test_framework} tests/")

def _format_user_stories(stories: List[str]) -> str:
    """Format user stories for README"""
    if not stories:
        return "No user stories generated."
    
    formatted = []
    for i, story in enumerate(stories, 1):
        formatted.append(f"{i}. {story}")
    
    return '\n'.join(formatted)

def _format_design_section(items: List[str]) -> str:
    """Format design document section"""
    if not items:
        return "Not specified."
    
    formatted = []
    for item in items:
        formatted.append(f"- {item}")
    
    return '\n'.join(formatted)

def validate_language_support(language: str) -> bool:
    """Validate if the language is supported"""
    return language in Config.SUPPORTED_LANGUAGES

def get_supported_languages() -> List[str]:
    """Get list of supported programming languages"""
    return list(Config.SUPPORTED_LANGUAGES.keys())

def create_deployment_script(language: str, project_name: str = "generated_project"):
    """Create deployment script for the specific language"""
    deployment_scripts = {
        "python": f"""#!/bin/bash
# Deployment script for {project_name}

echo "Deploying {project_name}..."

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start application
python main.py
""",
        "javascript": f"""#!/bin/bash
# Deployment script for {project_name}

echo "Deploying {project_name}..."

# Install dependencies
npm install

# Run tests
npm test

# Start application
npm start
""",
        "java": f"""#!/bin/bash
# Deployment script for {project_name}

echo "Deploying {project_name}..."

# Build project
mvn clean compile

# Run tests
mvn test

# Package application
mvn package

# Run application
java -jar target/{project_name}-1.0.0.jar
"""
    }
    
    script_content = deployment_scripts.get(language, f"# Deployment script for {language} not implemented")
    
    script_filename = f"{project_name}/deploy.sh"
    with open(script_filename, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Make script executable
    os.chmod(script_filename, 0o755)
    
    print(f"✅ Created deployment script: deploy.sh")

# Export enhanced functions
__all__ = [
    'EnhancedState',
    'get_llm',
    'get_language_specific_prompt_addon',
    'generate_code_enhanced',
    'write_test_cases_enhanced',
    'security_review_enhanced',
    'parse_files_with_language',
    'save_files_with_language',
    'create_language_specific_project_structure',
    'generate_language_specific_config_files',
    'create_readme_file',
    'validate_language_support',
    'get_supported_languages',
    'create_deployment_script'
]