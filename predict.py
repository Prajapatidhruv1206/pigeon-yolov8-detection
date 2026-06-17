import os
import sys
from ultralytics import YOLO

def main(image_path):
    # The default path where YOLO saves the best model weights after training
    model_path = os.path.join("runs", "detect", "train", "weights", "best.pt")
    
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        print("Please wait for the training process to finish.")
        return

    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)

    print(f"Running prediction on {image_path}...")
    # Run prediction:
    # save=True will save the annotated image to runs/detect/predict
    # show=True will display the image in a window (if your environment supports it)
    results = model.predict(source=image_path, save=True, show=True)
    
    print("\n" + "="*40)
    print("🎯 PREDICTION RESULTS")
    print("="*40)
    
    if len(results) > 0:
        # Each result corresponds to one image (we only passed one)
        result = results[0]
        
        # Get the number of detected boxes (pigeons)
        num_pigeons = len(result.boxes)
        print(f"I found {num_pigeons} pigeon(s) in this image!")
        
        print(f"Saved the annotated image to: {result.save_dir}")
    print("="*40 + "\n")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <path_to_image>")
        print("No image provided. Attempting to use a random training image as a test...\n")
        
        # Try to find a training image to test on if no argument is provided
        train_img_dir = os.path.join("train", "images")
        if os.path.exists(train_img_dir):
            images = [f for f in os.listdir(train_img_dir) if f.endswith((".jpg", ".png", ".jpeg"))]
            if images:
                # Pick the first image as a sample
                test_image = os.path.join(train_img_dir, images[0])
                main(test_image)
            else:
                print("No images found in train/images.")
        else:
            print("Please provide an image path.")
    else:
        # Run prediction on the user-provided image path
        main(sys.argv[1])
