import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from ultralytics import YOLO
import uuid

app = FastAPI(title="Pigeon Detector API")

# Initialize model
MODEL_PATH = os.path.join("runs", "detect", "train", "weights", "best.pt")
model = YOLO(MODEL_PATH)

# Setup directories
UPLOAD_DIR = "uploads"
PREDICT_DIR = "runs/detect/predict_web"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PREDICT_DIR, exist_ok=True)
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/predictions", StaticFiles(directory=PREDICT_DIR), name="predictions")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/predict")
async def predict(file: UploadFile = File(...), conf: float = Form(0.5), iou: float = Form(0.5)):
    # Create a unique filename to prevent overwriting
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save uploaded file (User requested to keep them)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Run YOLO prediction without saving automatically
    results = model.predict(source=file_path, save=False, conf=conf, iou=iou)
    
    if len(results) > 0:
        result = results[0]
        num_pigeons = len(result.boxes)
        
        # We'll use OpenCV to manually draw the boxes and numbers
        import cv2
        img = cv2.imread(file_path)
        
        predictions_data = []
        
        for i, box in enumerate(result.boxes):
            # Get coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            
            predictions_data.append({
                "class": "pigeon",
                "confidence": round(confidence, 4),
                "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            })
            
            # Draw the bounding box (Pink color)
            cv2.rectangle(img, (x1, y1), (x2, y2), (246, 92, 139), 2)
            
            # Create the numbering label (e.g., "#1", "#2")
            label = f"#{i+1}"
            
            # Smaller text scale and thickness
            font_scale = 0.5
            thickness = 1
            
            # Draw a filled rectangle behind the text for readability (with less padding)
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            
            # Ensure we don't draw outside the image top boundary
            y_bg_top = max(0, y1 - h - 4)
            cv2.rectangle(img, (x1, y_bg_top), (x1 + w + 4, y1), (246, 92, 139), -1)
            
            # Draw the text
            cv2.putText(img, label, (x1 + 2, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
            
        # Save the custom annotated image
        output_path = os.path.join(PREDICT_DIR, unique_filename)
        cv2.imwrite(output_path, img)
        
        # Return the URL to access it
        predicted_image_url = f"/predictions/{unique_filename}"
        
        return {
            "success": True,
            "num_pigeons": num_pigeons,
            "image_url": predicted_image_url,
            "predictions_data": predictions_data
        }
    
    return {"success": False, "message": "Failed to process image"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
