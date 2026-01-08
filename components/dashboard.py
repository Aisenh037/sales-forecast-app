"""
📊 Dashboard Components
Main dashboard and analytics components
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def show_dashboard(demo_data):
    """Show the main dashboard with metrics and overview."""
    st.header("Platform Overview")
    
    metrics = demo_data['metrics']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Datasets</h3>
            <h2>{metrics['total_datasets']}</h2>
            <p>↗️ +3 this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Active Models</h3>
            <h2>{metrics['active_models']}</h2>
            <p>🚀 +2 deployed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Dashboards</h3>
            <h2>{metrics['total_dashboards']}</h2>
            <p>📊 All active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Data Processed</h3>
            <h2>{metrics['data_processed']}</h2>
            <p>📈 +15% this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.subheader("Platform Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Model performance chart
        models = demo_data['models']
        model_df = pd.DataFrame(models)
        
        fig = px.bar(
            model_df, 
            x='name', 
            y='accuracy',
            color='type',
            title="Model Performance Overview",
            labels={'accuracy': 'Accuracy Score', 'name': 'Model Name'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Dataset distribution
        datasets = demo_data['datasets']
        dataset_df = pd.DataFrame(datasets)
        
        fig = px.pie(
            dataset_df,
            names='type',
            title="Dataset Types Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent Activity")
    
    activities = [
        {"time": "2 minutes ago", "action": "Model 'Sales Predictor' deployed successfully", "type": "success"},
        {"time": "15 minutes ago", "action": "Dataset 'Customer Data Q4' uploaded", "type": "info"},
        {"time": "1 hour ago", "action": "Dashboard 'Revenue Analytics' updated", "type": "info"},
        {"time": "3 hours ago", "action": "Training job completed for 'Churn Model'", "type": "success"},
        {"time": "5 hours ago", "action": "New user 'john.doe@company.com' registered", "type": "info"}
    ]
    
    for activity in activities:
        icon = "✅" if activity["type"] == "success" else "ℹ️"
        st.markdown(f"{icon} **{activity['time']}** - {activity['action']}")

def show_analytics(demo_data):
    """Show analytics and reporting interface."""
    st.header("Analytics & Reporting")
    
    tab1, tab2, tab3 = st.tabs(["Dashboards", "Reports", "Data Explorer"])
    
    with tab1:
        st.subheader("Interactive Dashboards")
        
        dashboards = demo_data['dashboards']
        
        # Dashboard grid
        cols = st.columns(2)
        for i, dashboard in enumerate(dashboards):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {dashboard['name']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Widgets", dashboard['widgets'])
                        st.metric("Views", f"{dashboard['views']:,}")
                    with col2:
                        st.metric("Last Updated", dashboard['last_updated'].strftime("%H:%M"))
                        st.metric("Status", dashboard['status'])
                    
                    if st.button(f"Open Dashboard", key=f"open_dash_{dashboard['id']}"):
                        st.success(f"Opening {dashboard['name']}...")
                    
                    st.divider()
    
    with tab2:
        st.subheader("Automated Reports")
        st.info("Report generation features coming soon!")
    
    with tab3:
        st.subheader("Data Explorer")
        st.info("Interactive data exploration features coming soon!")