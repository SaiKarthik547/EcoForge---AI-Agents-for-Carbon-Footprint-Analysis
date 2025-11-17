import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import time
from langsmith import Client
import os

class ObservabilityPanel:
    """CAPSTONE: Real-time Observability and Monitoring Dashboard"""
    
    def __init__(self):
        self.traces = []
        self.metrics = {
            'agent_performance': {},
            'workflow_timing': {},
            'api_calls': {},
            'memory_usage': {}
        }
        
        # Initialize LangSmith client for tracing
        try:
            self.langsmith_client = Client(api_key=os.getenv("LANGSMITH_API_KEY", "demo_key"))
        except:
            self.langsmith_client = None
    
    def log_trace(self, agent_name: str, action: str, duration: float, status: str = "success", metadata: Dict[str, Any] = {}):
        """CAPSTONE: LangSmith Integration for Agent Tracing"""
        
        trace_data = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_name,
            'action': action,
            'duration': duration,
            'status': status,
            'metadata': metadata or {}
        }
        
        self.traces.append(trace_data)
        
        # Send to LangSmith if available
        if self.langsmith_client:
            try:
                self.langsmith_client.create_run(
                    name=f"{agent_name}_{action}",
                    run_type="llm",
                    inputs={"action": action, "agent": agent_name},
                    outputs={"status": status, "duration": duration},
                    extra=metadata
                )
            except:
                pass  # Graceful fallback
    
    def update_metrics(self, metric_type: str, key: str, value: Any):
        """Update real-time metrics"""
        
        if metric_type not in self.metrics:
            self.metrics[metric_type] = {}
        
        self.metrics[metric_type][key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
    
    def display_panel(self):
        """CAPSTONE: Real-time Observability Dashboard"""
        
        st.markdown("#### 🔍 Live Agent Monitoring")
        
        # Real-time metrics
        if self.metrics:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Active Agents", 
                    len(self.metrics.get('agent_performance', {})),
                    delta=1 if self.metrics.get('agent_performance') else 0
                )
            
            with col2:
                total_traces = len(self.traces)
                st.metric(
                    "Total Operations", 
                    total_traces,
                    delta=1 if total_traces > 0 else 0
                )
        
        # Agent performance visualization
        if self.traces:
            self._display_agent_performance_chart()
        
        # Live trace log
        self._display_live_traces()
        
        # API call monitoring
        self._display_api_monitoring()
        
        # Memory usage tracking
        self._display_memory_tracking()
    
    def _display_agent_performance_chart(self):
        """Real-time agent performance visualization"""
        
        st.markdown("##### ⚡ Agent Performance")
        
        # Aggregate performance data
        agent_stats = {}
        for trace in self.traces[-20:]:  # Last 20 traces
            agent = trace['agent']
            if agent not in agent_stats:
                agent_stats[agent] = {'count': 0, 'avg_duration': 0, 'success_rate': 0}
            
            agent_stats[agent]['count'] += 1
            agent_stats[agent]['avg_duration'] += trace['duration']
            if trace['status'] == 'success':
                agent_stats[agent]['success_rate'] += 1
        
        # Calculate averages
        for agent, stats in agent_stats.items():
            if stats['count'] > 0:
                stats['avg_duration'] /= stats['count']
                stats['success_rate'] = (stats['success_rate'] / stats['count']) * 100
        
        if agent_stats:
            # Create performance chart
            agents = list(agent_stats.keys())
            durations = [agent_stats[agent]['avg_duration'] for agent in agents]
            success_rates = [agent_stats[agent]['success_rate'] for agent in agents]
            
            fig = go.Figure()
            
            # Duration bars
            fig.add_trace(go.Bar(
                name='Avg Duration (s)',
                x=agents,
                y=durations,
                yaxis='y',
                marker_color='rgba(0, 255, 136, 0.7)'
            ))
            
            # Success rate line
            fig.add_trace(go.Scatter(
                name='Success Rate (%)',
                x=agents,
                y=success_rates,
                yaxis='y2',
                mode='lines+markers',
                line=dict(color='#00d4ff', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title='Agent Performance Metrics',
                xaxis=dict(title='Agents'),
                yaxis=dict(title='Duration (seconds)', side='left'),
                yaxis2=dict(title='Success Rate (%)', side='right', overlaying='y'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#00ff88'),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_live_traces(self):
        """Live trace monitoring"""
        
        st.markdown("##### 📊 Live Trace Log")
        
        if self.traces:
            # Display last 10 traces
            recent_traces = self.traces[-10:]
            
            for trace in reversed(recent_traces):
                status_color = "#00ff88" if trace['status'] == 'success' else "#ff0080"
                
                st.markdown(f"""
                <div style="
                    background: rgba(0, 255, 136, 0.1);
                    border-left: 4px solid {status_color};
                    padding: 10px;
                    margin: 5px 0;
                    border-radius: 5px;
                ">
                    <strong>{trace['agent']}</strong> → {trace['action']}<br>
                    <small>Duration: {trace['duration']:.2f}s | Status: {trace['status']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No traces available yet. Start an analysis to see live monitoring.")
    
    def _display_api_monitoring(self):
        """API call monitoring and rate limiting"""
        
        st.markdown("##### 🌐 API Monitoring")
        
        api_calls = self.metrics.get('api_calls', {})
        
        if api_calls:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                climatiq_calls = api_calls.get('climatiq', {}).get('value', 0)
                st.metric("Climatiq API", climatiq_calls, delta=1 if climatiq_calls > 0 else 0)
            
            with col2:
                tavily_calls = api_calls.get('tavily', {}).get('value', 0)
                st.metric("Tavily Search", tavily_calls, delta=1 if tavily_calls > 0 else 0)
            
            with col3:
                weather_calls = api_calls.get('weather', {}).get('value', 0)
                st.metric("Weather API", weather_calls, delta=1 if weather_calls > 0 else 0)
        else:
            st.info("API monitoring will appear during agent execution.")
    
    def _display_memory_tracking(self):
        """Memory usage and optimization tracking"""
        
        st.markdown("##### 🧠 Memory Tracking")
        
        memory_stats = self.metrics.get('memory_usage', {})
        
        if memory_stats:
            conversations = memory_stats.get('conversations', {}).get('value', 0)
            compacted = memory_stats.get('compacted', {}).get('value', 0)
            efficiency = (compacted / max(conversations, 1)) * 100
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Conversations", conversations)
            
            with col2:
                st.metric("Memory Efficiency", f"{efficiency:.1f}%")
            
            # Memory efficiency gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = efficiency,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Memory Efficiency"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#00ff88"},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(255, 0, 128, 0.3)"},
                        {'range': [50, 80], 'color': "rgba(255, 255, 0, 0.3)"},
                        {'range': [80, 100], 'color': "rgba(0, 255, 136, 0.3)"}
                    ]
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "#00ff88"},
                height=200
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Memory tracking will appear after conversations are stored.")
    
    def start_workflow_trace(self, workflow_id: str):
        """Start tracing a complete workflow"""
        
        self.log_trace(
            agent_name="WorkflowManager",
            action="start_workflow",
            duration=0.0,
            status="started",
            metadata={"workflow_id": workflow_id}
        )
    
    def end_workflow_trace(self, workflow_id: str, total_duration: float):
        """End workflow tracing"""
        
        self.log_trace(
            agent_name="WorkflowManager",
            action="complete_workflow",
            duration=total_duration,
            status="success",
            metadata={"workflow_id": workflow_id}
        )
    
    def log_agent_communication(self, sender: str, receiver: str, message_type: str):
        """CAPSTONE: Log A2A communication for observability"""
        
        self.log_trace(
            agent_name="CommunicationHub",
            action="agent_message",
            duration=0.1,
            status="success",
            metadata={
                "sender": sender,
                "receiver": receiver,
                "message_type": message_type
            }
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        
        if not self.traces:
            return {"status": "no_data"}
        
        total_operations = len(self.traces)
        successful_operations = len([t for t in self.traces if t['status'] == 'success'])
        avg_duration = sum(t['duration'] for t in self.traces) / total_operations
        
        return {
            "total_operations": total_operations,
            "success_rate": (successful_operations / total_operations) * 100,
            "average_duration": avg_duration,
            "active_agents": len(set(t['agent'] for t in self.traces))
        }