import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

# Load the dataset from a CSV file (update the path accordingly)
file_path = "E:/gitrepo/art_daily_nojump.csv"  # Update with the correct path to your CSV file

# Check if the file exists
if os.path.exists(file_path):
    # Load the dataset from the CSV file
    df = pd.read_csv(file_path)

    # Print the first few rows of the dataset to check the structure
    print("Dataset loaded successfully:")
    print(df.head())  # Check the first few rows of the dataset

    # Only use CPU usage for anomaly detection (assuming the column is named 'cpu_usage')
    if 'cpu_usage' not in df.columns:
        print("Error: 'cpu_usage' column not found in the dataset.")
    else:
        # Extract the 'cpu_usage' column for clustering (since we only use CPU usage for the detection)
        sample_data = df[['cpu_usage']].values.tolist()

        # Initialize the scaler
        scaler = StandardScaler()

        # Initialize KMeans Model (for anomaly detection)
        kmeans = KMeans(n_clusters=2, random_state=42)  # 2 clusters: normal and anomaly

        # Fit the scaler and KMeans model to the sample data
        scaler.fit(sample_data)  # Fit the scaler to the sample data
        scaled_data = scaler.transform(sample_data)  # Scale the data
        kmeans.fit(scaled_data)  # Fit the KMeans model to the scaled data

        # Real-time monitoring loop - Simulating the data from the table
        for idx, data in enumerate(sample_data):
            cpu_usage = data[0]  # Extract CPU usage value from the tuple

            # Simulate scaling the new data (like we would do in real-time)
            new_data = np.array([[cpu_usage]])  # Collect real-time data for CPU usage
            new_data_scaled = scaler.transform(new_data)  # Scale the new data using the scaler

            # Anomaly detection using KMeans model
            label = kmeans.predict(new_data_scaled)  # Predict if the data point is an anomaly (1) or normal (0)

            # Check if the model predicted an anomaly
            if label == 1:  # If the predicted label is 1 (anomaly detected)
                print(f"Anomaly detected at index {idx}! CPU Usage: {cpu_usage}%")
            else:
                print(f"Normal data at index {idx}: CPU Usage: {cpu_usage}%")

            time.sleep(1)  # Simulate a small delay (e.g., 1 second between data points for real-time simulation)

