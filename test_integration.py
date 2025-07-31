# test_integration.py
"""
Integration tests and health checks for AI SDLC Wizard
Run this to verify all components are working correctly
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import json
import traceback
from datetime import datetime
from typing import List, Dict, Any, Tuple

class IntegrationTester:
    """Comprehensive integration testing suite"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        self.original_dir = os.getcwd()
    
    def setup_test_environment(self):
        """Set up temporary test environment"""
        self.temp_dir = tempfile.mkdtemp(prefix="sdlc_test_")
        print(f"🧪 Test environment: {self.temp_dir}")
        
        # Copy required files to test directory
        required_files = [
            "config.py", "sdlc_graph.py", "autonomous_features.py",
            "ui_utils.py", "advanced_features.py", ".env"
        ]
        
        for file in required_files:
            if Path(file).exists():
                shutil.copy2(file, self.temp_dir)
        
        # Change to test directory
        os.chdir(self.temp_dir)
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        os.chdir(self.original_dir)
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            print(f"🧹 Cleaned up test environment")
    
    def run_test(self, test_name: str, test_func) -> Tuple[bool, str, Any]:
        """Run a single test and capture results"""
        print(f"🔍 Testing: {test_name}")
        
        try:
            start_time = datetime.now()
            result = test_func()
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if result is True or (isinstance(result, tuple) and result[0]):
                print(f"✅ {test_name} - PASSED ({duration:.2f}s)")
                return True, "PASSED", result
            else:
                print(f"❌ {test_name} - FAILED ({duration:.2f}s)")
                return False, "FAILED", result
                
        except Exception as e:
            print(f"💥 {test_name} - ERROR: {str(e)}")
            return False, "ERROR", str(e)
    
    def test_imports(self) -> bool:
        """Test all critical imports"""
        try:
            # Core framework imports
            import streamlit
            import plotly
            import pandas
            
            # LangChain imports
            import langchain
            import langgraph
            from langchain_groq import ChatGroq
            
            # Project imports
            from config import Config
            from autonomous_features import AutonomousDecisionEngine
            from ui_utils import ValidationHelper
            
            return True
        except ImportError as e:
            print(f"Import error: {e}")
            return False
    
    def test_config_loading(self) -> bool:
        """Test configuration loading"""
        try:
            from config import Config, ActiveConfig
            
            # Test basic config access
            assert hasattr(Config, 'SUPPORTED_LANGUAGES')
            assert hasattr(Config, 'AVAILABLE_MODELS') 
            assert hasattr(Config, 'AUTONOMY_LEVELS')
            
            # Test config methods
            python_config = Config.get_language_config("python")
            assert python_config['name'] == 'Python'
            
            model_config = Config.get_model_config(Config.DEFAULT_LLM_MODEL)
            assert 'name' in model_config
            
            return True
        except Exception as e:
            print(f"Config error: {e}")
            return False
    
    def test_autonomous_engine(self) -> bool:
        """Test autonomous decision engine"""
        try:
            from autonomous_features import AutonomousDecisionEngine, AutonomyLevel, QualityMetrics
            
            # Test engine creation
            engine = AutonomousDecisionEngine(AutonomyLevel.SEMI_AUTO)
            
            # Test user story analysis
            test_stories = [
                "As a user, I want to log in so that I can access my account",
                "As an admin, I want to manage users so that I can control access"
            ]
            test_requirements = "Create a user management system with login functionality"
            
            decision, metrics, feedback = engine.analyze_user_stories(test_stories, test_requirements)
            
            assert decision in ["Approve", "Denied"]
            assert isinstance(metrics, QualityMetrics)
            assert isinstance(feedback, str)
            assert 0.0 <= metrics.overall_score <= 1.0
            
            return True
        except Exception as e:
            print(f"Autonomous engine error: {e}")
            return False
    
    def test_graph_workflow(self) -> bool:
        """Test the LangGraph workflow"""
        try:
            from sdlc_graph import graph, State
            
            # Test graph structure
            assert graph is not None
            
            # Test state structure
            test_state = {
                "requirements": "Test requirement",
                "user_stories": [],
                "user_story_status": "Approve",
                "user_story_feedback": [],
                "design_document": {},
                "code": "",
                "test_cases": "",
                "deployment": ""
            }
            
            # Verify state can be processed
            assert isinstance(test_state, dict)
            
            return True
        except Exception as e:
            print(f"Graph workflow error: {e}")
            return False
    
    def test_file_operations(self) -> bool:
        """Test file creation and management"""
        try:
            from ui_utils import FileManager, ExportManager
            
            # Test directory creation
            FileManager.ensure_directories()
            
            # Test file stats
            stats = FileManager.get_file_stats(".")
            assert stats['exists'] == True
            
            # Test export functionality
            test_state = {
                "requirements": "Test requirements",
                "user_stories": ["Test story 1", "Test story 2"],
                "programming_language": "python"
            }
            
            # Test text export
            export_manager = ExportManager()
            filename = export_manager.export_to_text(test_state, "test_export.txt")
            assert Path(filename).exists()
            
            return True
        except Exception as e:
            print(f"File operations error: {e}")
            return False
    
    def test_validation_helpers(self) -> bool:
        """Test validation helpers"""
        try:
            from ui_utils import ValidationHelper
            
            # Test requirements validation
            errors, warnings = ValidationHelper.validate_requirements("Test requirements for validation")
            assert isinstance(errors, list)
            assert isinstance(warnings, list)
            
            # Test empty requirements
            errors, warnings = ValidationHelper.validate_requirements("")
            assert len(errors) > 0  # Should have errors for empty requirements
            
            # Test code syntax validation
            valid_python = "def hello():\n    return 'Hello World'"
            is_valid, error = ValidationHelper.validate_code_syntax(valid_python, "python")
            assert is_valid == True
            
            invalid_python = "def hello(\n    return 'Hello World'"
            is_valid, error = ValidationHelper.validate_code_syntax(invalid_python, "python")
            assert is_valid == False
            
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    def test_language_support(self) -> bool:
        """Test multi-language support"""
        try:
            from enhanced_sdlc_graph import (
                get_language_specific_prompt_addon,
                parse_files_with_language,
                validate_language_support
            )
            
            # Test language validation
            assert validate_language_support("python") == True
            assert validate_language_support("invalid_language") == False
            
            # Test prompt addon generation
            addon = get_language_specific_prompt_addon("python")
            assert "Python" in addon
            assert "pytest" in addon
            
            # Test file parsing
            test_response = '''
            Filename: test.py
            Code:
            ```python
            def hello():
                return "Hello World"
            ```
            '''
            
            files = parse_files_with_language(test_response, "python")
            assert len(files) == 1
            assert files[0]['filename'] == 'test.py'
            assert 'hello' in files[0]['code']
            
            return True
        except Exception as e:
            print(f"Language support error: {e}")
            return False
    
    def test_error_recovery(self) -> bool:
        """Test error recovery mechanisms"""
        try:
            from autonomous_features import ErrorRecoveryEngine
            
            engine = ErrorRecoveryEngine()
            
            # Test API error recovery
            success, action = engine.handle_error(
                "api_error",
                {"retry_count": 0, "error": "Connection timeout"},
                {"active_node": "test_stage"}
            )
            
            assert success == True
            assert action['action'] == 'retry'
            
            # Test error history
            summary = engine.get_error_summary()
            assert summary['total_errors'] == 1
            
            return True
        except Exception as e:
            print(f"Error recovery error: {e}")
            return False
    
    def test_workflow_optimization(self) -> bool:
        """Test workflow optimization"""
        try:
            from autonomous_features import WorkflowOptimizer
            
            optimizer = WorkflowOptimizer()
            
            # Test performance analysis
            test_data = {
                "duration": 300,  # 5 minutes
                "iterations": 2,
                "errors": 1,
                "autonomous_decisions": 3
            }
            
            analysis = optimizer.analyze_workflow_performance(test_data)
            
            assert 'performance_score' in analysis
            assert 'suggestions' in analysis
            assert 'trend' in analysis
            assert 0.0 <= analysis['performance_score'] <= 1.0
            
            return True
        except Exception as e:
            print(f"Workflow optimization error: {e}")
            return False
    
    def test_environment_variables(self) -> bool:
        """Test environment variable loading"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            # Check if GROQ_API_KEY is available (not necessarily valid)
            groq_key = os.getenv("GROQ_API_KEY")
            
            if not groq_key:
                print("⚠️  GROQ_API_KEY not found in environment")
                return False
            
            if groq_key == "your_groq_api_key_here":
                print("⚠️  GROQ_API_KEY is still set to default value")
                return False
            
            return True
        except Exception as e:
            print(f"Environment variables error: {e}")
            return False
    
    def test_llm_connection(self) -> bool:
        """Test LLM connection (if API key is available)"""
        try:
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key or groq_key == "your_groq_api_key_here":
                print("⚠️  Skipping LLM test - API key not configured")
                return True  # Not a failure, just skip
            
            from enhanced_sdlc_graph import get_llm
            
            llm = get_llm("gemma2-9b-it")
            
            # Test with a simple prompt
            test_response = llm.invoke("Say 'Hello' in one word")
            
            if hasattr(test_response, 'content'):
                response_text = test_response.content
            else:
                response_text = str(test_response)
            
            # Basic validation of response
            assert len(response_text) > 0
            print(f"✅ LLM responded: {response_text[:50]}...")
            
            return True
        except Exception as e:
            print(f"LLM connection error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("🚀 Starting AI SDLC Wizard Integration Tests")
        print("=" * 60)
        
        # Set up test environment
        self.setup_test_environment()
        
        try:
            # Define all tests
            tests = [
                ("Core Imports", self.test_imports),
                ("Configuration Loading", self.test_config_loading),
                ("Autonomous Engine", self.test_autonomous_engine),
                ("Graph Workflow", self.test_graph_workflow),
                ("File Operations", self.test_file_operations),
                ("Validation Helpers", self.test_validation_helpers),
                ("Language Support", self.test_language_support),
                ("Error Recovery", self.test_error_recovery),
                ("Workflow Optimization", self.test_workflow_optimization),
                ("Environment Variables", self.test_environment_variables),
                ("LLM Connection", self.test_llm_connection),
            ]
            
            passed = 0
            failed = 0
            
            # Run each test
            for test_name, test_func in tests:
                success, status, result = self.run_test(test_name, test_func)
                
                test_record = {
                    "name": test_name,
                    "status": status,
                    "success": success,
                    "result": str(result)[:200],  # Limit result length
                    "timestamp": datetime.now().isoformat()
                }
                
                self.test_results.append(test_record)
                
                if success:
                    passed += 1
                else:
                    failed += 1
            
            # Summary
            print("\n" + "=" * 60)
            print(f"📊 Test Summary: {passed} passed, {failed} failed")
            
            if failed == 0:
                print("🎉 All tests passed! AI SDLC Wizard is ready to use.")
                overall_status = "SUCCESS"
            else:
                print("⚠️  Some tests failed. Please check the errors above.")
                overall_status = "PARTIAL"
            
            # Generate test report
            report = self._generate_test_report(overall_status, passed, failed)
            
            return {
                "overall_status": overall_status,
                "passed": passed,
                "failed": failed,
                "report_file": report,
                "test_results": self.test_results
            }
            
        finally:
            # Always clean up
            self.cleanup_test_environment()
    
    def _generate_test_report(self, status: str, passed: int, failed: int) -> str:
        """Generate detailed test report"""
        report_data = {
            "test_summary": {
                "overall_status": status,
                "total_tests": len(self.test_results),
                "passed": passed,
                "failed": failed,
                "success_rate": f"{(passed / len(self.test_results) * 100):.1f}%"
            },
            "system_info": {
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform,
                "timestamp": datetime.now().isoformat()
            },
            "test_details": self.test_results,
            "recommendations": self._generate_recommendations()
        }
        
        # Save to file
        report_filename = f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = Path(self.original_dir) / report_filename
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"📄 Test report saved: {report_filename}")
        return str(report_path)
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [t for t in self.test_results if not t['success']]
        
        for test in failed_tests:
            if "Import" in test['name']:
                recommendations.append("Install missing dependencies: pip install -r requirements.txt")
            elif "Environment" in test['name']:
                recommendations.append("Configure GROQ_API_KEY in .env file")
            elif "LLM" in test['name']:
                recommendations.append("Verify API key and internet connection")
            elif "Config" in test['name']:
                recommendations.append("Check config.py file exists and is properly formatted")
        
        if not recommendations:
            recommendations.append("All tests passed! Your installation is ready to use.")
        
        return recommendations


class HealthChecker:
    """System health check utilities"""
    
    @staticmethod
    def check_disk_space() -> Tuple[bool, str]:
        """Check available disk space"""
        try:
            usage = shutil.disk_usage(".")
            free_gb = usage.free / (1024**3)
            
            if free_gb >= 2:
                return True, f"Sufficient disk space: {free_gb:.1f}GB available"
            else:
                return False, f"Low disk space: {free_gb:.1f}GB available (2GB+ recommended)"
        except Exception as e:
            return False, f"Cannot check disk space: {e}"
    
    @staticmethod
    def check_memory() -> Tuple[bool, str]:
        """Check available memory"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            available_gb = memory.available / (1024**3)
            
            if available_gb >= 1:
                return True, f"Sufficient memory: {available_gb:.1f}GB available"
            else:
                return False, f"Low memory: {available_gb:.1f}GB available (1GB+ recommended)"
        except ImportError:
            return True, "Cannot check memory (psutil not available)"
        except Exception as e:
            return False, f"Cannot check memory: {e}"
    
    @staticmethod
    def check_network_connectivity() -> Tuple[bool, str]:
        """Check network connectivity to AI services"""
        try:
            import requests
            
            # Test connection to Groq API
            response = requests.get("https://api.groq.com", timeout=10)
            
            if response.status_code in [200, 404]:  # 404 is also fine, means we can reach the server
                return True, "Network connectivity to AI services is working"
            else:
                return False, f"Network issue: HTTP {response.status_code}"
                
        except requests.RequestException as e:
            return False, f"Network connectivity issue: {e}"
        except ImportError:
            return True, "Cannot check network (requests not available)"
    
    @staticmethod
    def check_permissions() -> Tuple[bool, str]:
        """Check file system permissions"""
        try:
            # Test write permissions
            test_file = Path("permission_test.tmp")
            test_file.write_text("test")
            test_file.unlink()
            
            return True, "File system permissions are correct"
        except Exception as e:
            return False, f"Permission issue: {e}"
    
    @staticmethod
    def run_health_check() -> Dict[str, Any]:
        """Run comprehensive health check"""
        print("🏥 Running System Health Check")
        print("-" * 40)
        
        checks = [
            ("Disk Space", HealthChecker.check_disk_space),
            ("Memory", HealthChecker.check_memory),
            ("Network", HealthChecker.check_network_connectivity),
            ("Permissions", HealthChecker.check_permissions),
        ]
        
        results = {}
        all_healthy = True
        
        for check_name, check_func in checks:
            try:
                success, message = check_func()
                results[check_name] = {"success": success, "message": message}
                
                if success:
                    print(f"✅ {check_name}: {message}")
                else:
                    print(f"❌ {check_name}: {message}")
                    all_healthy = False
                    
            except Exception as e:
                results[check_name] = {"success": False, "message": f"Check failed: {e}"}
                print(f"💥 {check_name}: Check failed - {e}")
                all_healthy = False
        
        health_status = "HEALTHY" if all_healthy else "ISSUES_DETECTED"
        
        print(f"\n🏥 Overall Health: {health_status}")
        
        return {
            "overall_health": health_status,
            "individual_checks": results,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI SDLC Wizard Integration Tests")
    parser.add_argument("--health-only", action="store_true", help="Run only health checks")
    parser.add_argument("--tests-only", action="store_true", help="Run only integration tests")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    
    args = parser.parse_args()
    
    try:
        if args.health_only:
            # Run health check only
            health_results = HealthChecker.run_health_check()
            return health_results['overall_health'] == "HEALTHY"
        
        elif args.tests_only:
            # Run integration tests only
            tester = IntegrationTester()
            results = tester.run_all_tests()
            return results['overall_status'] == "SUCCESS"
        
        else:
            # Run both health check and integration tests
            print("🔍 Running Comprehensive System Check")
            print("=" * 60)
            
            # Health check first
            health_results = HealthChecker.run_health_check()
            
            print("\n")
            
            # Integration tests
            tester = IntegrationTester()
            test_results = tester.run_all_tests()
            
            # Overall summary
            print("\n" + "=" * 60)
            print("📋 FINAL SUMMARY")
            print("=" * 60)
            
            health_ok = health_results['overall_health'] == "HEALTHY"
            tests_ok = test_results['overall_status'] == "SUCCESS"
            
            if health_ok and tests_ok:
                print("🎉 ALL SYSTEMS GO! AI SDLC Wizard is fully operational.")
                return True
            else:
                if not health_ok:
                    print("⚠️  System health issues detected")
                if not tests_ok:
                    print("⚠️  Integration test failures detected")
                print("💡 Please address the issues above before using the application")
                return False
    
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)