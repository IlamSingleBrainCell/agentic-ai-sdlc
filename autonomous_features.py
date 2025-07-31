# autonomous_features.py
"""
Autonomous features for the AI SDLC Wizard
Provides automatic decision-making, error recovery, and intelligent workflow management
"""

import streamlit as st
from typing import Dict, Any, List, Tuple, Optional
import json
import re
from datetime import datetime
import time
from dataclasses import dataclass
from enum import Enum
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutonomyLevel(Enum):
    """Levels of automation for the SDLC workflow"""
    MANUAL = "manual"  # All decisions require human approval
    SEMI_AUTO = "semi_auto"  # Critical decisions need approval
    FULL_AUTO = "full_auto"  # Fully autonomous with quality checks
    EXPERT_AUTO = "expert_auto"  # Autonomous with advanced AI reasoning

@dataclass
class QualityMetrics:
    """Quality metrics for autonomous decision making"""
    completeness_score: float  # 0-1
    consistency_score: float   # 0-1
    security_score: float      # 0-1
    best_practices_score: float # 0-1
    overall_score: float       # 0-1
    
    def meets_threshold(self, threshold: float = 0.8) -> bool:
        """Check if quality meets the threshold for autonomous approval"""
        return self.overall_score >= threshold
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for serialization"""
        return {
            "completeness_score": self.completeness_score,
            "consistency_score": self.consistency_score,
            "security_score": self.security_score,
            "best_practices_score": self.best_practices_score,
            "overall_score": self.overall_score
        }

class AutonomousDecisionEngine:
    """Intelligent decision engine for autonomous SDLC workflow"""
    
    def __init__(self, autonomy_level: AutonomyLevel = AutonomyLevel.SEMI_AUTO):
        self.autonomy_level = autonomy_level
        self.decision_history = []
        self.quality_thresholds = {
            AutonomyLevel.MANUAL: 1.0,  # Never auto-approve
            AutonomyLevel.SEMI_AUTO: 0.85,
            AutonomyLevel.FULL_AUTO: 0.75,
            AutonomyLevel.EXPERT_AUTO: 0.70
        }
    
    def analyze_user_stories(self, stories: List[str], requirements: str) -> Tuple[str, QualityMetrics, str]:
        """Analyze user stories for quality and completeness"""
        try:
            # Check completeness
            completeness = self._check_story_completeness(stories)
            
            # Check consistency with requirements
            consistency = self._check_requirements_alignment(stories, requirements)
            
            # Check for best practices
            best_practices = self._check_story_best_practices(stories)
            
            # Calculate overall score
            overall = (completeness + consistency + best_practices) / 3
            
            metrics = QualityMetrics(
                completeness_score=completeness,
                consistency_score=consistency,
                security_score=1.0,  # N/A for user stories
                best_practices_score=best_practices,
                overall_score=overall
            )
            
            # Generate feedback
            feedback = self._generate_story_feedback(metrics, stories)
            
            # Make decision
            decision = "Approve" if metrics.meets_threshold(self.quality_thresholds[self.autonomy_level]) else "Denied"
            
            # Log decision
            self._log_decision("user_stories", decision, metrics, feedback)
            
            return decision, metrics, feedback
            
        except Exception as e:
            logger.error(f"Error in user story analysis: {e}")
            # Fallback to manual review
            return "Denied", QualityMetrics(0.5, 0.5, 1.0, 0.5, 0.5), f"Analysis failed: {str(e)}"
    
    def analyze_design_document(self, design_doc: Dict, stories: List[str]) -> Tuple[str, QualityMetrics, str]:
        """Analyze design document for technical completeness"""
        try:
            functional = design_doc.get('functional', [])
            technical = design_doc.get('technical', [])
            
            # Check completeness
            completeness = self._check_design_completeness(functional, technical)
            
            # Check alignment with user stories
            consistency = self._check_design_story_alignment(design_doc, stories)
            
            # Check technical best practices
            best_practices = self._check_design_best_practices(technical)
            
            # Security considerations
            security = self._check_design_security(technical)
            
            overall = (completeness + consistency + best_practices + security) / 4
            
            metrics = QualityMetrics(
                completeness_score=completeness,
                consistency_score=consistency,
                security_score=security,
                best_practices_score=best_practices,
                overall_score=overall
            )
            
            feedback = self._generate_design_feedback(metrics, design_doc)
            decision = "Approve" if metrics.meets_threshold(self.quality_thresholds[self.autonomy_level]) else "Denied"
            
            self._log_decision("design_document", decision, metrics, feedback)
            
            return decision, metrics, feedback
            
        except Exception as e:
            logger.error(f"Error in design document analysis: {e}")
            return "Denied", QualityMetrics(0.5, 0.5, 0.5, 0.5, 0.5), f"Analysis failed: {str(e)}"
    
    def analyze_code(self, code: str, design_doc: Dict, language: str) -> Tuple[str, QualityMetrics, str]:
        """Analyze generated code for quality and security"""
        try:
            # Language-specific analysis
            if language.lower() == "python":
                metrics = self._analyze_python_code(code, design_doc)
            elif language.lower() in ["javascript", "typescript"]:
                metrics = self._analyze_javascript_code(code, design_doc)
            elif language.lower() == "java":
                metrics = self._analyze_java_code(code, design_doc)
            else:
                # Generic analysis for other languages
                metrics = self._analyze_generic_code(code, design_doc)
            
            feedback = self._generate_code_feedback(metrics, code, language)
            decision = "Approve" if metrics.meets_threshold(self.quality_thresholds[self.autonomy_level]) else "Denied"
            
            self._log_decision("code_review", decision, metrics, feedback)
            
            return decision, metrics, feedback
            
        except Exception as e:
            logger.error(f"Error in code analysis: {e}")
            return "Denied", QualityMetrics(0.5, 0.5, 0.5, 0.5, 0.5), f"Analysis failed: {str(e)}"
    
    def analyze_security(self, code: str, language: str) -> Tuple[str, QualityMetrics, str]:
        """Perform security analysis on code"""
        try:
            # Common security checks
            vulnerabilities = self._check_common_vulnerabilities(code, language)
            
            # Authentication & authorization
            auth_score = self._check_auth_implementation(code)
            
            # Input validation
            validation_score = self._check_input_validation(code)
            
            # Encryption and data protection
            encryption_score = self._check_encryption(code)
            
            security_score = max(0.0, 1.0 - (vulnerabilities * 0.1))  # Deduct for each vulnerability
            overall = (security_score + auth_score + validation_score + encryption_score) / 4
            
            metrics = QualityMetrics(
                completeness_score=1.0,
                consistency_score=1.0,
                security_score=security_score,
                best_practices_score=overall,
                overall_score=overall
            )
            
            feedback = self._generate_security_feedback(metrics, code, vulnerabilities)
            decision = "Approve" if metrics.meets_threshold(self.quality_thresholds[self.autonomy_level]) else "Denied"
            
            self._log_decision("security_review", decision, metrics, feedback)
            
            return decision, metrics, feedback
            
        except Exception as e:
            logger.error(f"Error in security analysis: {e}")
            return "Denied", QualityMetrics(0.5, 0.5, 0.5, 0.5, 0.5), f"Security analysis failed: {str(e)}"
    
    def analyze_test_cases(self, test_cases: str, code: str) -> Tuple[str, QualityMetrics, str]:
        """Analyze test cases for coverage and quality"""
        try:
            # Check test coverage
            coverage = self._estimate_test_coverage(test_cases, code)
            
            # Check test quality
            quality = self._check_test_quality(test_cases)
            
            # Check test types (unit, integration, e2e)
            test_types = self._check_test_types(test_cases)
            
            # Best practices
            best_practices = self._check_test_best_practices(test_cases)
            
            overall = (coverage + quality + test_types + best_practices) / 4
            
            metrics = QualityMetrics(
                completeness_score=coverage,
                consistency_score=quality,
                security_score=1.0,  # N/A for test cases
                best_practices_score=best_practices,
                overall_score=overall
            )
            
            feedback = self._generate_test_feedback(metrics, test_cases)
            decision = "Approve" if metrics.meets_threshold(self.quality_thresholds[self.autonomy_level]) else "Denied"
            
            self._log_decision("test_cases", decision, metrics, feedback)
            
            return decision, metrics, feedback
            
        except Exception as e:
            logger.error(f"Error in test case analysis: {e}")
            return "Denied", QualityMetrics(0.5, 0.5, 1.0, 0.5, 0.5), f"Test analysis failed: {str(e)}"
    
    def analyze_qa_results(self, qa_feedback: str, test_cases: str) -> Tuple[str, QualityMetrics, str]:
        """Analyze QA testing results"""
        try:
            # Parse QA results
            passed_tests = qa_feedback.lower().count("passed")
            failed_tests = qa_feedback.lower().count("failed")
            total_tests = passed_tests + failed_tests
            
            if total_tests == 0:
                test_pass_rate = 0.5  # Default if no clear results
            else:
                test_pass_rate = passed_tests / total_tests
            
            # Check for critical failures
            critical_failures = self._check_critical_failures(qa_feedback)
            
            # Performance indicators
            performance = self._check_performance_indicators(qa_feedback)
            
            overall = (test_pass_rate + (1.0 - critical_failures * 0.2) + performance) / 3
            
            metrics = QualityMetrics(
                completeness_score=test_pass_rate,
                consistency_score=1.0,
                security_score=1.0,
                best_practices_score=performance,
                overall_score=overall
            )
            
            feedback = self._generate_qa_feedback(metrics, qa_feedback)
            decision = "Approve" if metrics.meets_threshold(self.quality_thresholds[self.autonomy_level]) else "Denied"
            
            self._log_decision("qa_review", decision, metrics, feedback)
            
            return decision, metrics, feedback
            
        except Exception as e:
            logger.error(f"Error in QA analysis: {e}")
            return "Denied", QualityMetrics(0.5, 1.0, 1.0, 0.5, 0.5), f"QA analysis failed: {str(e)}"
    
    def _log_decision(self, stage: str, decision: str, metrics: QualityMetrics, feedback: str):
        """Log autonomous decision for tracking"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "decision": decision,
            "metrics": metrics.to_dict(),
            "feedback": feedback,
            "autonomy_level": self.autonomy_level.value
        }
        
        self.decision_history.append(decision_record)
        logger.info(f"Autonomous decision: {stage} -> {decision} (score: {metrics.overall_score:.2f})")
    
    # Helper methods for analysis (implementation details)
    def _check_story_completeness(self, stories: List[str]) -> float:
        """Check if user stories follow the standard format"""
        if not stories:
            return 0.0
        
        complete_stories = 0
        for story in stories:
            # Check for standard user story format
            has_as_a = "as a" in story.lower()
            has_i_want = "i want" in story.lower()
            has_so_that = "so that" in story.lower()
            
            if has_as_a and has_i_want and has_so_that:
                complete_stories += 1
            elif has_as_a and has_i_want:  # Partial credit
                complete_stories += 0.7
            elif any([has_as_a, has_i_want, has_so_that]):  # Minimal credit
                complete_stories += 0.3
        
        return complete_stories / len(stories)
    
    def _check_requirements_alignment(self, stories: List[str], requirements: str) -> float:
        """Check how well stories align with requirements"""
        if not requirements or not stories:
            return 0.0
        
        # Extract keywords from requirements
        req_keywords = set(re.findall(r'\b\w{4,}\b', requirements.lower()))
        req_keywords = {word for word in req_keywords if word not in {'that', 'with', 'have', 'will', 'this', 'from', 'they'}}
        
        # Extract keywords from stories
        story_keywords = set()
        for story in stories:
            story_words = set(re.findall(r'\b\w{4,}\b', story.lower()))
            story_keywords.update(story_words)
        
        if not req_keywords:
            return 0.5  # Default if no meaningful keywords
        
        # Calculate alignment
        common_keywords = req_keywords.intersection(story_keywords)
        alignment_score = len(common_keywords) / len(req_keywords)
        
        return min(1.0, alignment_score)
    
    def _check_story_best_practices(self, stories: List[str]) -> float:
        """Check if stories follow best practices"""
        if not stories:
            return 0.0
        
        score = 1.0
        
        # Check story length and clarity
        for story in stories:
            word_count = len(story.split())
            if word_count < 8:
                score -= 0.1  # Too short
            elif word_count > 60:
                score -= 0.1  # Too long
        
        # Check for uniqueness
        unique_stories = len(set(stories))
        if unique_stories < len(stories):
            score -= 0.2  # Duplicate stories
        
        # Check for testability indicators
        testable_indicators = ['validate', 'verify', 'ensure', 'check', 'confirm']
        testable_count = 0
        for story in stories:
            if any(indicator in story.lower() for indicator in testable_indicators):
                testable_count += 1
        
        if testable_count < len(stories) * 0.3:  # At least 30% should be testable
            score -= 0.15
        
        return max(0.0, score)
    
    def _check_design_completeness(self, functional: List[str], technical: List[str]) -> float:
        """Check design document completeness"""
        score = 0.0
        
        # Functional requirements scoring
        if len(functional) >= 5:
            score += 0.5
        elif len(functional) >= 3:
            score += 0.35
        else:
            score += len(functional) * 0.1
        
        # Technical requirements scoring
        if len(technical) >= 5:
            score += 0.5
        elif len(technical) >= 3:
            score += 0.35
        else:
            score += len(technical) * 0.1
        
        return min(1.0, score)
    
    def _check_design_story_alignment(self, design_doc: Dict, stories: List[str]) -> float:
        """Check if design covers all user stories"""
        if not stories:
            return 1.0
        
        covered_stories = 0
        all_design_text = ' '.join(
            design_doc.get('functional', []) + 
            design_doc.get('technical', []) +
            design_doc.get('assumptions', [])
        ).lower()
        
        for story in stories:
            # Extract key concepts from story
            key_parts = re.findall(r'\b\w{4,}\b', story.lower())
            key_parts = [part for part in key_parts if part not in {'that', 'with', 'have', 'will', 'want'}]
            
            # Check if at least 2 key parts are mentioned in design
            matches = sum(1 for part in key_parts if part in all_design_text)
            if matches >= 2 or (len(key_parts) <= 2 and matches >= 1):
                covered_stories += 1
        
        return covered_stories / len(stories)
    
    def _check_design_best_practices(self, technical: List[str]) -> float:
        """Check if design follows technical best practices"""
        if not technical:
            return 0.3  # Base score for minimal technical requirements
        
        score = 0.0
        tech_text = ' '.join(technical).lower()
        
        # Check for important technical considerations
        technical_aspects = {
            'api': ['api', 'endpoint', 'rest', 'graphql'],
            'database': ['database', 'data model', 'schema', 'storage'],
            'security': ['security', 'authentication', 'authorization', 'encryption'],
            'scalability': ['scalability', 'performance', 'load', 'cache'],
            'error_handling': ['error handling', 'exception', 'validation', 'logging'],
            'testing': ['test', 'testing', 'quality', 'validation'],
            'deployment': ['deployment', 'docker', 'cloud', 'infrastructure']
        }
        
        for aspect, keywords in technical_aspects.items():
            if any(keyword in tech_text for keyword in keywords):
                score += 0.14  # Each aspect is worth ~14% (7 aspects = ~100%)
        
        return min(1.0, score)
    
    def _check_design_security(self, technical: List[str]) -> float:
        """Check security considerations in design"""
        score = 0.4  # Base score
        
        if not technical:
            return score
        
        tech_text = ' '.join(technical).lower()
        
        security_keywords = [
            'authentication', 'authorization', 'encryption', 'validation',
            'sanitization', 'ssl', 'https', 'token', 'security', 'access control'
        ]
        
        for keyword in security_keywords:
            if keyword in tech_text:
                score += 0.06  # Each keyword adds 6%
        
        return min(1.0, score)
    
    def _analyze_python_code(self, code: str, design_doc: Dict) -> QualityMetrics:
        """Python-specific code analysis"""
        lines = code.split('\n')
        
        # Check for proper structure
        has_imports = any(line.strip().startswith(('import ', 'from ')) for line in lines)
        has_functions = 'def ' in code
        has_classes = 'class ' in code
        has_main = '__main__' in code or 'if __name__' in code
        
        structure_score = sum([has_imports, has_functions or has_classes, has_main]) / 3
        
        # Check for error handling
        has_try_except = 'try:' in code and 'except' in code
        has_logging = 'logging' in code or 'logger' in code
        error_score = (int(has_try_except) + int(has_logging)) / 2
        
        # Check for documentation
        has_docstrings = '"""' in code or "'''" in code
        has_comments = any(line.strip().startswith('#') for line in lines)
        doc_score = (int(has_docstrings) + int(has_comments)) / 2
        
        # Security checks
        security_issues = 0
        dangerous_patterns = [
            r'eval\s*\(',
            r'exec\s*\(',
            r'os\.system\s*\(',
            r'subprocess\.call\s*\(',
            r'password\s*=\s*["\'][^"\']*["\']',
            r'secret\s*=\s*["\'][^"\']*["\']'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                security_issues += 1
        
        security_score = max(0.0, 1.0 - (security_issues * 0.2))
        
        overall = (structure_score + error_score + doc_score + security_score) / 4
        
        return QualityMetrics(
            completeness_score=structure_score,
            consistency_score=doc_score,
            security_score=security_score,
            best_practices_score=error_score,
            overall_score=overall
        )
    
    def _analyze_javascript_code(self, code: str, design_doc: Dict) -> QualityMetrics:
        """JavaScript/TypeScript specific code analysis"""
        # Modern JavaScript practices
        has_const_let = 'const ' in code or 'let ' in code
        avoids_var = code.count('var ') == 0 or code.count('var ') < 3
        has_functions = 'function ' in code or '=>' in code
        has_classes = 'class ' in code
        has_modules = 'export ' in code or 'module.exports' in code
        
        structure_score = sum([has_const_let, has_functions, avoids_var]) / 3
        
        # Error handling
        has_try_catch = 'try {' in code and 'catch' in code
        has_promises = '.then(' in code or 'async' in code or 'await' in code
        error_score = (int(has_try_catch) + int(has_promises)) / 2
        
        # Documentation
        has_jsdoc = '/**' in code
        has_comments = '//' in code
        doc_score = (int(has_jsdoc) + int(has_comments)) / 2
        
        # Security checks
        security_issues = 0
        dangerous_patterns = [
            r'eval\s*\(',
            r'innerHTML\s*=',
            r'document\.write\s*\(',
            r'setTimeout\s*\(\s*["\']',
            r'setInterval\s*\(\s*["\']'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                security_issues += 1
        
        # Check for sanitization when using innerHTML
        if 'innerHTML' in code and 'sanitize' not in code.lower():
            security_issues += 1
        
        security_score = max(0.0, 1.0 - (security_issues * 0.25))
        
        overall = (structure_score + error_score + doc_score + security_score) / 4
        
        return QualityMetrics(
            completeness_score=structure_score,
            consistency_score=doc_score,
            security_score=security_score,
            best_practices_score=error_score,
            overall_score=overall
        )
    
    def _analyze_java_code(self, code: str, design_doc: Dict) -> QualityMetrics:
        """Java-specific code analysis"""
        has_package = 'package ' in code
        has_classes = 'public class ' in code or 'class ' in code
        has_main = 'public static void main' in code
        has_imports = 'import ' in code
        
        structure_score = sum([has_package, has_classes, has_imports]) / 3
        
        # Error handling
        has_try_catch = 'try {' in code and 'catch' in code
        has_throws = 'throws ' in code
        error_score = (int(has_try_catch) + int(has_throws)) / 2
        
        # Documentation
        has_javadoc = '/**' in code
        has_comments = '//' in code
        doc_score = (int(has_javadoc) + int(has_comments)) / 2
        
        # Security
        security_score = 0.7  # Base score
        if 'PreparedStatement' in code:
            security_score += 0.2  # Good for SQL injection prevention
        if 'MessageDigest' in code or 'SecureRandom' in code:
            security_score += 0.1  # Secure cryptography
        
        overall = (structure_score + error_score + doc_score + security_score) / 4
        
        return QualityMetrics(
            completeness_score=structure_score,
            consistency_score=doc_score,
            security_score=security_score,
            best_practices_score=error_score,
            overall_score=overall
        )
    
    def _analyze_generic_code(self, code: str, design_doc: Dict) -> QualityMetrics:
        """Generic code analysis for any language"""
        lines = code.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        
        # Basic structure check
        structure_score = min(1.0, len(non_empty_lines) / 30)  # At least 30 lines for good structure
        
        # Comments check
        comment_patterns = [r'#.*', r'//.*', r'/\*.*?\*/', r'<!--.*?-->']
        comment_lines = 0
        for line in lines:
            for pattern in comment_patterns:
                if re.search(pattern, line):
                    comment_lines += 1
                    break
        
        doc_score = min(1.0, comment_lines / max(1, len(non_empty_lines) * 0.1))  # 10% comments is good
        
        # Generic security check
        security_issues = 0
        suspicious_patterns = [
            r'password\s*=\s*["\'][^"\']*["\']',
            r'secret\s*=\s*["\'][^"\']*["\']',
            r'key\s*=\s*["\'][^"\']*["\']',
            r'token\s*=\s*["\'][^"\']*["\']'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                security_issues += 1
        
        security_score = max(0.0, 1.0 - (security_issues * 0.25))
        
        overall = (structure_score + doc_score + security_score) / 3
        
        return QualityMetrics(
            completeness_score=structure_score,
            consistency_score=doc_score,
            security_score=security_score,
            best_practices_score=0.7,  # Default for unknown language
            overall_score=overall
        )
    
    def _check_common_vulnerabilities(self, code: str, language: str) -> int:
        """Check for common security vulnerabilities"""
        vulnerabilities = 0
        
        # SQL Injection patterns
        sql_patterns = [
            r'(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']',
            r'query.*%.*["\']',
            r'execute.*%.*["\']'
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                vulnerabilities += 1
                break  # Count as one vulnerability type
        
        # Command Injection
        dangerous_functions = {
            'python': [r'os\.system\s*\(', r'subprocess\.call\s*\(', r'eval\s*\(', r'exec\s*\('],
            'javascript': [r'eval\s*\(', r'Function\s*\(', r'setTimeout\s*\(\s*["\']', r'setInterval\s*\(\s*["\']'],
            'java': [r'Runtime\.exec\s*\(', r'ProcessBuilder\s*\('],
            'php': [r'eval\s*\(', r'exec\s*\(', r'system\s*\(', r'shell_exec\s*\('],
            'go': [r'exec\.Command\s*\(', r'os\.Exec\s*\('],
            'csharp': [r'Process\.Start\s*\(', r'System\.Diagnostics\.Process']
        }
        
        lang_functions = dangerous_functions.get(language.lower(), [])
        for pattern in lang_functions:
            if re.search(pattern, code):
                vulnerabilities += 1
        
        # XSS patterns (for web languages)
        if language.lower() in ['javascript', 'typescript', 'php']:
            xss_patterns = [r'innerHTML\s*=', r'document\.write\s*\(', r'echo\s+\$_']
            for pattern in xss_patterns:
                if re.search(pattern, code) and 'sanitize' not in code.lower():
                    vulnerabilities += 1
                    break
        
        return vulnerabilities
    
    def _check_auth_implementation(self, code: str) -> float:
        """Check authentication implementation"""
        auth_keywords = [
            'authenticate', 'authorization', 'login', 'token', 
            'session', 'jwt', 'auth', 'password', 'credential'
        ]
        auth_score = 0.3  # Base score
        
        code_lower = code.lower()
        for keyword in auth_keywords:
            if keyword in code_lower:
                auth_score += 0.1
        
        # Bonus for secure auth patterns
        secure_patterns = ['bcrypt', 'hash', 'salt', 'pepper', 'scrypt', 'argon2']
        for pattern in secure_patterns:
            if pattern in code_lower:
                auth_score += 0.1
        
        return min(1.0, auth_score)
    
    def _check_input_validation(self, code: str) -> float:
        """Check input validation practices"""
        validation_keywords = [
            'validate', 'sanitize', 'escape', 'filter', 'check',
            'verify', 'clean', 'strip', 'trim', 'regex'
        ]
        validation_score = 0.3  # Base score
        
        code_lower = code.lower()
        for keyword in validation_keywords:
            if keyword in code_lower:
                validation_score += 0.1
        
        # Check for specific validation patterns
        validation_patterns = [
            r'if\s+.*\s+(len|length)\s*\(',  # Length validation
            r'isinstance\s*\(',               # Type validation
            r'match\s*\(',                    # Regex validation
            r'in\s+\[.*\]',                   # Whitelist validation
        ]
        
        for pattern in validation_patterns:
            if re.search(pattern, code):
                validation_score += 0.05
        
        return min(1.0, validation_score)
    
    def _check_encryption(self, code: str) -> float:
        """Check encryption usage"""
        encryption_keywords = [
            'encrypt', 'decrypt', 'hash', 'bcrypt', 'sha', 'aes', 
            'ssl', 'tls', 'https', 'crypto', 'cipher'
        ]
        encryption_score = 0.5  # Base score
        
        code_lower = code.lower()
        for keyword in encryption_keywords:
            if keyword in code_lower:
                encryption_score += 0.08
        
        return min(1.0, encryption_score)
    
    def _estimate_test_coverage(self, test_cases: str, code: str) -> float:
        """Estimate test coverage based on test cases and code"""
        if not test_cases or not code:
            return 0.0
        
        # Count functions/methods in code
        function_patterns = [
            r'def\s+\w+',      # Python
            r'function\s+\w+', # JavaScript
            r'public\s+\w+',   # Java/C#
            r'func\s+\w+'      # Go
        ]
        
        function_count = 0
        for pattern in function_patterns:
            function_count += len(re.findall(pattern, code))
        
        # Count test cases
        test_count = max(
            test_cases.count('[Test Case Name]'),
            test_cases.count('def test_'),
            test_cases.count('test('),
            test_cases.count('@Test')
        )
        
        if function_count == 0:
            return 0.5 if test_count > 0 else 0.0
        
        # Estimate coverage (2-3 tests per function is good)
        coverage_ratio = test_count / (function_count * 2.5)
        return min(1.0, coverage_ratio)
    
    def _check_test_quality(self, test_cases: str) -> float:
        """Check quality of test cases"""
        if not test_cases:
            return 0.0
        
        quality_score = 0.0
        
        # Check for test structure elements
        structure_elements = [
            ('[Test Steps]', 0.2),
            ('[Expected Result]', 0.2),
            ('[Test Type]', 0.15),
            ('[Description]', 0.15),
            ('assert', 0.15),
            ('expect', 0.15)
        ]
        
        for element, weight in structure_elements:
            if element in test_cases:
                quality_score += weight
        
        return min(1.0, quality_score)
    
    def _check_test_types(self, test_cases: str) -> float:
        """Check variety of test types"""
        test_types = ['unit', 'integration', 'e2e', 'performance', 'security', 'negative', 'edge']
        found_types = sum(1 for t in test_types if t in test_cases.lower())
        
        return min(1.0, found_types / 4)  # Having 4+ types is excellent
    
    def _check_test_best_practices(self, test_cases: str) -> float:
        """Check if tests follow best practices"""
        score = 0.4  # Base score
        
        test_cases_lower = test_cases.lower()
        
        # Check for important testing practices
        practices = [
            ('edge', 0.15),      # Edge case testing
            ('boundary', 0.15),   # Boundary testing
            ('negative', 0.15),   # Negative testing
            ('invalid', 0.1),     # Invalid input testing
            ('setup', 0.1),       # Test setup
            ('teardown', 0.1),    # Test cleanup
            ('mock', 0.1),        # Mocking
            ('stub', 0.1)         # Stubbing
        ]
        
        for practice, weight in practices:
            if practice in test_cases_lower:
                score += weight
        
        return min(1.0, score)
    
    def _check_critical_failures(self, qa_feedback: str) -> int:
        """Check for critical failures in QA"""
        critical_keywords = [
            'crash', 'critical', 'blocker', 'security breach', 
            'data loss', 'corruption', 'severe', 'fatal'
        ]
        failures = 0
        
        qa_lower = qa_feedback.lower()
        for keyword in critical_keywords:
            if keyword in qa_lower:
                failures += 1
        
        return failures
    
    def _check_performance_indicators(self, qa_feedback: str) -> float:
        """Check performance indicators in QA feedback"""
        performance_score = 0.6  # Base score
        
        qa_lower = qa_feedback.lower()
        
        # Positive indicators
        positive_indicators = ['fast', 'quick', 'responsive', 'efficient', 'optimized']
        for indicator in positive_indicators:
            if indicator in qa_lower:
                performance_score += 0.08
        
        # Negative indicators
        negative_indicators = ['slow', 'timeout', 'lag', 'delay', 'bottleneck', 'memory leak']
        for indicator in negative_indicators:
            if indicator in qa_lower:
                performance_score -= 0.15
        
        return max(0.0, min(1.0, performance_score))
    
    # Feedback generation methods
    def _generate_story_feedback(self, metrics: QualityMetrics, stories: List[str]) -> str:
        """Generate feedback for user stories"""
        feedback = []
        
        if metrics.completeness_score < 0.7:
            feedback.append("Some user stories are missing the standard 'As a... I want... So that...' format")
        
        if metrics.consistency_score < 0.7:
            feedback.append("User stories could better align with the stated requirements")
        
        if metrics.best_practices_score < 0.7:
            feedback.append("Consider making stories more concise, unique, and testable")
        
        if metrics.overall_score >= 0.9:
            feedback.append("Excellent user stories! Well-structured and comprehensive")
        elif metrics.overall_score >= 0.75:
            feedback.append("Good user stories with minor improvements needed")
        
        return ". ".join(feedback) if feedback else "User stories meet quality standards"
    
    def _generate_design_feedback(self, metrics: QualityMetrics, design_doc: Dict) -> str:
        """Generate feedback for design document"""
        feedback = []
        
        if metrics.completeness_score < 0.7:
            feedback.append("Design document needs more detail in functional or technical specifications")
        
        if metrics.consistency_score < 0.7:
            feedback.append("Ensure all user stories are addressed in the design")
        
        if metrics.security_score < 0.7:
            feedback.append("Add more security considerations (authentication, encryption, access control)")
        
        if metrics.best_practices_score < 0.7:
            feedback.append("Include more technical best practices (APIs, database design, error handling)")
        
        if metrics.overall_score >= 0.9:
            feedback.append("Comprehensive design document with excellent technical depth")
        elif metrics.overall_score >= 0.75:
            feedback.append("Good design document with solid technical foundation")
        
        return ". ".join(feedback) if feedback else "Design document meets technical standards"
    
    def _generate_code_feedback(self, metrics: QualityMetrics, code: str, language: str) -> str:
        """Generate feedback for code"""
        feedback = []
        
        if metrics.completeness_score < 0.7:
            feedback.append(f"Code structure could be improved for {language} best practices")
        
        if metrics.security_score < 0.7:
            feedback.append("Security vulnerabilities detected - review input validation and avoid dangerous functions")
        
        if metrics.best_practices_score < 0.7:
            feedback.append("Add more error handling, logging, and defensive programming practices")
        
        if metrics.consistency_score < 0.7:
            feedback.append("Improve code documentation and comments for better maintainability")
        
        if metrics.overall_score >= 0.9:
            feedback.append(f"High-quality {language} code following excellent practices")
        elif metrics.overall_score >= 0.75:
            feedback.append(f"Good {language} code with solid structure and practices")
        
        return ". ".join(feedback) if feedback else f"Code meets {language} quality standards"
    
    def _generate_test_feedback(self, metrics: QualityMetrics, test_cases: str) -> str:
        """Generate feedback for test cases"""
        feedback = []
        
        if metrics.completeness_score < 0.7:
            feedback.append("Test coverage could be improved - add more test cases for better coverage")
        
        if metrics.consistency_score < 0.7:
            feedback.append("Ensure test cases have complete structure (steps, expected results, descriptions)")
        
        if metrics.best_practices_score < 0.7:
            feedback.append("Add more edge cases, negative tests, and boundary condition testing")
        
        if metrics.overall_score >= 0.9:
            feedback.append("Comprehensive test suite with excellent coverage and quality")
        elif metrics.overall_score >= 0.75:
            feedback.append("Good test suite with solid coverage")
        
        return ". ".join(feedback) if feedback else "Test cases are well-designed and comprehensive"
    
    def _generate_security_feedback(self, metrics: QualityMetrics, code: str, vulnerabilities: int) -> str:
        """Generate security feedback"""
        feedback = []
        
        if vulnerabilities > 0:
            feedback.append(f"Found {vulnerabilities} potential security vulnerabilities that need attention")
        
        if metrics.security_score < 0.7:
            feedback.append("Implement proper input validation, sanitization, and secure coding practices")
        
        if metrics.overall_score < 0.6:
            feedback.append("Critical security improvements needed before deployment")
        elif metrics.overall_score >= 0.9:
            feedback.append("Code follows security best practices with minimal risk")
        elif metrics.overall_score >= 0.75:
            feedback.append("Good security posture with minor improvements needed")
        
        return ". ".join(feedback) if feedback else "Security review passed with acceptable risk level"
    
    def _generate_qa_feedback(self, metrics: QualityMetrics, qa_feedback: str) -> str:
        """Generate QA feedback"""
        feedback = []
        
        if metrics.completeness_score < 0.7:
            feedback.append("Some tests are failing - review and fix issues before deployment")
        
        if metrics.best_practices_score < 0.7:
            feedback.append("Performance issues detected - optimization recommended")
        
        if metrics.overall_score >= 0.9:
            feedback.append("All tests passing with excellent performance metrics")
        elif metrics.overall_score >= 0.75:
            feedback.append("Most tests passing with good overall quality")
        
        return ". ".join(feedback) if feedback else "QA validation completed successfully"


class ErrorRecoveryEngine:
    """Handles errors and provides recovery strategies"""
    
    def __init__(self):
        self.error_history = []
        self.recovery_strategies = {
            "api_error": self._recover_from_api_error,
            "validation_error": self._recover_from_validation_error,
            "generation_error": self._recover_from_generation_error,
            "timeout_error": self._recover_from_timeout_error,
            "import_error": self._recover_from_import_error,
            "workflow_error": self._recover_from_workflow_error
        }
    
    def handle_error(self, error_type: str, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Handle errors and attempt recovery"""
        error_record = {
            "type": error_type,
            "details": error_details,
            "timestamp": datetime.now(),
            "state_stage": state.get("active_node", "unknown")
        }
        
        self.error_history.append(error_record)
        logger.error(f"Error occurred: {error_type} - {error_details}")
        
        if error_type in self.recovery_strategies:
            return self.recovery_strategies[error_type](error_details, state)
        else:
            return self._generic_recovery(error_details, state)
    
    def _recover_from_api_error(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Recover from API errors"""
        retry_count = error_details.get("retry_count", 0)
        
        if retry_count < 3:
            wait_time = min(2 ** retry_count, 10)  # Exponential backoff, max 10 seconds
            time.sleep(wait_time)
            error_details["retry_count"] = retry_count + 1
            return True, {"action": "retry", "wait_time": wait_time, "attempt": retry_count + 1}
        else:
            # Switch to a different model if available
            fallback_models = ["gemma2-9b-it", "llama-3.1-70b-versatile"]
            current_model = state.get("llm_model", "gemma2-9b-it")
            
            for model in fallback_models:
                if model != current_model:
                    return True, {"action": "switch_model", "fallback_model": model}
            
            return False, {"action": "manual_intervention", "message": "All API retry attempts failed"}
    
    def _recover_from_validation_error(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Recover from validation errors"""
        return True, {
            "action": "enhance_prompt",
            "suggestions": [
                "Add more specific requirements and examples",
                "Include technical constraints and preferences",
                "Break down complex requirements into smaller parts",
                "Specify user roles and personas more clearly"
            ]
        }
    
    def _recover_from_generation_error(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Recover from generation errors"""
        return True, {
            "action": "simplify_and_retry",
            "strategy": "break_into_smaller_parts",
            "suggestion": "Try reducing the scope or complexity of the current stage"
        }
    
    def _recover_from_timeout_error(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Recover from timeout errors"""
        return True, {
            "action": "increase_timeout_and_retry",
            "new_timeout": min(180, error_details.get("timeout", 60) * 2),  # Double timeout, max 3 minutes
            "suggestion": "Using longer timeout for complex operations"
        }
    
    def _recover_from_import_error(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Recover from import errors"""
        missing_module = error_details.get("module", "unknown")
        return True, {
            "action": "install_dependency",
            "module": missing_module,
            "suggestion": f"Install missing dependency: {missing_module}"
        }
    
    def _recover_from_workflow_error(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Recover from workflow errors"""
        return True, {
            "action": "reset_stage",
            "suggestion": "Reset current stage and try again with simplified parameters"
        }
    
    def _generic_recovery(self, error_details: Dict[str, Any], state: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Generic recovery strategy"""
        return True, {
            "action": "manual_intervention",
            "message": "An unexpected error occurred. Manual review and intervention recommended.",
            "details": str(error_details)
        }
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors encountered"""
        if not self.error_history:
            return {"total_errors": 0, "error_types": {}, "last_error": None}
        
        error_types = {}
        for error in self.error_history:
            error_type = error["type"]
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "error_types": error_types,
            "last_error": self.error_history[-1],
            "recovery_rate": len([e for e in self.error_history if e.get("recovered", False)]) / len(self.error_history)
        }


class WorkflowOptimizer:
    """Optimizes workflow based on historical data and patterns"""
    
    def __init__(self):
        self.performance_history = []
        self.optimization_rules = []
        self.user_patterns = {}
    
    def analyze_workflow_performance(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow performance and suggest optimizations"""
        duration = workflow_data.get("duration", 0)
        iterations = workflow_data.get("iterations", 0)
        errors = workflow_data.get("errors", 0)
        autonomous_decisions = workflow_data.get("autonomous_decisions", 0)
        
        # Calculate performance score
        performance_score = self._calculate_performance_score(duration, iterations, errors, autonomous_decisions)
        
        # Generate optimization suggestions
        suggestions = self._generate_optimization_suggestions(workflow_data)
        
        # Store in history
        performance_record = {
            "timestamp": datetime.now(),
            "score": performance_score,
            "data": workflow_data,
            "suggestions_count": len(suggestions)
        }
        
        self.performance_history.append(performance_record)
        
        # Keep only last 50 records
        if len(self.performance_history) > 50:
            self.performance_history = self.performance_history[-50:]
        
        return {
            "performance_score": performance_score,
            "suggestions": suggestions,
            "trend": self._calculate_trend(),
            "efficiency_rating": self._get_efficiency_rating(performance_score)
        }
    
    def _calculate_performance_score(self, duration: float, iterations: int, errors: int, autonomous_decisions: int) -> float:
        """Calculate overall performance score"""
        # Lower duration is better (normalize to 0-1, assuming 1 hour baseline)
        duration_score = max(0.0, 1.0 - (duration / 3600))
        
        # Fewer iterations is better (normalize to 0-1, assuming 5 iterations baseline)
        iteration_score = max(0.0, 1.0 - (iterations / 5))
        
        # No errors is best (normalize to 0-1, assuming 3 errors baseline)
        error_score = max(0.0, 1.0 - (errors / 3))
        
        # More autonomous decisions is generally better for efficiency
        autonomy_bonus = min(0.2, autonomous_decisions * 0.05)  # Up to 20% bonus
        
        base_score = (duration_score + iteration_score + error_score) / 3
        final_score = min(1.0, base_score + autonomy_bonus)
        
        return final_score
    
    def _generate_optimization_suggestions(self, workflow_data: Dict[str, Any]) -> List[str]:
        """Generate optimization suggestions based on workflow data"""
        suggestions = []
        
        iterations = workflow_data.get("iterations", 0)
        errors = workflow_data.get("errors", 0)
        duration = workflow_data.get("duration", 0)
        autonomous_decisions = workflow_data.get("autonomous_decisions", 0)
        
        # Iteration-based suggestions
        if iterations > 3:
            suggestions.append("Consider providing more detailed initial requirements to reduce iterations")
            suggestions.append("Use requirement templates for common project types")
        
        # Error-based suggestions  
        if errors > 2:
            suggestions.append("Enable error recovery features to handle common issues automatically")
            suggestions.append("Check your GROQ API key and network connection")
        
        # Duration-based suggestions
        if duration > 1800:  # 30 minutes
            suggestions.append("Consider enabling higher autonomy levels to speed up routine decisions")
            suggestions.append("Use more powerful AI models for complex analysis")
        
        # Autonomy-based suggestions
        if autonomous_decisions == 0 and iterations > 1:
            suggestions.append("Try semi-autonomous mode to auto-approve high-quality outputs")
        
        # Model-specific suggestions
        current_model = workflow_data.get("llm_model", "")
        if "gemma" in current_model.lower() and duration > 900:  # 15 minutes
            suggestions.append("Consider upgrading to Llama 3.1 70B for better performance on complex tasks")
        
        return suggestions[:4]  # Limit to 4 most relevant suggestions
    
    def _calculate_trend(self) -> str:
        """Calculate performance trend"""
        if len(self.performance_history) < 3:
            return "insufficient_data"
        
        # Get recent scores (last 5 or all if less than 5)
        recent_count = min(5, len(self.performance_history))
        recent_scores = [h["score"] for h in self.performance_history[-recent_count:]]
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        # Get older scores for comparison
        if len(self.performance_history) > recent_count:
            older_scores = [h["score"] for h in self.performance_history[:-recent_count]]
            avg_older = sum(older_scores) / len(older_scores)
        else:
            return "insufficient_data"
        
        # Calculate trend
        improvement_threshold = 0.05  # 5% improvement
        if avg_recent > avg_older + improvement_threshold:
            return "improving"
        elif avg_recent < avg_older - improvement_threshold:
            return "declining"
        else:
            return "stable"
    
    def _get_efficiency_rating(self, score: float) -> str:
        """Get efficiency rating based on score"""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.75:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        elif score >= 0.4:
            return "Poor"
        else:
            return "Needs Improvement"
    
    def learn_user_patterns(self, user_action: str, context: Dict[str, Any]):
        """Learn from user patterns to improve recommendations"""
        # Simple pattern learning (can be enhanced with ML)
        if user_action not in self.user_patterns:
            self.user_patterns[user_action] = []
        
        pattern_record = {
            "timestamp": datetime.now(),
            "context": context,
            "frequency": 1
        }
        
        self.user_patterns[user_action].append(pattern_record)
        
        # Keep only recent patterns
        cutoff_date = datetime.now() - timedelta(days=30)
        self.user_patterns[user_action] = [
            p for p in self.user_patterns[user_action] 
            if p["timestamp"] >= cutoff_date
        ]


class SmartSuggestionEngine:
    """AI-powered smart suggestions throughout the workflow"""
    
    @staticmethod
    def suggest_improvements(stage: str, content: Any, context: Dict[str, Any] = None) -> List[str]:
        """Provide context-aware suggestions"""
        suggestions = []
        
        if stage == "requirements":
            suggestions.extend(SmartSuggestionEngine._suggest_requirements_improvements(content, context))
        elif stage == "user_stories":
            suggestions.extend(SmartSuggestionEngine._suggest_user_story_improvements(content, context))
        elif stage == "design":
            suggestions.extend(SmartSuggestionEngine._suggest_design_improvements(content, context))
        elif stage == "code":
            suggestions.extend(SmartSuggestionEngine._suggest_code_improvements(content, context))
        elif stage == "tests":
            suggestions.extend(SmartSuggestionEngine._suggest_test_improvements(content, context))
        
        return suggestions[:3]  # Limit to 3 most relevant suggestions
    
    @staticmethod
    def _suggest_requirements_improvements(content: str, context: Dict[str, Any]) -> List[str]:
        """Suggest improvements for requirements"""
        suggestions = []
        
        if not content:
            return ["💡 Start by describing what you want to build"]
        
        word_count = len(content.split())
        content_lower = content.lower()
        
        if word_count < 30:
            suggestions.append("💡 Add more detail about user roles, features, and technical constraints")
        
        if 'user' not in content_lower and 'admin' not in content_lower:
            suggestions.append("💡 Specify different user types and their needs")
        
        if 'api' in content_lower and 'documentation' not in content_lower:
            suggestions.append("💡 Consider mentioning API documentation requirements")
        
        if 'data' in content_lower and 'security' not in content_lower:
            suggestions.append("💡 Include data security and privacy requirements")
        
        return suggestions
    
    @staticmethod
    def _suggest_user_story_improvements(content: List[str], context: Dict[str, Any]) -> List[str]:
        """Suggest improvements for user stories"""
        suggestions = []
        
        if not content:
            return ["💡 User stories will be generated from your requirements"]
        
        stories_text = ' '.join(content).lower()
        
        # Check for missing user types
        if 'admin' not in stories_text and len(content) > 3:
            suggestions.append("💡 Consider adding administrator user stories")
        
        if 'error' not in stories_text and 'fail' not in stories_text:
            suggestions.append("💡 Add stories for error handling and edge cases")
        
        if len(content) < 4:
            suggestions.append("💡 Consider adding more user stories to cover all functionality")
        
        return suggestions
    
    @staticmethod
    def _suggest_design_improvements(content: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Suggest improvements for design document"""
        suggestions = []
        
        if not content:
            return ["💡 Design document will be created from approved user stories"]
        
        functional = content.get('functional', [])
        technical = content.get('technical', [])
        
        if len(technical) < 3:
            suggestions.append("💡 Add more technical details (architecture, APIs, database design)")
        
        tech_text = ' '.join(technical).lower()
        if 'database' not in tech_text and 'storage' not in tech_text:
            suggestions.append("💡 Specify data storage and database requirements")
        
        if 'security' not in tech_text:
            suggestions.append("💡 Include security architecture and authentication design")
        
        return suggestions
    
    @staticmethod
    def _suggest_code_improvements(content: str, context: Dict[str, Any]) -> List[str]:
        """Suggest improvements for code"""
        suggestions = []
        
        if not content:
            return ["💡 Code will be generated after design document approval"]
        
        language = context.get('language', 'python') if context else 'python'
        
        if 'try:' not in content and 'except' not in content:
            suggestions.append("💡 Consider adding comprehensive error handling")
        
        if 'logging' not in content and 'log' not in content:
            suggestions.append("💡 Implement logging for better debugging and monitoring")
        
        if language == 'python' and 'def test_' not in content:
            suggestions.append("💡 Add unit tests alongside your main code")
        
        return suggestions
    
    @staticmethod
    def _suggest_test_improvements(content: str, context: Dict[str, Any]) -> List[str]:
        """Suggest improvements for test cases"""
        suggestions = []
        
        if not content:
            return ["💡 Test cases will be generated after code review"]
        
        content_lower = content.lower()
        
        if 'edge' not in content_lower and 'boundary' not in content_lower:
            suggestions.append("💡 Add edge case and boundary condition tests")
        
        if 'performance' not in content_lower:
            suggestions.append("💡 Consider adding performance and load tests")
        
        if 'security' not in content_lower:
            suggestions.append("💡 Include security-focused test scenarios")
        
        return suggestions


# Export the main classes
__all__ = [
    'AutonomyLevel',
    'QualityMetrics',
    'AutonomousDecisionEngine',
    'ErrorRecoveryEngine',
    'WorkflowOptimizer',
    'SmartSuggestionEngine'
]