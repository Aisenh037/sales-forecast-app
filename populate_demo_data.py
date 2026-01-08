#!/usr/bin/env python3
"""
Populate demo data for AstralytiQ backend
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
import random

def populate_demo_data():
    """Populate the database with realistic demo data."""
    conn = sqlite3.connect("backend/astralytiq.db")
    cursor = conn.cursor()
    
    print("🗄️ Populating demo data...")
    
    # Clear existing demo data (except users)
    cursor.execute("DELETE FROM datasets")
    cursor.execute("DELETE FROM ml_models")
    cursor.execute("DELETE FROM dashboards")
    
    # Demo datasets
    datasets = [
        ("ds_001", "Customer Analytics Dataset 1", "CSV", 1250, 500000, 25, "Active", 0.95),
        ("ds_002", "Sales Performance Data Q4", "Parquet", 890, 250000, 18, "Active", 0.92),
        ("ds_003", "Marketing Campaign Results", "JSON", 340, 125000, 12, "Processing", 0.88),
        ("ds_004", "Product Inventory Tracking", "CSV", 2100, 750000, 35, "Active", 0.97),
        ("ds_005", "Customer Support Tickets", "CSV", 680, 180000, 22, "Active", 0.91),
        ("ds_006", "Financial Transactions Log", "Parquet", 3200, 1200000, 28, "Active", 0.99),
        ("ds_007", "Website Analytics Data", "JSON", 1800, 650000, 45, "Processing", 0.85),
        ("ds_008", "Supply Chain Metrics", "CSV", 950, 320000, 19, "Active", 0.94),
        ("ds_009", "Employee Performance Data", "CSV", 420, 85000, 16, "Archived", 0.89),
        ("ds_010", "IoT Sensor Readings", "Parquet", 5600, 2500000, 52, "Active", 0.96),
        ("ds_011", "Social Media Engagement", "JSON", 780, 450000, 31, "Active", 0.87),
        ("ds_012", "Quality Control Metrics", "CSV", 1100, 380000, 24, "Processing", 0.93),
        ("ds_013", "Logistics Optimization Data", "Parquet", 1450, 520000, 33, "Active", 0.98),
        ("ds_014", "Customer Feedback Analysis", "JSON", 620, 195000, 14, "Active", 0.90),
        ("ds_015", "Energy Consumption Patterns", "CSV", 2800, 980000, 41, "Active", 0.95)
    ]
    
    for dataset in datasets:
        cursor.execute("""
            INSERT INTO datasets (id, name, type, size_mb, rows, columns, status, quality_score, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, dataset)
    
    # Demo ML models
    models = [
        ("ml_001", "Deep Learning Model v2.1", "Deep Learning", 0.94, 0.92, 0.89, 0.90, "Deployed", 15420, 156, 2800),
        ("ml_002", "Random Forest Classifier", "Random Forest", 0.89, 0.87, 0.91, 0.89, "Deployed", 8750, 89, 1200),
        ("ml_003", "XGBoost Predictor v3.0", "Gradient Boosting", 0.92, 0.90, 0.88, 0.89, "Deployed", 12300, 134, 1800),
        ("ml_004", "Neural Network Ensemble", "Deep Learning", 0.96, 0.94, 0.93, 0.94, "Training", 0, 0, 0),
        ("ml_005", "SVM Classification Model", "Support Vector Machine", 0.87, 0.85, 0.89, 0.87, "Deployed", 5600, 201, 950),
        ("ml_006", "LSTM Time Series Model", "Recurrent Neural Network", 0.91, 0.89, 0.87, 0.88, "Deployed", 9800, 178, 2100),
        ("ml_007", "Logistic Regression v2", "Linear Model", 0.83, 0.81, 0.85, 0.83, "Deployed", 18500, 45, 450),
        ("ml_008", "Transformer NLP Model", "Transformer", 0.95, 0.93, 0.92, 0.93, "Testing", 0, 0, 0),
        ("ml_009", "Clustering Algorithm v1.5", "K-Means", 0.78, 0.76, 0.80, 0.78, "Deployed", 3200, 298, 680),
        ("ml_010", "Reinforcement Learning Agent", "Deep Q-Network", 0.88, 0.86, 0.84, 0.85, "Training", 0, 0, 0),
        ("ml_011", "Anomaly Detection System", "Isolation Forest", 0.90, 0.88, 0.86, 0.87, "Deployed", 7400, 167, 1350),
        ("ml_012", "Recommendation Engine v3", "Collaborative Filtering", 0.85, 0.83, 0.87, 0.85, "Deployed", 22100, 112, 3200)
    ]
    
    for i, model in enumerate(models):
        deployment_date = datetime.now() - timedelta(days=random.randint(1, 180)) if model[7] == "Deployed" else None
        cursor.execute("""
            INSERT INTO ml_models (id, name, type, accuracy, precision_score, recall_score, f1_score, 
                                 status, deployment_date, requests_per_day, avg_latency_ms, cost_per_month, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (*model, deployment_date))
    
    # Demo dashboards
    dashboards = [
        ("dash_001", "Executive Summary Dashboard", 12, 245, 15680, "Active", "1 minute"),
        ("dash_002", "Sales Performance Analytics", 8, 189, 8920, "Active", "5 minutes"),
        ("dash_003", "Customer Insights Portal", 15, 156, 12450, "Active", "2 minutes"),
        ("dash_004", "Operations Monitoring Hub", 20, 298, 22100, "Active", "30 seconds"),
        ("dash_005", "Financial KPI Dashboard", 10, 134, 9870, "Active", "10 minutes"),
        ("dash_006", "Marketing Campaign Tracker", 6, 87, 4560, "Active", "15 minutes"),
        ("dash_007", "Quality Control Center", 14, 203, 18900, "Active", "1 minute"),
        ("dash_008", "Supply Chain Overview", 9, 167, 11200, "Active", "5 minutes"),
        ("dash_009", "HR Analytics Dashboard", 7, 98, 6780, "Maintenance", "1 hour"),
        ("dash_010", "IT Infrastructure Monitor", 18, 312, 28900, "Active", "30 seconds"),
        ("dash_011", "Product Performance Metrics", 11, 145, 13400, "Active", "2 minutes"),
        ("dash_012", "Customer Support Analytics", 13, 178, 16700, "Active", "5 minutes")
    ]
    
    for dashboard in dashboards:
        cursor.execute("""
            INSERT INTO dashboards (id, name, widgets, views_today, views_total, status, refresh_rate, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """, dashboard)
    
    conn.commit()
    conn.close()
    
    print("✅ Demo data populated successfully!")
    print(f"   📊 {len(datasets)} datasets")
    print(f"   🤖 {len(models)} ML models")
    print(f"   📈 {len(dashboards)} dashboards")

if __name__ == "__main__":
    populate_demo_data()