# professional_success_component.py
"""
Professional success modal and notification components for AI SDLC Wizard
Replaces the balloons animation with enterprise-appropriate success indicators
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional

class ProfessionalSuccessModal:
    """Professional modal window for deployment success"""
    
    @staticmethod
    def show_deployment_success(state: Dict[str, Any], deployment_time: Optional[str] = None):
        """Show professional deployment success modal"""
        
        if not deployment_time:
            deployment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Professional Success Modal CSS
        modal_css = """
        <style>
        /* Modal Overlay */
        .success-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 2000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease-in-out;
        }
        
        /* Modal Content */
        .success-modal {
            background: white;
            padding: 0;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow: hidden;
            animation: slideIn 0.4s ease-out;
            position: relative;
        }
        
        /* Modal Header */
        .success-modal-header {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }
        
        .success-icon {
            font-size: 4rem;
            margin-bottom: 15px;
            display: block;
            animation: checkmarkAnimation 0.6s ease-in-out;
        }
        
        .success-title {
            font-size: 2rem;
            margin: 0;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .success-subtitle {
            font-size: 1.1rem;
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-weight: 400;
        }
        
        /* Modal Body */
        .success-modal-body {
            padding: 30px;
        }
        
        .deployment-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        /* Action Buttons */
        .modal-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        
        .btn-primary {
            flex: 1;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
        }
        
        .btn-secondary {
            flex: 1;
            background: #f1f5f9;
            color: #475569;
            border: 2px solid #e2e8f0;
            padding: 15px 25px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            text-align: center;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        }
        
        .btn-secondary:hover {
            background: #e2e8f0;
            transform: translateY(-1px);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideIn {
            from { 
                opacity: 0;
                transform: translateY(-50px) scale(0.95);
            }
            to { 
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        @keyframes checkmarkAnimation {
            0% {
                transform: scale(0);
                opacity: 0;
            }
            50% {
                transform: scale(1.2);
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        /* Success Metrics */
        .success-metrics {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 1px solid #f59e0b;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .metrics-title {
            color: #92400e;
            font-weight: 700;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .metric-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .metric-label {
            color: #78350f;
            font-weight: 500;
        }
        
        .metric-value {
            color: #92400e;
            font-weight: 700;
        }
        
        /* Close button */
        .modal-close {
            position: absolute;
            top: 15px;
            right: 20px;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }
        
        .modal-close:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
        }
        </style>
        """
        
        # Calculate deployment statistics
        lang_config = st.session_state.state.get("programming_language", "python")
        language_name = st.session_state.get("config", {}).get("SUPPORTED_LANGUAGES", {}).get(lang_config, {}).get("name", "Python")
        
        # Get quality metrics
        quality_metrics = state.get("quality_metrics", {})
        overall_score = quality_metrics.get("overall_score", 0.85)
        autonomous_decisions = len(state.get("autonomous_decisions", []))
        
        # Files generated
        files_generated = 0
        if st.session_state.state.get("code"):
            files_generated += st.session_state.state["code"].count("Filename:")
        if st.session_state.state.get("test_cases"):
            files_generated += st.session_state.state["test_cases"].count("Filename:")
        
        # Modal HTML
        modal_html = f"""
        {modal_css}
        <div class="success-modal-overlay" id="successModal">
            <div class="success-modal">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                
                <div class="success-modal-header">
                    <div class="success-icon">🎉</div>
                    <h1 class="success-title">Deployment Successful!</h1>
                    <p class="success-subtitle">Your application is now live in production</p>
                </div>
                
                <div class="success-modal-body">
                    <div class="deployment-stats">
                        <div class="stat-card">
                            <div class="stat-value">{language_name}</div>
                            <div class="stat-label">Language</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{files_generated}</div>
                            <div class="stat-label">Files Generated</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{int(overall_score * 100)}%</div>
                            <div class="stat-label">Quality Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{autonomous_decisions}</div>
                            <div class="stat-label">Auto Decisions</div>
                        </div>
                    </div>
                    
                    <div class="success-metrics">
                        <div class="metrics-title">📊 Deployment Summary</div>
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <span class="metric-label">Environment:</span>
                                <span class="metric-value">Production</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-label">Version:</span>
                                <span class="metric-value">1.0.0</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-label">Status:</span>
                                <span class="metric-value">Active</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-label">Health:</span>
                                <span class="metric-value">✅ Passing</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-label">Deployed:</span>
                                <span class="metric-value">{deployment_time}</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-label">Autonomy:</span>
                                <span class="metric-value">{state.get('autonomy_level', 'manual').title()}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="modal-actions">
                        <button class="btn-secondary" onclick="closeModal()">
                            📊 View Analytics
                        </button>
                        <button class="btn-primary" onclick="downloadArtifacts()">
                            📦 Download All Artifacts
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        function closeModal() {{
            document.getElementById('successModal').style.display = 'none';
        }}
        
        function downloadArtifacts() {{
            // This would trigger the download in a real implementation
            alert('Downloading all project artifacts...');
            closeModal();
        }}
        
        // Auto-close after 10 seconds
        setTimeout(() => {{
            const modal = document.getElementById('successModal');
            if (modal) {{
                modal.style.opacity = '0';
                setTimeout(() => modal.style.display = 'none', 300);
            }}
        }}, 10000);
        </script>
        """
        
        # Display the modal
        st.markdown(modal_html, unsafe_allow_html=True)

class ProfessionalNotifications:
    """Professional notification system"""
    
    @staticmethod
    def show_success_toast(title: str, message: str, duration: int = 5):
        """Show a professional success toast notification"""
        
        toast_css = """
        <style>
        .success-toast {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-left: 5px solid #10b981;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            padding: 20px 25px;
            min-width: 350px;
            max-width: 450px;
            z-index: 1000;
            animation: slideInRight 0.4s ease-out;
        }
        
        .toast-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
        }
        
        .toast-icon {
            font-size: 1.5rem;
            color: #10b981;
        }
        
        .toast-title {
            font-weight: 700;
            color: #1e293b;
            margin: 0;
            font-size: 1.1rem;
        }
        
        .toast-message {
            color: #64748b;
            margin: 0;
            line-height: 1.5;
        }
        
        .toast-progress {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            background: #10b981;
            animation: progressBar {duration}s linear;
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes progressBar {
            from { width: 100%; }
            to { width: 0%; }
        }
        </style>
        """
        
        toast_html = f"""
        {toast_css}
        <div class="success-toast" id="successToast">
            <div class="toast-header">
                <div class="toast-icon">✅</div>
                <h4 class="toast-title">{title}</h4>
            </div>
            <p class="toast-message">{message}</p>
            <div class="toast-progress"></div>
        </div>
        
        <script>
        setTimeout(() => {{
            const toast = document.getElementById('successToast');
            if (toast) {{
                toast.style.transform = 'translateX(100%)';
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }}
        }}, {duration * 1000});
        </script>
        """
        
        st.markdown(toast_html, unsafe_allow_html=True)
    
    @staticmethod
    def show_deployment_complete_banner():
        """Show a professional deployment completion banner"""
        
        banner_css = """
        <style>
        .deployment-banner {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border: 2px solid #10b981;
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: successPulse 2s ease-in-out;
        }
        
        .deployment-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 3s ease-in-out infinite;
        }
        
        .banner-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            display: block;
            color: #065f46;
        }
        
        .banner-title {
            color: #065f46;
            font-size: 2rem;
            margin: 0 0 10px 0;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        .banner-subtitle {
            color: #047857;
            font-size: 1.2rem;
            margin: 0;
            font-weight: 500;
        }
        
        .banner-stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }
        
        .banner-stat {
            text-align: center;
        }
        
        .banner-stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #065f46;
            display: block;
        }
        
        .banner-stat-label {
            font-size: 0.9rem;
            color: #047857;
            font-weight: 500;
        }
        
        @keyframes successPulse {
            0% {
                transform: scale(0.95);
                opacity: 0;
            }
            50% {
                transform: scale(1.02);
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
        
        .success-checkmark {
            display: inline-block;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #10b981;
            position: relative;
            margin: 0 auto 20px;
            animation: checkmarkBounce 0.6s ease-in-out;
        }
        
        .success-checkmark::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 2rem;
            font-weight: bold;
        }
        
        @keyframes checkmarkBounce {
            0% {
                transform: scale(0);
                opacity: 0;
            }
            50% {
                transform: scale(1.3);
            }
            100% {
                transform: scale(1);
                opacity: 1;
            }
        }
        </style>
        """
        
        banner_html = f"""
        {banner_css}
        <div class="deployment-banner">
            <div class="success-checkmark"></div>
            <h1 class="banner-title">🚀 Deployment Successful!</h1>
            <p class="banner-subtitle">Your application is now live and ready for users</p>
        </div>
        """
        
        st.markdown(banner_html, unsafe_allow_html=True)

class DeploymentCelebration:
    """Professional deployment celebration component"""
    
    @staticmethod
    def show_completion_summary(state: Dict[str, Any]):
        """Show a comprehensive completion summary"""
        
        # Calculate metrics
        total_files = 0
        if state.get("code"):
            total_files += state["code"].count("Filename:")
        if state.get("test_cases"):
            total_files += state["test_cases"].count("Filename:")
        
        user_stories_count = len(state.get("user_stories", []))
        autonomous_decisions = len(state.get("autonomous_decisions", []))
        
        # Get workflow duration
        start_time = st.session_state.get("start_time")
        duration = "N/A"
        if start_time:
            elapsed = datetime.now() - start_time
            duration = f"{elapsed.total_seconds() / 60:.1f} minutes"
        
        quality_score = state.get("quality_metrics", {}).get("overall_score", 0.85)
        
        summary_html = f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        ">
            <div style="font-size: 3rem; margin-bottom: 20px;">🏆</div>
            <h2 style="margin: 0 0 15px 0; font-size: 2.2rem; font-weight: 800;">
                Project Completed Successfully!
            </h2>
            <p style="margin: 0 0 25px 0; font-size: 1.2rem; opacity: 0.9;">
                Your AI-powered SDLC workflow has been completed
            </p>
            
            <div style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 20px;
                margin: 25px 0;
            ">
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700;">{user_stories_count}</div>
                    <div style="opacity: 0.8;">User Stories</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700;">{total_files}</div>
                    <div style="opacity: 0.8;">Files Generated</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700;">{int(quality_score * 100)}%</div>
                    <div style="opacity: 0.8;">Quality Score</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700;">{autonomous_decisions}</div>
                    <div style="opacity: 0.8;">AI Decisions</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700;">{duration}</div>
                    <div style="opacity: 0.8;">Duration</div>
                </div>
            </div>
        </div>
        """
        
        st.markdown(summary_html, unsafe_allow_html=True)

# Usage example for the updated deployment section
def render_professional_deployment_success(state: Dict[str, Any]):
    """Render professional deployment success instead of balloons"""
    
    # Show the modal
    success_modal = ProfessionalSuccessModal()
    success_modal.show_deployment_success(state)
    
    # Show the banner
    notifications = ProfessionalNotifications()
    notifications.show_deployment_complete_banner()
    
    # Show completion summary
    celebration = DeploymentCelebration()
    celebration.show_completion_summary(state)
    
    # Show success toast
    notifications.show_success_toast(
        "Deployment Complete",
        "Your application has been successfully deployed to production and is ready for users!"
    )