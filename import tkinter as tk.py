import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pickle
import cv2

# Global variables to store file paths
dataset_path = None
test_image_path = None

def browse_training_dataset():
    global dataset_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        dataset_path = file_path
        messagebox.showinfo("Dataset Loaded", f"Dataset loaded from {file_path}")

def train_dataset():
    if not dataset_path:
        messagebox.showwarning("Warning", "Please load the dataset first.")
        return

    df = pd.read_csv(dataset_path)
    X = df[['R', 'G', 'B']].values
    y = df['Soil_pH'].values

    # Standardize the data
    X_scaled = StandardScaler().fit_transform(X)

    # Apply PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X_scaled)

    # Train a simple model (e.g., Linear Regression) on principal components
    model = LinearRegression()
    model.fit(principal_components, y)

    # Save the model for later use
    with open('pca_model.pkl', 'wb') as file:
        pickle.dump(model, file)

    messagebox.showinfo("Training Complete", "PCA Model has been trained and saved.")

def browse_test_image():
    global test_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        test_image_path = file_path
        messagebox.showinfo("Test Image Loaded", f"Test image loaded from {file_path}")

def crop_image():
    if not test_image_path:
        messagebox.showwarning("Warning", "Please load the test image first.")
        return

    image = cv2.imread(test_image_path)
    # For simplicity, crop a fixed region of the image (e.g., top-left corner)
    cropped_image = image[0:100, 0:100]
    
    # Save cropped image
    cv2.imwrite('cropped_image.jpg', cropped_image)
    messagebox.showinfo("Crop Complete", "Image has been cropped.")

def perform_pca_recognition():
    if not test_image_path:
        messagebox.showwarning("Warning", "Please load the test image first.")
        return

    # Load the model
    with open('pca_model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    # Process the image
    image = cv2.imread(test_image_path)
    avg_color_per_row = cv2.mean(image)
    avg_color = [avg_color_per_row[2], avg_color_per_row[1], avg_color_per_row[0]]  # BGR to RGB

    # Apply PCA and model prediction
    X = [avg_color]
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X_scaled)
    pH_value = model.predict(principal_components)[0]

    final_output_pca_entry.delete(0, tk.END)
    final_output_pca_entry.insert(0, str(pH_value))

def perform_color_based_recognition():
    if not test_image_path:
        messagebox.showwarning("Warning", "Please load the test image first.")
        return

    image = cv2.imread(test_image_path)
    avg_color_per_row = cv2.mean(image)
    avg_color = [avg_color_per_row[2], avg_color_per_row[1], avg_color_per_row[0]]  # BGR to RGB
    
    # Map avg_color to a pH value (this is a simple approach)
    pH_value = map_rgb_to_ph(avg_color)
    final_output_ph_entry.delete(0, tk.END)
    final_output_ph_entry.insert(0, str(pH_value))

def map_rgb_to_ph(rgb):
    # Placeholder function - implement the actual mapping
    r, g, b = rgb
    if r > 150 and g < 100 and b < 100:
        return 5.5
    elif r < 100 and g > 150 and b < 100:
        return 7.0
    elif r < 100 and g < 100 and b > 150:
        return 8.5
    else:
        return 7.0  # Default pH

def find_suitable_crops():
    pH_value = final_output_ph_entry.get()
    if not pH_value:
        messagebox.showwarning("Warning", "Please perform color-based recognition first.")
        return
    
    pH_value = float(pH_value)
    
    # Suggest crops based on pH value
    if pH_value < 6.0:
        crops = "Crops suitable for acidic soil."
    elif 6.0 <= pH_value <= 7.5:
        crops = "Crops suitable for neutral soil."
    else:
        crops = "Crops suitable for alkaline soil."

    messagebox.showinfo("Suitable Crops", crops)

# Set up the main window
root = tk.Tk()
root.title("DETERMINATION OF SOIL pH")
root.geometry("800x400")

# Input Image Section
input_image_label = tk.Label(root, text="INPUT IMAGE")
input_image_label.place(x=250, y=20)

# Training Section
train_section_label = tk.Label(root, text="Training Section")
train_section_label.place(x=30, y=20)

browse_training_button = tk.Button(root, text="Browse Training Dataset", command=browse_training_dataset)
browse_training_button.place(x=30, y=50)

train_dataset_button = tk.Button(root, text="Train Dataset", command=train_dataset)
train_dataset_button.place(x=30, y=90)

# Testing Section
test_section_label = tk.Label(root, text="Testing Section")
test_section_label.place(x=30, y=160)

browse_test_image_button = tk.Button(root, text="Browse Test Image", command=browse_test_image)
browse_test_image_button.place(x=30, y=190)

crop_image_button = tk.Button(root, text="Crop Image", command=crop_image)
crop_image_button.place(x=30, y=230)

pca_recognition_button = tk.Button(root, text="Perform PCA Recognition", command=perform_pca_recognition)
pca_recognition_button.place(x=30, y=270)

color_based_recognition_button = tk.Button(root, text="Perform Color Based Recognition", command=perform_color_based_recognition)
color_based_recognition_button.place(x=30, y=310)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.place(x=30, y=350)

# Feature Extraction Section
feature_extraction_label = tk.Label(root, text="FEATURE EXTRACTION SECTION")
feature_extraction_label.place(x=550, y=20)

r_index_label = tk.Label(root, text="R INDEX")
r_index_label.place(x=550, y=60)

g_index_label = tk.Label(root, text="G INDEX")
g_index_label.place(x=550, y=100)

b_index_label = tk.Label(root, text="B INDEX")
b_index_label.place(x=550, y=140)

# Color Based Results
color_based_results_label = tk.Label(root, text="Color Based Results")
color_based_results_label.place(x=300, y=270)

final_output_ph_label = tk.Label(root, text="FINAL OUTPUT (pH)")
final_output_ph_label.place(x=300, y=310)

final_output_ph_entry = tk.Entry(root)
final_output_ph_entry.place(x=450, y=310)

# PCA Based Results
pca_based_results_label = tk.Label(root, text="PCA Based Results")
pca_based_results_label.place(x=300, y=350)

final_output_pca_entry = tk.Entry(root)
final_output_pca_entry.place(x=450, y=350)

# Button to find suitable crops
find_crops_button = tk.Button(root, text="Find Suitable Crops", command=find_suitable_crops)
find_crops_button.place(x=600, y=310)

root.mainloop()


