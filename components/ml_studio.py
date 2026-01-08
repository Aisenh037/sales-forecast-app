"""
🤖 ML Studio Components
Machine learning model training, deployment, and monitoring
"""

import streamlit as st
import pandas as pd
import numpy as np
import time

def show_ml_studio(demo_data, user_level):
    """Show ML Studio interface."""
    st.header("ML Studio")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Model Training", "Model Registry", "Deployment", "Monitoring"])
    
    with tab1:
        st.subheader("Train New Model")
        
        # Model configuration
        col1, col2 = st.columns(2)
        
        with col1:
            model_name = st.text_input("Model Name", placeholder="My Awesome Model")
            dataset = st.selectbox("Select Dataset", [d['name'] for d in demo_data['datasets']])
            model_type = st.selectbox("Model Type", ["Classification", "Regression", "Clustering", "Deep Learning", "Time Series"])
        
        with col2:
            target_column = st.text_input("Target Column", placeholder="target")
            test_size = st.slider("Test Size (%)", 10, 40, 20)
            auto_ml = st.checkbox("Enable AutoML", help="Automatically select best algorithm and hyperparameters")
        
        # Advanced settings (for intermediate/advanced users)
        if user_level in ['Intermediate', 'Advanced']:
            with st.expander("Advanced Settings"):
                col1, col2 = st.columns(2)
                with col1:
                    st.selectbox("Algorithm", ["Auto", "Random Forest", "XGBoost", "Neural Network", "SVM"])
                    st.slider("Cross-validation folds", 3, 10, 5)
                with col2:
                    st.selectbox("Optimization metric", ["Accuracy", "F1-Score", "ROC-AUC", "RMSE"])
                    st.number_input("Max training time (minutes)", 1, 120, 30)
        
        if st.button("Start Training"):
            st.markdown("""
            <div class="success-card">
                <h4>Training Started!</h4>
                <p>Your model training has been queued. You'll receive notifications when complete.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate training progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            training_steps = [
                "Preparing data...",
                "Feature engineering...",
                "Model selection...",
                "Training model...",
                "Validating results...",
                "Finalizing model..."
            ]
            
            for i, step in enumerate(training_steps):
                status_text.text(step)
                progress_bar.progress((i + 1) / len(training_steps))
                time.sleep(0.8)
            
            st.success("✅ Model training completed! Check the Model Registry for results.")
    
    with tab2:
        st.subheader("Model Registry")
        
        models = demo_data['models']
        
        # Model filters
        col1, col2, col3 = st.columns(3)
        with col1:
            type_filter = st.selectbox("Filter by type", ["All"] + list(set([m['type'] for m in models])))
        with col2:
            status_filter = st.selectbox("Filter by status", ["All", "Training", "Deployed", "Failed", "Completed"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Name", "Accuracy", "Created Date"])
        
        # Display models
        for model in models:
            if (type_filter == "All" or model['type'] == type_filter) and \
               (status_filter == "All" or model['status'] == status_filter):
                
                with st.expander(f"{model['name']} ({model['type']})"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Accuracy", f"{model['accuracy']:.2%}")
                    with col2:
                        st.metric("Status", model['status'])
                    with col3:
                        st.metric("Dataset", model['dataset'])
                    with col4:
                        st.metric("Created", model['created'].strftime("%Y-%m-%d"))
                    
                    # Action buttons
                    button_col1, button_col2, button_col3 = st.columns(3)
                    with button_col1:
                        if st.button("View Details", key=f"details_{model['id']}"):
                            st.info(f"Opening detailed view for {model['name']}")
                    with button_col2:
                        if model['status'] == 'Completed' and st.button("Deploy", key=f"deploy_{model['id']}"):
                            st.success(f"Deploying {model['name']}...")
                    with button_col3:
                        if st.button("Compare", key=f"compare_{model['id']}"):
                            st.info("Opening model comparison tool...")
    
    with tab3:
        st.subheader("Model Deployment")
        
        deployed_models = [m for m in demo_data['models'] if m['status'] == 'Deployed']
        
        if deployed_models:
            st.markdown("### Active Deployments")
            
            for model in deployed_models:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{model['name']}**")
                        st.caption(f"{model['type']} • Accuracy: {model['accuracy']:.2%}")
                    
                    with col2:
                        st.metric("Requests/day", f"{np.random.randint(100, 1000)}")
                    
                    with col3:
                        st.metric("Avg Response", f"{np.random.randint(50, 200)}ms")
                    
                    with col4:
                        if st.button("Manage", key=f"manage_{model['id']}"):
                            st.info(f"Opening management panel for {model['name']}")
                    
                    st.divider()
        
        else:
            st.info("No models currently deployed. Train and deploy a model from the Model Registry.")
    
    with tab4:
        st.subheader("Model Monitoring")
        st.info("Model monitoring and performance tracking features coming soon!")