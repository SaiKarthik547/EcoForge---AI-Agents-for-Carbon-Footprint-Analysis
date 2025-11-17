import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import asyncio
import json
import time
from typing import Dict, Any, List

# Import configuration and components
from config import Config
from workflow import EcoForgeWorkflow
from memory import ConversationMemory
from observability import ObservabilityPanel

# Configure Streamlit page
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cinematic effects
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .agent-card {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .eco-score {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #00ff88, #00cc6a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0,255,136,0.5);
    }
    
    .carbon-footprint {
        font-size: 2.5rem;
        color: #ff4757;
        text-align: center;
        text-shadow: 0 0 20px rgba(255,71,87,0.5);
    }
    
    .action-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .glow {
        box-shadow: 0 0 20px rgba(0,255,136,0.6);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(0,255,136,0.6); }
        to { box-shadow: 0 0 30px rgba(0,255,136,0.8); }
    }
</style>
""", unsafe_allow_html=True)

class EcoForgeApp:
    """Main EcoForge Streamlit Application"""
    
    def __init__(self):
        self.config = Config()
        self.workflow = EcoForgeWorkflow()
        self.memory = ConversationMemory()
        self.observability = ObservabilityPanel()
        
        # Initialize session state
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if 'current_analysis' not in st.session_state:
            st.session_state.current_analysis = None
        if 'eco_score' not in st.session_state:
            st.session_state.eco_score = 0
        if 'agent_status' not in st.session_state:
            st.session_state.agent_status = {}
    
    def render_header(self):
        """Render the main application header"""
        st.markdown(f"""
        <div class="main-header">
            <h1>🌍 {self.config.APP_TITLE}</h1>
            <p>{self.config.APP_DESCRIPTION}</p>
            <p><em>Powered by AI Agents • Real-time Carbon Analysis • Personalized Action Plans</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the application sidebar"""
        with st.sidebar:
            st.header("🚀 EcoForge Control Panel")
            
            # API Status
            st.subheader("🔌 API Integration Status")
            api_status = self.config.get_api_status()
            
            for service, status in api_status.items():
                if service == "mock_mode":
                    continue
                icon = "✅" if status else "⚠️"
                status_text = "Connected" if status else "Mock Data"
                st.write(f"{icon} **{service.title()}**: {status_text}")
            
            if api_status["mock_mode"]:
                st.info("🎭 **Demo Mode Active** - Using realistic mock data for demonstration")
            
            st.divider()
            
            # Agent Status
            st.subheader("🤖 Agent Status")
            agent_names = ["Supervisor", "Home Expert", "Transport Expert", "Diet Expert", "Shopping Expert"]
            
            for agent in agent_names:
                status = st.session_state.agent_status.get(agent, "Idle")
                if status == "Active":
                    st.write(f"🟢 **{agent}**: {status}")
                elif status == "Processing":
                    st.write(f"🟡 **{agent}**: {status}")
                else:
                    st.write(f"⚪ **{agent}**: {status}")
            
            st.divider()
            
            # Memory Management
            st.subheader("🧠 Memory Management")
            if st.button("Clear Conversation History"):
                st.session_state.conversation_history = []
                st.session_state.current_analysis = None
                st.session_state.eco_score = 0
                st.success("Memory cleared!")
                st.rerun()
            
            # Show conversation count
            conv_count = len(st.session_state.conversation_history)
            st.write(f"📝 **Conversations**: {conv_count}")
    
    def render_3d_globe(self):
        """Render the 3D interactive globe"""
        st.subheader("🌍 Global Carbon Impact Visualization")
        
        # Create sample data for global visualization
        globe_data = pd.DataFrame({
            'lat': [35.6762, 40.7128, 51.5074, -33.8688, 55.7558],
            'lon': [139.6503, -74.0060, -0.1278, 151.2093, 37.6176],
            'city': ['Tokyo', 'New York', 'London', 'Sydney', 'Moscow'],
            'carbon_intensity': [518, 386, 254, 820, 450],
            'size': [100, 80, 60, 90, 70]
        })
        
        # Create 3D globe visualization
        view_state = pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1,
            pitch=50,
            bearing=0
        )
        
        # Carbon intensity layer
        carbon_layer = pdk.Layer(
            'ScatterplotLayer',
            data=globe_data,
            get_position='[lon, lat]',
            get_color='[carbon_intensity, 255-carbon_intensity, 100, 200]',
            get_radius='size * 1000',
            radius_scale=100,
            pickable=True,
            auto_highlight=True
        )
        
        # Agent activity layer (animated)
        if st.session_state.current_analysis:
            agent_data = pd.DataFrame({
                'lat': [35.6762 + np.random.normal(0, 5, 1)[0]],
                'lon': [139.6503 + np.random.normal(0, 5, 1)[0]],
                'activity': ['Analysis Active']
            })
            
            agent_layer = pdk.Layer(
                'ScatterplotLayer',
                data=agent_data,
                get_position='[lon, lat]',
                get_color='[0, 255, 136, 255]',
                get_radius=50000,
                radius_scale=1,
                pickable=True
            )
            
            deck = pdk.Deck(
                layers=[carbon_layer, agent_layer],
                initial_view_state=view_state,
                tooltip=True
            )
        else:
            deck = pdk.Deck(
                layers=[carbon_layer],
                initial_view_state=view_state,
                tooltip=True
            )
        
        st.pydeck_chart(deck, height=400)
    
    def render_eco_score_crystal(self):
        """Render the EcoScore crystal visualization"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            eco_score = st.session_state.eco_score
            
            # Create crystal-like visualization
            fig = go.Figure()
            
            # Crystal base
            fig.add_trace(go.Scatter(
                x=[0, 1, 2, 3, 4, 3, 2, 1, 0],
                y=[0, 1, 1, 2, 4, 6, 6, 5, 4],
                fill='tonexty',
                fillcolor=f'rgba(0, 255, 136, {eco_score/100})',
                line=dict(color='rgba(0, 255, 136, 1)', width=3),
                name='EcoScore Crystal'
            ))
            
            # Add glow effect
            for i in range(3):
                opacity = 0.3 - i * 0.1
                fig.add_trace(go.Scatter(
                    x=[0-i*0.1, 1-i*0.1, 2+i*0.1, 3+i*0.1, 4+i*0.1, 3+i*0.1, 2+i*0.1, 1-i*0.1, 0-i*0.1],
                    y=[0-i*0.1, 1-i*0.1, 1-i*0.1, 2-i*0.1, 4+i*0.2, 6+i*0.2, 6+i*0.2, 5+i*0.1, 4+i*0.2],
                    fill='tonexty',
                    fillcolor=f'rgba(0, 255, 136, {opacity})',
                    line=dict(color='rgba(0, 255, 136, 0)', width=0),
                    showlegend=False
                ))
            
            fig.update_layout(
                title=f"EcoScore: {eco_score}/100",
                title_font_size=24,
                title_font_color='rgba(0, 255, 136, 1)',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Score interpretation
            if eco_score >= 80:
                st.success("🌟 **Exceptional!** You're a sustainability champion!")
            elif eco_score >= 60:
                st.info("🌱 **Good Progress!** You're on the right track!")
            elif eco_score >= 40:
                st.warning("⚡ **Getting Started!** Room for improvement!")
            else:
                st.error("🚨 **High Impact!** Significant changes needed!")
    
    def render_agent_communication(self):
        """Render agent-to-agent communication visualization"""
        if not st.session_state.current_analysis:
            return
        
        st.subheader("🤖 Agent Communication Network")
        
        # Create agent network visualization
        agents = ["Supervisor", "Home", "Transport", "Diet", "Shopping", "Synthesizer"]
        
        # Create network graph
        fig = go.Figure()
        
        # Agent positions (circular layout)
        n_agents = len(agents)
        angles = np.linspace(0, 2*np.pi, n_agents, endpoint=False)
        x_pos = np.cos(angles)
        y_pos = np.sin(angles)
        
        # Add agent nodes
        fig.add_trace(go.Scatter(
            x=x_pos, y=y_pos,
            mode='markers+text',
            marker=dict(size=30, color='rgba(0, 255, 136, 0.8)', line=dict(width=2, color='white')),
            text=agents,
            textposition='middle center',
            textfont=dict(color='white', size=10),
            name='Agents'
        ))
        
        # Add communication lines (animated effect)
        for i in range(n_agents):
            for j in range(i+1, n_agents):
                if np.random.random() > 0.7:  # Random communication
                    fig.add_trace(go.Scatter(
                        x=[x_pos[i], x_pos[j]], y=[y_pos[i], y_pos[j]],
                        mode='lines',
                        line=dict(color='rgba(0, 255, 136, 0.3)', width=2),
                        showlegend=False
                    ))
        
        fig.update_layout(
            title="Real-time Agent Collaboration",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_carbon_analysis(self, analysis_result: Dict[str, Any]):
        """Render carbon footprint analysis results"""
        st.subheader("📊 Carbon Footprint Analysis")
        
        # Extract data from analysis
        total_footprint = analysis_result.get('total_carbon_footprint', 0)
        domain_breakdown = analysis_result.get('domain_breakdown', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Total footprint display
            st.markdown(f"""
            <div class="carbon-footprint">
                {total_footprint:.1f} tons CO2/year
            </div>
            """, unsafe_allow_html=True)
            
            # Comparison with global average
            global_avg = 4.8
            comparison = ((total_footprint / global_avg) - 1) * 100
            
            if comparison > 0:
                st.error(f"🔴 {comparison:.1f}% above global average")
            else:
                st.success(f"🟢 {abs(comparison):.1f}% below global average")
        
        with col2:
            # Domain breakdown pie chart
            if domain_breakdown:
                domains = list(domain_breakdown.keys())
                values = [domain_breakdown[d].get('carbon_footprint', 0) for d in domains]
                
                fig = px.pie(
                    values=values,
                    names=domains,
                    title="Emissions by Domain",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def render_action_plan(self, analysis_result: Dict[str, Any]):
        """Render personalized action plan"""
        st.subheader("🎯 Personalized Action Plan")
        
        prioritized_actions = analysis_result.get('prioritized_actions', [])
        
        if not prioritized_actions:
            st.warning("No actions generated yet. Please run an analysis first.")
            return
        
        # Display top actions
        for i, action in enumerate(prioritized_actions[:6]):
            with st.container():
                st.markdown(f"""
                <div class="action-card">
                    <h4>#{i+1} {action.get('action', 'Unknown Action')}</h4>
                    <p><strong>Impact:</strong> {action.get('co2_reduction', 'Unknown')}</p>
                    <p><strong>Feasibility:</strong> {action.get('feasibility', 'Medium')}</p>
                    <p><strong>Cost Impact:</strong> {action.get('cost_impact', 'Medium')}</p>
                    <p><strong>Domain:</strong> {action.get('domain', 'General')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    async def run_analysis(self, user_input: str):
        """Run the complete EcoForge analysis workflow"""
        
        # Update agent status
        st.session_state.agent_status = {
            "Supervisor": "Processing",
            "Home Expert": "Idle",
            "Transport Expert": "Idle", 
            "Diet Expert": "Idle",
            "Shopping Expert": "Idle"
        }
        
        # Create progress indicators
        progress_container = st.container()
        with progress_container:
            st.info("🚀 **Initializing AI Agents...**")
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        try:
            # Step 1: Initialize workflow
            status_text.text("🤖 Supervisor Agent analyzing your lifestyle...")
            progress_bar.progress(20)
            await asyncio.sleep(1)  # Simulate processing
            
            # Step 2: Parallel domain analysis
            status_text.text("🏠🚗🍽️🛍️ Domain experts working in parallel...")
            st.session_state.agent_status.update({
                "Home Expert": "Active",
                "Transport Expert": "Active",
                "Diet Expert": "Active", 
                "Shopping Expert": "Active"
            })
            progress_bar.progress(50)
            await asyncio.sleep(2)
            
            # Step 3: Synthesis
            status_text.text("🔄 Synthesizing cross-domain insights...")
            progress_bar.progress(70)
            await asyncio.sleep(1)
            
            # Step 4: Refinement
            status_text.text("✨ Refining recommendations...")
            progress_bar.progress(85)
            await asyncio.sleep(1)
            
            # Step 5: Final evaluation
            status_text.text("🎯 Finalizing your personalized plan...")
            progress_bar.progress(100)
            await asyncio.sleep(1)
            
            # Run actual workflow (with mock data for demo)
            analysis_result = await self.workflow.run_complete_analysis(user_input)
            
            # Update session state
            st.session_state.current_analysis = analysis_result
            st.session_state.eco_score = analysis_result.get('eco_score', 25)
            st.session_state.conversation_history.append({
                'timestamp': datetime.now(),
                'user_input': user_input,
                'analysis_result': analysis_result
            })
            
            # Reset agent status
            st.session_state.agent_status = {agent: "Idle" for agent in st.session_state.agent_status}
            
            # Clear progress indicators
            progress_container.empty()
            
            return analysis_result
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            progress_container.empty()
            return None
    
    def render_main_interface(self):
        """Render the main user interface"""
        
        # User input section
        st.subheader("💬 Tell us about your lifestyle")
        
        user_input = st.text_area(
            "Describe your daily life, home, transportation, diet, and shopping habits:",
            placeholder="Example: I live in Tokyo in a 2-bedroom apartment, drive a luxury SUV 20km daily, eat wagyu beef regularly, and shop for designer clothes monthly...",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button("🚀 **Analyze My Carbon Footprint**", use_container_width=True)
        
        if analyze_button and user_input:
            # Run analysis
            with st.spinner("🤖 AI Agents are analyzing your lifestyle..."):
                analysis_result = asyncio.run(self.run_analysis(user_input))
            
            if analysis_result:
                st.success("✅ **Analysis Complete!** Check your results below.")
                st.rerun()
        
        elif analyze_button and not user_input:
            st.warning("Please describe your lifestyle first!")
        
        # Display results if available
        if st.session_state.current_analysis:
            st.divider()
            
            # Carbon analysis
            self.render_carbon_analysis(st.session_state.current_analysis)
            
            st.divider()
            
            # Action plan
            self.render_action_plan(st.session_state.current_analysis)
    
    def run(self):
        """Run the complete EcoForge application"""
        
        # Render header
        self.render_header()
        
        # Render sidebar
        self.render_sidebar()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Main interface
            self.render_main_interface()
        
        with col2:
            # EcoScore crystal
            self.render_eco_score_crystal()
            
            st.divider()
            
            # Agent communication
            if Config.SHOW_AGENT_COMMUNICATION:
                self.render_agent_communication()
        
        # 3D Globe (full width)
        st.divider()
        self.render_3d_globe()
        
        # Footer
        st.divider()
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>🌍 <strong>EcoForge</strong> - Powered by AI Agents for Environmental Good</p>
            <p><em>Transform your lifestyle • Reduce your impact • Save the planet</em></p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = EcoForgeApp()
    app.run()