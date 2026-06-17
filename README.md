# 🐦 Pigeon Detection & Counting — YOLOv8

> A real-time pigeon detection and counting system powered by **YOLOv8** and served via a **FastAPI** web application. Upload any image and instantly get annotated results with bounding boxes and pigeon counts.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

This project fine-tunes the **YOLOv8 nano** (`yolov8n`) model on a custom annotated dataset of **490 pigeon images** to accurately detect, localize, and count pigeons in images. The trained model is deployed as a FastAPI web service with a clean HTML/JS frontend.

---

## ✨ Features

- 🔍 **Real-time detection** — detects pigeons in uploaded images within milliseconds
- 🔢 **Automatic counting** — returns the exact count of pigeons found
- 🎨 **Custom annotations** — draws pink bounding boxes with sequential labels (`#1`, `#2`, ...)
- ⚙️ **Configurable thresholds** — adjustable Confidence (`conf`) and IoU thresholds
- 🌐 **Web UI** — interactive browser interface, no coding needed
- 📡 **REST API** — JSON responses with bounding box coordinates and confidence scores

---

## 🗂️ Project Structure

```
pigeon-yolov8-detection/
│
├── app.py                          # FastAPI backend & prediction endpoint
├── predict.py                      # Standalone inference script
├── data.yaml                       # Dataset configuration (YOLOv8 format)
├── requirements.txt                # Python dependencies
├── yolov8n.pt                      # Base YOLOv8 nano weights
│
├── runs/
│   └── detect/
│       └── train/
│           └── weights/
│               ├── best.pt         # ✅ Best trained model weights
│               └── last.pt         # Last epoch weights
│
├── static/
│   ├── index.html                  # Web frontend
│   ├── style.css                   # Styles
│   └── script.js                   # Frontend logic
│
├── train/
│   └── labels/                     # YOLO annotation label files
│
├── research_paper/                 # LaTeX research paper & figures
│   ├── paper.tex
│   └── README.md
│
└── Report/                         # Project report
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Prajapatidhruv1206/pigeon-yolov8-detection.git
cd pigeon-yolov8-detection
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

The server starts at **`http://localhost:8000`**

---

## 🌐 Usage

### Web Interface
Open your browser and go to:
```
http://localhost:8000
```
Upload any image and click **Detect** to see annotated results.

### REST API

**Endpoint:** `POST /predict`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file` | image file | required | Image to run detection on |
| `conf` | float | `0.5` | Confidence threshold (0.0 – 1.0) |
| `iou` | float | `0.5` | IoU threshold for NMS (0.0 – 1.0) |

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@your_image.jpg" \
  -F "conf=0.5" \
  -F "iou=0.45"
```

**Example response:**
```json
{
  "success": true,
  "num_pigeons": 7,
  "image_url": "/predictions/uuid-filename.jpg",
  "predictions_data": [
    {
      "class": "pigeon",
      "confidence": 0.9123,
      "box": { "x1": 120, "y1": 85, "x2": 210, "y2": 175 }
    }
  ]
}
```

---

## 🧠 Model Details

| Property | Value |
|----------|-------|
| Base Model | YOLOv8 nano (`yolov8n`) |
| Parameters | ~3.2 million |
| Training Images | 490 |
| Classes | 1 (Pigeon) |
| Input Resolution | 640 × 640 px |
| Annotation Format | YOLOv8 PyTorch |
| Dataset Source | Roboflow |
| Loss Function | Distribution Focal Loss (DFL) |

---

## 📊 Training Results

Training metrics and validation plots are available in `runs/detect/train/`, including:
- Precision / Recall curves
- mAP@0.5 and mAP@0.5:0.95
- Confusion matrix
- Validation batch predictions

---

## 📄 Research Paper

A formal research paper documenting the methodology, experiments, and findings is available in the [`research_paper/`](./research_paper/) directory (LaTeX source: `paper.tex`).

---

## 🛠️ Tech Stack

- **[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)** — Object detection model
- **[FastAPI](https://fastapi.tiangolo.com/)** — Backend REST API framework
- **[OpenCV](https://opencv.org/)** — Image annotation and processing
- **[Roboflow](https://roboflow.com/)** — Dataset annotation and export
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server

---

## 👤 Author

**Dhruv Prajapati**
- GitHub: [@Prajapatidhruv1206](https://github.com/Prajapatidhruv1206)

---

## 📜 License

This project is licensed under the MIT License.
