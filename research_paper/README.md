# YOLOv8 Pigeon Detection and Counting: Project Overview

This document serves as a foundational understanding of the Pigeon Detection project to aid in the drafting of a formal research paper. The project leverages a custom-trained YOLOv8 (You Only Look Once version 8) object detection model to accurately detect, localize, and count pigeons in various images. 

## 1. Project Objectives
- **Detection & Localization:** Identify the presence and exact location of pigeons within an image using bounding boxes.
- **Automated Counting:** Automatically quantify the number of pigeons detected in the frame.
- **Accessible Interface:** Provide a user-friendly API and Web interface to interact with the model seamlessly.

## 2. Dataset Details
- **Source:** Custom annotated dataset hosted and exported via Roboflow.
- **Size:** 490 images.
- **Format:** YOLOv8 PyTorch format.
- **Preprocessing & Augmentations:** No automated pre-processing or augmentations were applied prior to export, indicating the model learns directly from the raw image variations provided.

## 3. Methodology & Architecture
The core architecture is based on Ultralytics YOLOv8 (`yolov8n.pt` base model). The pipeline consists of three main stages:

### A. Training Phase
- The model is fine-tuned on the custom pigeon dataset.
- Training weights are saved iteratively, and the optimal weights are stored at `runs/detect/train/weights/best.pt`.

### B. Inference Pipeline (`predict.py`)
- Loads the fine-tuned `best.pt` weights.
- Processes single or batch images for inference.
- Outputs annotated images (with drawn bounding boxes) and logs the total count of pigeons detected to the console.

### C. Web Application & API (`app.py`)
- **Backend:** Built using **FastAPI**, creating a robust, asynchronous RESTful API.
- **Endpoint (`/predict`):** Accepts image file uploads along with configurable parameters for `conf` (Confidence Threshold) and `iou` (Intersection over Union).
- **Post-processing:** Uses OpenCV (`cv2`) to dynamically annotate the uploaded images. It draws custom pink bounding boxes `(246, 92, 139)` and applies sequential labels (e.g., `#1`, `#2`) to uniquely identify each detected pigeon.
- **Response:** Returns JSON containing the `num_pigeons`, URLs to the annotated images, and precise bounding box coordinates with confidence scores.
- **Frontend:** Serves a static HTML interface (`static/index.html`) for easy web-based testing.

## 4. Potential Research Paper Angles
When drafting the research paper, we can focus on several novel or technical aspects of this implementation:
1. **Real-world Application:** Evaluating YOLOv8's performance in urban wildlife monitoring (specifically pigeons), dealing with challenges like occlusion and varying scales.
2. **End-to-End System Design:** Detailing the integration of state-of-the-art deep learning (YOLOv8) with a high-performance web framework (FastAPI) for real-time inference.
3. **Thresholding Impact:** Analyzing how different Confidence and IoU thresholds affect counting accuracy in dense pigeon flocks.

---

*Note: This README is intended to summarize the technical architecture for the purpose of structuring the subsequent academic paper and documenting the project repository.*
