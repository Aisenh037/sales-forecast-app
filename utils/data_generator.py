"""
🎲 Data Generation Utilities
Generate demo data for the platform
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_demo_data():
    """Generate comprehensive demo data for the platform."""
    np.random.seed(42)
    
    # Generate sample datasets
    datasets = []
    for i in range(12):
        datasets.append({
            'id': f'dataset_{i+1}',
            'name': f'Dataset {i+1}',
            'type': np.random.choice(['CSV', 'JSON', 'Parquet', 'Excel']),
            'size': f"{np.random.randint(1, 500)} MB",
            'rows': np.random.randint(1000, 100000),
            'columns': np.random.randint(5, 50),
            'created': datetime.now() - timedelta(days=np.random.randint(1, 365)),
            'status': np.random.choice(['Active', 'Processing', 'Archived'], p=[0.7, 0.2, 0.1])
        })
    
    # Generate ML models
    models = []
    model_types = ['Classification', 'Regression', 'Clustering', 'Deep Learning', 'Time Series']
    for i in range(8):
        models.append({
            'id': f'model_{i+1}',
            'name': f'Model {i+1}',
            'type': np.random.choice(model_types),
            'accuracy': np.random.uniform(0.75, 0.98),
            'status': np.random.choice(['Training', 'Deployed', 'Failed', 'Completed'], p=[0.2, 0.5, 0.1, 0.2]),
            'created': datetime.now() - timedelta(days=np.random.randint(1, 180)),
            'dataset': f'Dataset {np.random.randint(1, 12)}'
        })
    
    # Generate dashboards
    dashboards = []
    for i in range(6):
        dashboards.append({
            'id': f'dashboard_{i+1}',
            'name': f'Analytics Dashboard {i+1}',
            'widgets': np.random.randint(3, 12),
            'views': np.random.randint(100, 5000),
            'last_updated': datetime.now() - timedelta(hours=np.random.randint(1, 48)),
            'status': 'Active'
        })
    
    return {
        'datasets': datasets,
        'models': models,
        'dashboards': dashboards,
        'metrics': {
            'total_datasets': len(datasets),
            'active_models': len([m for m in models if m['status'] == 'Deployed']),
            'total_dashboards': len(dashboards),
            'data_processed': f"{np.random.randint(50, 500)} GB",
            'api_calls_today': np.random.randint(1000, 10000),
            'uptime': "99.9%"
        }
    }