# ui_utils.py
"""
Enhanced utility functions for UI components and features
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import zipfile
from pathlib import Path
import shutil
from docx import Document
import ast
import re
from typing import List, Dict, Any, Optional

# Try to import PDF generation, fallback if not available
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class WorkflowAnalytics:
    """Analytics and visualization utilities for the SDLC workflow"""
    
    @staticmethod
    def create_workflow_gantt(events, start_time):
        """Create a Gantt chart of the workflow stages"""
        if not events or not start_time:
            return None
        
        tasks = []
        current_time = start_time
        
        for i, event in enumerate(events):
            for node_name in event:
                # Calculate duration based on node type
                if "Auto" in node_name or "Generate" in node_name:
                    duration = timedelta(minutes=2 + (i % 3))  # AI tasks are faster
                else:
                    duration = timedelta(minutes=5 + (i * 2))  # Human tasks take longer
                
                tasks.append({
                    'Task': node_name,
                    'Start': current_time,
                    'Finish': current_time + duration,
                    'Resource': 'AI' if any(keyword in node_name for keyword in ['Auto', 'Generate', 'Security Review', 'QA Testing']) else 'Human',
                    'Duration_Minutes': duration.total_seconds() / 60
                })
                current_time += duration
        
        if not tasks:
            return None
        
        df = pd.DataFrame(tasks)
        
        fig = px.timeline(
            df, 
            x_start="Start", 
            x_end="Finish", 
            y="Task",
            color="Resource",
            title="Workflow Timeline",
            color_discrete_map={'AI': '#667eea', 'Human': '#764ba2'}
        )
        
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=400, showlegend=True)
        
        return fig
    
    @staticmethod
    def create_approval_funnel(state):
        """Create a funnel chart showing approval rates"""
        stages = [
            ('Requirements', 100),
            ('User Stories', 90 if state.get('user_story_status') == 'Approve' else 70),
            ('Design Document', 80 if state.get('design_document_review_status') == 'Approve' else 60),
            ('Code Review', 70 if state.get('code_review_status') == 'Approve' else 50),
            ('Security', 60 if state.get('security_review_status') == 'Approve' else 40),
            ('QA Testing', 50 if state.get('qa_review_status') == 'Approve' else 30),
            ('Deployment', 40 if state.get('deployment') == 'deployed' else 0)
        ]
        
        fig = go.Figure(go.Funnel(
            y=[s[0] for s in stages],
            x=[s[1] for s in stages],
            textposition="inside",
            textinfo="value+percent initial",
            marker={"color": ["#667eea", "#7c3aed", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#ede9fe"]},
        ))
        
        fig.update_layout(title="Workflow Progress Funnel", height=400)
        return fig
    
    @staticmethod
    def create_code_complexity_chart(code):
        """Analyze and visualize code complexity"""
        if not code:
            return None
        
        # Simple complexity metrics
        lines = code.split('\n')
        metrics = {
            'Total Lines': len(lines),
            'Code Lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'Comment Lines': len([l for l in lines if l.strip().startswith('#')]),
            'Functions': len(re.findall(r'def\s+\w+', code)),
            'Classes': len(re.findall(r'class\s+\w+', code)),
            'Imports': len([l for l in lines if l.strip().startswith(('import ', 'from '))]),
        }
        
        # Calculate complexity score
        code_lines = metrics['Code Lines']
        functions = metrics['Functions']
        classes = metrics['Classes']
        
        # Basic cyclomatic complexity estimation
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'with']
        complexity_count = sum(code.lower().count(keyword) for keyword in complexity_keywords)
        
        metrics['Complexity Score'] = complexity_count
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                marker_color=['#667eea', '#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe', '#10b981']
            )
        ])
        
        fig.update_layout(
            title="Code Metrics Analysis",
            xaxis_title="Metric",
            yaxis_title="Count",
            height=300
        )
        
        return fig
    
    @staticmethod
    def create_quality_trends(quality_history):
        """Create quality trends over time"""
        if not quality_history:
            return None
        
        df = pd.DataFrame(quality_history)
        
        fig = px.line(df, x='timestamp', y='quality_score', 
                     title='Quality Score Trends',
                     labels={'quality_score': 'Quality Score', 'timestamp': 'Time'})
        
        fig.update_layout(height=300)
        return fig


class ExportManager:
    """Handle exporting of artifacts in various formats"""
    
    @staticmethod
    def export_to_pdf(state, filename="sdlc_report.pdf"):
        """Export complete SDLC report to PDF"""
        if not REPORTLAB_AVAILABLE:
            # Fallback to text export
            return ExportManager.export_to_text(state, filename.replace('.pdf', '.txt'))
        
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#667eea'),
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            
            story.append(Paragraph("AI SDLC Workflow Report", title_style))
            story.append(Spacer(1, 0.5*inch))
            
            # Metadata
            metadata = [
                ['Generated Date:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ['Session ID:', st.session_state.thread["configurable"]["thread_id"][:8] if 'thread' in st.session_state else 'N/A'],
                ['Language:', state.get('programming_language', 'python').title()],
                ['Status:', 'Completed' if state.get('deployment') == 'deployed' else 'In Progress']
            ]
            
            t = Table(metadata)
            t.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ]))
            
            story.append(t)
            story.append(Spacer(1, 0.5*inch))
            
            # Requirements
            story.append(Paragraph("Requirements", styles['Heading2']))
            story.append(Paragraph(state.get('requirements', 'No requirements specified'), styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # User Stories
            if state.get('user_stories'):
                story.append(Paragraph("User Stories", styles['Heading2']))
                for i, story_text in enumerate(state['user_stories'], 1):
                    story.append(Paragraph(f"{i}. {story_text}", styles['Normal']))
                story.append(Spacer(1, 0.3*inch))
            
            # Build PDF
            doc.build(story)
            return filename
        except Exception as e:
            # Fallback to text export
            return ExportManager.export_to_text(state, filename.replace('.pdf', '.txt'))
    
    @staticmethod
    def export_to_text(state, filename="sdlc_report.txt"):
        """Export report to text file"""
        content = []
        content.append("AI SDLC WORKFLOW REPORT")
        content.append("=" * 50)
        content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"Language: {state.get('programming_language', 'python').title()}")
        content.append(f"Status: {'Completed' if state.get('deployment') == 'deployed' else 'In Progress'}")
        content.append("")
        
        # Requirements
        content.append("REQUIREMENTS:")
        content.append("-" * 20)
        content.append(state.get('requirements', 'No requirements specified'))
        content.append("")
        
        # User Stories
        if state.get('user_stories'):
            content.append("USER STORIES:")
            content.append("-" * 20)
            for i, story in enumerate(state['user_stories'], 1):
                content.append(f"{i}. {story}")
            content.append("")
        
        # Design Document
        if state.get('design_document'):
            content.append("DESIGN DOCUMENT:")
            content.append("-" * 20)
            doc = state['design_document']
            
            if doc.get('functional'):
                content.append("Functional Requirements:")
                for item in doc['functional']:
                    content.append(f"• {item}")
                content.append("")
            
            if doc.get('technical'):
                content.append("Technical Requirements:")
                for item in doc['technical']:
                    content.append(f"• {item}")
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return filename
    
    @staticmethod
    def export_all_artifacts(state):
        """Create a ZIP file with all artifacts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"sdlc_artifacts_{timestamp}.zip"
        
        try:
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                # Add existing artifact files
                artifact_paths = [
                    "artifacts/user_stories.txt",
                    "artifacts/design_document.docx",
                ]
                
                for path in artifact_paths:
                    if os.path.exists(path):
                        zipf.write(path, os.path.basename(path))
                
                # Add generated code
                if os.path.exists("generated_code"):
                    for root, dirs, files in os.walk("generated_code"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)
                
                # Add test cases
                if os.path.exists("test_cases"):
                    for root, dirs, files in os.walk("test_cases"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)
                
                # Create and add summary JSON
                summary = {
                    "session_id": st.session_state.thread["configurable"]["thread_id"] if 'thread' in st.session_state else 'unknown',
                    "timestamp": timestamp,
                    "requirements": state.get("requirements", ""),
                    "programming_language": state.get("programming_language", "python"),
                    "llm_model": state.get("llm_model", "gemma2-9b-it"),
                    "autonomy_level": state.get("autonomy_level", "manual"),
                    "status": "deployed" if state.get("deployment") == "deployed" else "in_progress",
                    "statistics": {
                        "user_stories_count": len(state.get("user_stories", [])),
                        "files_generated": len(os.listdir("generated_code")) if os.path.exists("generated_code") else 0,
                        "test_cases_count": len(os.listdir("test_cases")) if os.path.exists("test_cases") else 0,
                    }
                }
                
                zipf.writestr("summary.json", json.dumps(summary, indent=2))
            
            return zip_filename
        except Exception as e:
            st.error(f"Export failed: {str(e)}")
            return None


class ValidationHelper:
    """Input validation and error handling utilities"""
    
    @staticmethod
    def validate_requirements(requirements):
        """Validate user requirements input"""
        errors = []
        warnings = []
        
        if not requirements or not requirements.strip():
            errors.append("Requirements cannot be empty")
            return errors, warnings
        
        word_count = len(requirements.split())
        
        if word_count < 10:
            errors.append("Requirements must be at least 10 words long")
        elif word_count < 50:
            warnings.append("Consider adding more detail for better results (50+ words recommended)")
        
        if word_count > 1000:
            warnings.append("Requirements are very long. Consider breaking into phases.")
        
        # Check for common missing elements
        elements_to_check = {
            'user': "Consider mentioning user roles or personas",
            'feature': "Include specific features or functionality", 
            'data': "Mention data or database requirements if applicable",
            'security': "Consider mentioning security requirements",
            'performance': "Include performance requirements if relevant",
            'api': "Specify API requirements if applicable",
            'authentication': "Consider user authentication needs",
            'integration': "Mention any third-party integrations"
        }
        
        requirements_lower = requirements.lower()
        missing_count = 0
        for key, suggestion in elements_to_check.items():
            if key not in requirements_lower:
                missing_count += 1
                if missing_count <= 3:  # Only show first 3 suggestions
                    warnings.append(suggestion)
        
        # Check for specific language-related requirements
        if 'python' in requirements_lower:
            if 'flask' not in requirements_lower and 'django' not in requirements_lower and 'fastapi' not in requirements_lower:
                warnings.append("Consider specifying a Python web framework (Flask, Django, FastAPI)")
        
        return errors, warnings[:3]  # Limit warnings to 3
    
    @staticmethod
    def validate_code_syntax(code, language="python"):
        """Basic syntax validation for different languages"""
        if not code or not code.strip():
            return False, "Code is empty"
        
        try:
            if language.lower() == "python":
                # Python syntax validation
                compile(code, '<string>', 'exec')
                return True, None
            elif language.lower() in ["javascript", "typescript"]:
                # Basic JavaScript validation (simplified)
                # Check for common syntax errors
                if code.count('{') != code.count('}'):
                    return False, "Mismatched curly braces"
                if code.count('(') != code.count(')'):
                    return False, "Mismatched parentheses"
                return True, None
            else:
                # For other languages, do basic checks
                if code.count('{') != code.count('}'):
                    return False, "Mismatched curly braces"
                return True, None
                
        except SyntaxError as e:
            return False, f"Syntax error: {e.msg}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def analyze_requirements_quality(requirements: str) -> Dict[str, Any]:
        """Analyze the quality of requirements"""
        if not requirements:
            return {"score": 0, "issues": ["No requirements provided"]}
        
        words = requirements.split()
        word_count = len(words)
        
        # Scoring factors
        score = 0.0
        issues = []
        recommendations = []
        
        # Length score (0-25 points)
        if word_count >= 50 and word_count <= 300:
            score += 25
        elif word_count >= 20:
            score += 15
            if word_count < 50:
                recommendations.append("Add more detail for better results")
        else:
            score += 5
            issues.append("Requirements too brief")
        
        # Clarity score (0-25 points)
        clear_keywords = ['user', 'system', 'feature', 'function', 'requirement']
        clarity_score = min(25, sum(5 for keyword in clear_keywords if keyword in requirements.lower()))
        score += clarity_score
        
        # Technical depth score (0-25 points)
        technical_keywords = ['api', 'database', 'authentication', 'security', 'performance', 'scalability']
        tech_score = min(25, sum(4 for keyword in technical_keywords if keyword in requirements.lower()))
        score += tech_score
        
        if tech_score < 10:
            recommendations.append("Include more technical details")
        
        # Completeness score (0-25 points)
        completeness_keywords = ['input', 'output', 'validation', 'error', 'handling']
        completeness_score = min(25, sum(5 for keyword in completeness_keywords if keyword in requirements.lower()))
        score += completeness_score
        
        if completeness_score < 15:
            recommendations.append("Specify input/output and error handling requirements")
        
        return {
            "score": min(100, score),
            "word_count": word_count,
            "issues": issues,
            "recommendations": recommendations[:3],
            "breakdown": {
                "length": min(25, word_count // 2),
                "clarity": clarity_score,
                "technical_depth": tech_score,
                "completeness": completeness_score
            }
        }


class NotificationManager:
    """Enhanced notification system with persistence and styling"""
    
    @staticmethod
    def show_notification(message, type="info", duration=3):
        """Display a styled notification"""
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        colors = {
            "info": "#3b82f6",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }
        
        st.toast(f"{icons.get(type, icons['info'])} {message}", icon=icons.get(type, icons['info']))
    
    @staticmethod
    def add_to_history(message, type="info"):
        """Add notification to session history"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.append({
            'message': message,
            'type': type,
            'timestamp': datetime.now()
        })
        
        # Keep only last 50 notifications
        if len(st.session_state.notifications) > 50:
            st.session_state.notifications = st.session_state.notifications[-50:]
    
    @staticmethod
    def clear_old_notifications():
        """Remove notifications older than 5 minutes"""
        if 'notifications' in st.session_state:
            cutoff_time = datetime.now() - timedelta(minutes=5)
            st.session_state.notifications = [
                n for n in st.session_state.notifications 
                if n['timestamp'] > cutoff_time
            ]


class ThemeManager:
    """Handle theme switching and custom styling"""
    
    @staticmethod
    def apply_dark_theme():
        """Apply dark theme styles"""
        st.markdown("""
        <style>
        .stApp {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        .pro-card {
            background: #2d2d2d !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .main-header {
            background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 100%) !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background: #2d2d2d !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #4c1d95 0%, #5b21b6 100%) !important;
        }
        
        :root {
            --bg-primary: #2d2d2d;
            --bg-secondary: #1a1a1a;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --border-color: rgba(255, 255, 255, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_light_theme():
        """Apply light theme styles (default)"""
        st.markdown("""
        <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f5f7fa;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: rgba(0, 0, 0, 0.05);
        }
        </style>
        """, unsafe_allow_html=True)


class CodeAnalyzer:
    """Advanced code analysis utilities"""
    
    @staticmethod
    def analyze_code_structure(code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze code structure and provide metrics"""
        if not code:
            return {"error": "No code provided"}
        
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        analysis = {
            "total_lines": len(lines),
            "code_lines": len(non_empty_lines),
            "blank_lines": len(lines) - len(non_empty_lines),
            "language": language
        }
        
        if language.lower() == "python":
            analysis.update(CodeAnalyzer._analyze_python_code(code))
        elif language.lower() in ["javascript", "typescript"]:
            analysis.update(CodeAnalyzer._analyze_javascript_code(code))
        elif language.lower() == "java":
            analysis.update(CodeAnalyzer._analyze_java_code(code))
        else:
            analysis.update(CodeAnalyzer._analyze_generic_code(code))
        
        return analysis
    
    @staticmethod
    def _analyze_python_code(code: str) -> Dict[str, Any]:
        """Python-specific code analysis"""
        analysis = {
            "functions": len(re.findall(r'def\s+\w+', code)),
            "classes": len(re.findall(r'class\s+\w+', code)),
            "imports": len(re.findall(r'^(import|from)\s+', code, re.MULTILINE)),
            "comments": len(re.findall(r'#.*$', code, re.MULTILINE)),
            "docstrings": len(re.findall(r'""".*?"""', code, re.DOTALL)),
        }
        
        # Check for common patterns
        analysis["has_main"] = "__main__" in code
        analysis["has_error_handling"] = "try:" in code and "except" in code
        analysis["has_type_hints"] = ":" in code and "->" in code
        
        return analysis
    
    @staticmethod
    def _analyze_javascript_code(code: str) -> Dict[str, Any]:
        """JavaScript-specific code analysis"""
        analysis = {
            "functions": len(re.findall(r'function\s+\w+|const\s+\w+\s*=.*?=>', code)),
            "classes": len(re.findall(r'class\s+\w+', code)),
            "imports": len(re.findall(r'^(import|require)', code, re.MULTILINE)),
            "comments": len(re.findall(r'//.*$|/\*.*?\*/', code, re.MULTILINE | re.DOTALL)),
        }
        
        # Check for common patterns
        analysis["has_async"] = "async" in code
        analysis["has_promises"] = ".then(" in code or "await" in code
        analysis["has_error_handling"] = "try" in code and "catch" in code
        analysis["uses_modern_syntax"] = "const" in code or "let" in code
        
        return analysis
    
    @staticmethod
    def _analyze_java_code(code: str) -> Dict[str, Any]:
        """Java-specific code analysis"""
        analysis = {
            "classes": len(re.findall(r'class\s+\w+', code)),
            "methods": len(re.findall(r'(public|private|protected).*?\w+\s*\(', code)),
            "imports": len(re.findall(r'^import\s+', code, re.MULTILINE)),
            "comments": len(re.findall(r'//.*$|/\*.*?\*/', code, re.MULTILINE | re.DOTALL)),
        }
        
        # Check for common patterns
        analysis["has_main"] = "public static void main" in code
        analysis["has_package"] = "package " in code
        analysis["has_error_handling"] = "try" in code and "catch" in code
        
        return analysis
    
    @staticmethod
    def _analyze_generic_code(code: str) -> Dict[str, Any]:
        """Generic code analysis for unsupported languages"""
        return {
            "comment_lines": len(re.findall(r'(#|//|/\*).*$', code, re.MULTILINE)),
            "bracket_balance": code.count('{') - code.count('}'),
            "paren_balance": code.count('(') - code.count(')'),
        }


class FileManager:
    """File management utilities"""
    
    @staticmethod
    def ensure_directories():
        """Ensure all required directories exist"""
        directories = [
            "artifacts",
            "generated_code", 
            "test_cases",
            "exports",
            "auto_saves",
            "logs"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def clean_old_files(directory: str, days: int = 7):
        """Clean files older than specified days"""
        if not os.path.exists(directory):
            return
        
        cutoff_time = datetime.now() - timedelta(days=days)
        
        for file_path in Path(directory).glob("*"):
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    try:
                        file_path.unlink()
                    except Exception:
                        pass  # Ignore errors when cleaning
    
    @staticmethod
    def get_file_stats(directory: str) -> Dict[str, Any]:
        """Get statistics about files in directory"""
        if not os.path.exists(directory):
            return {"exists": False}
        
        files = list(Path(directory).glob("*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        
        return {
            "exists": True,
            "file_count": len([f for f in files if f.is_file()]),
            "directory_count": len([f for f in files if f.is_dir()]),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }


class PerformanceMonitor:
    """Monitor application performance"""
    
    @staticmethod
    def track_stage_duration(stage_name: str, start_time: datetime, end_time: datetime):
        """Track how long each stage takes"""
        if 'stage_durations' not in st.session_state:
            st.session_state.stage_durations = []
        
        duration = (end_time - start_time).total_seconds()
        
        st.session_state.stage_durations.append({
            "stage": stage_name,
            "duration_seconds": duration,
            "start_time": start_time,
            "end_time": end_time
        })
    
    @staticmethod
    def get_performance_metrics() -> Dict[str, Any]:
        """Get overall performance metrics"""
        if 'stage_durations' not in st.session_state:
            return {}
        
        durations = st.session_state.stage_durations
        if not durations:
            return {}
        
        total_duration = sum(d["duration_seconds"] for d in durations)
        avg_duration = total_duration / len(durations)
        
        return {
            "total_stages": len(durations),
            "total_duration_seconds": total_duration,
            "total_duration_minutes": round(total_duration / 60, 2),
            "average_duration_seconds": round(avg_duration, 2),
            "fastest_stage": min(durations, key=lambda x: x["duration_seconds"])["stage"],
            "slowest_stage": max(durations, key=lambda x: x["duration_seconds"])["stage"]
        }


# Export all utilities
__all__ = [
    'WorkflowAnalytics',
    'ExportManager',
    'NotificationManager',
    'ThemeManager',
    'ValidationHelper',
    'CodeAnalyzer',
    'FileManager',
    'PerformanceMonitor'
]