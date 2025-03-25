import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os  # Import the os module for file handling

# Load the dataset from a CSV file (update the path accordingly)
file_path = "E:/gitrepo/art_daily_nojump.csv"  # Update with your actual path to the CSV file

# Check if the file exists
if os.path.exists(file_path):
    # Load the dataset directly from the CSV file
    df = pd.read_csv(file_path)

    # Print the first few rows of the dataset to check the structure
    print("Dataset loaded successfully:")
    print(df.head())  # Check the first few rows of the dataset

    # Step 1: Preprocess Data (Use only 'cpu_usage' for clustering)
    if 'cpu_usage' not in df.columns:
        print("Error: 'cpu_usage' column not found in the dataset.")
    else:
        # Extract the 'cpu_usage' column for clustering
        X = df[['cpu_usage']]

        # Step 2: Normalize the feature (Scaling)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Step 3: Fit K-Means Model
        kmeans = KMeans(n_clusters=2, random_state=42)  # Using 2 clusters
        kmeans.fit(X_scaled)

        # Step 4: Predict Clusters
        labels = kmeans.predict(X_scaled)

        # Step 5: Identify Anomalies (assuming label 1 is the anomaly cluster)
        anomalies = [i for i, label in enumerate(labels) if label == 1]
        print(f"Anomalies detected at indices: {anomalies}")

        # Optionally, print the cluster centers
        print("Cluster Centers (scaled features):")
        print(kmeans.cluster_centers_)

        # Optionally, visualize the clusters
        plt.scatter(X_scaled[:, 0], np.zeros_like(X_scaled[:, 0]), c=labels, cmap='viridis')
        plt.title("K-Means Clustering (scaled CPU Usage)")
        plt.xlabel('CPU Usage (scaled)')
        plt.ylabel('Cluster Label')
        plt.colorbar(label='Cluster Label')
        plt.show()

else:
    print(f"Error: The file at {file_path} does not exist.")
