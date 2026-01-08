"""
📊 Data Management Components
Data upload, processing, and management interfaces
"""

import streamlit as st
import pandas as pd
import time

def show_data_management(demo_data, auth_manager=None):
    """Show data management interface."""
    st.header("Data Management")
    
    tab1, tab2, tab3 = st.tabs(["Datasets", "Upload Data", "Data Processing"])
    
    with tab1:
        st.subheader("Your Datasets")
        
        datasets = demo_data['datasets']
        dataset_df = pd.DataFrame(datasets)
        
        # Search and filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search datasets...", placeholder="Enter dataset name or type")
        with col2:
            status_filter = st.selectbox("Filter by status", ["All", "Active", "Processing", "Archived"])
        
        # Filter datasets
        filtered_df = dataset_df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False)]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        # Display datasets
        for _, dataset in filtered_df.iterrows():
            with st.expander(f"{dataset['name']} ({dataset['type']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Size", dataset['size'])
                    st.metric("Rows", f"{dataset['rows']:,}")
                with col2:
                    st.metric("Columns", dataset['columns'])
                    st.metric("Status", dataset['status'])
                with col3:
                    st.metric("Created", dataset['created'].strftime("%Y-%m-%d"))
                    if st.button(f"View Details", key=f"view_{dataset['id']}"):
                        st.success(f"Opening {dataset['name']} details...")
    
    with tab2:
        st.subheader("Upload New Dataset")
        
        upload_method = st.radio("Choose upload method:", ["File Upload", "URL Import", "Database Connection"])
        
        if upload_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'json', 'parquet'],
                help="Supported formats: CSV, Excel, JSON, Parquet"
            )
            
            if uploaded_file:
                # Enhanced upload with production storage
                if auth_manager and auth_manager.get_integration_status()["cloudinary"]:
                    with st.spinner("Uploading to cloud storage..."):
                        try:
                            file_url = auth_manager.upload_file(
                                uploaded_file.getvalue(), 
                                folder="datasets"
                            )
                            if file_url:
                                st.success(f"✅ File '{uploaded_file.name}' uploaded to cloud storage!")
                                st.info(f"🔗 Cloud URL: {file_url}")
                            else:
                                st.warning("⚠️ Cloud upload failed, using local processing")
                        except Exception as e:
                            st.error(f"❌ Upload error: {str(e)}")
                else:
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                
                # Show preview
                if uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                    st.subheader("Data Preview")
                    st.dataframe(df.head())
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Rows", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
        
        elif upload_method == "URL Import":
            url = st.text_input("Enter data URL:", placeholder="https://example.com/data.csv")
            if url and st.button("Import from URL"):
                st.success("Data imported successfully from URL!")
        
        else:  # Database Connection
            col1, col2 = st.columns(2)
            with col1:
                db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "MongoDB", "SQLite"])
                host = st.text_input("Host", placeholder="localhost")
            with col2:
                port = st.text_input("Port", placeholder="5432")
                database = st.text_input("Database Name")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Test Connection"):
                st.success("Connection successful!")
    
    with tab3:
        st.subheader("Data Processing Pipeline")
        
        st.markdown("""
        <div class="info-card">
            <h4>Automated Data Processing</h4>
            <p>Configure automated data cleaning, transformation, and validation pipelines.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Processing options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Cleaning Options:**")
            st.checkbox("Remove duplicates")
            st.checkbox("Handle missing values")
            st.checkbox("Normalize data types")
            st.checkbox("Validate data quality")
        
        with col2:
            st.markdown("**Transformation Options:**")
            st.checkbox("Feature scaling")
            st.checkbox("Encoding categorical variables")
            st.checkbox("Feature engineering")
            st.checkbox("Data aggregation")
        
        if st.button("Start Processing Pipeline"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = ["Validating data", "Cleaning records", "Applying transformations", "Quality checks", "Finalizing"]
            for i, step in enumerate(steps):
                status_text.text(f"Processing: {step}...")
                progress_bar.progress((i + 1) / len(steps))
                time.sleep(0.5)
            
            st.success("✅ Data processing completed successfully!")