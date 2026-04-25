# 🧠 Smart Image Organizer

An AI-powered web application that automatically classifies and organizes images into meaningful categories using deep learning. Built with **Streamlit**, **PyTorch**, and **EfficientNet**, this tool helps users manage large collections of images effortlessly.

---

## 🚀 Features

* 🔍 **Automatic Image Classification**
  Uses a trained EfficientNet model to categorize images into:

  * Documents
  * Educational
  * Others
  * Personal
  * Screenshots

* 📤 **Flexible Upload Options**

  * Upload multiple images (PNG, JPG, JPEG)
  * Upload entire folders via ZIP

* ⚡ **Real-Time AI Predictions**

  * Instant classification with confidence scores
  * Highlights low-confidence predictions (<70%)

* ✏️ **Manual Review & Editing**

  * Change predicted categories
  * Delete unwanted images
  * Interactive UI for easy corrections

* 🔎 **Smart Filtering**

  * Search by filename
  * Filter by category
  * View only low-confidence predictions

* 📊 **Data Visualization**

  * Interactive pie chart showing category distribution (Plotly)

* 📦 **Export Functionality**

  * Download all images as a structured ZIP file
  * Automatically sorted into category folders

* 🧹 **Session Management**

  * Clear all images in one click
  * Prevent duplicate uploads using hashing

---
## 🧠 Model Details

* **Architecture:** EfficientNet-B3
* **Library:** `timm`
* **Framework:** PyTorch
* **Classes:** 5 image categories
* **Inference:** Softmax probability with confidence score

---

## 📂 Project Structure

```bash
.
├── app.py                      # Main Streamlit application
├── best_model.pth             # Trained model weights
├── README.md                  # Project documentation
├── requirements.txt           # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/anuja-gutte/Image-Classifier-and-Organiser.git
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add model file

Place your trained model file:

```bash
best_model.pth
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📦 Requirements

* Python 3.8+
* Streamlit
* PyTorch
* torchvision
* timm
* Pillow
* pandas
* plotly

---

## 🧪 How It Works

1. User uploads images or ZIP folder
2. Images are preprocessed using torchvision transforms
3. Model predicts category using EfficientNet
4. Confidence score is calculated via Softmax
5. Images are displayed and grouped by category
6. User can edit, filter, and export results

---

## 🧠 Key Concepts Used

* Deep Learning (CNN – EfficientNet)
* Image Preprocessing
* Softmax Classification
* Hashing for duplicate detection
* Streamlit state management
* Interactive UI design
* Data visualization (Plotly)

---

## 🔮 Future Improvements

* Add custom category training
* Enable drag-and-drop folder upload
* Deploy as a full-stack app (React + FastAPI)
* Add cloud storage integration
* Improve model accuracy with larger dataset

---

## 📸 Use Cases

* Organizing personal photo collections
* Managing screenshots and documents
* Cleaning messy image folders
* Preprocessing datasets for ML projects

---

Streamlit Deployment Link: https://image-classifier-and-organiser.streamlit.app/

