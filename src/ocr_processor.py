import pytesseract
from PIL import Image
import os
from pathlib import Path
import cv2
import numpy as np

# --- SETTINGS ---
INPUT_FOLDER = "input_image"       # Folder containing images
OUTPUT_FILE = "vstup.txt"          # Output text file
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
LANGUAGE = "ces"                   # Czech language code for Tesseract
# -----------------

def ensure_input_folder():
    """Create input folder if it doesn't exist"""
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"--- Created folder: {INPUT_FOLDER} ---")
    else:
        print(f"--- Using existing folder: {INPUT_FOLDER} ---")

def get_image_files():
    """Get all supported image files from input folder"""
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(Path(INPUT_FOLDER).glob(f"*{ext}"))
        image_files.extend(Path(INPUT_FOLDER).glob(f"*{ext.upper()}"))
    
    return sorted(image_files)

def preprocess_image(image_path):
    """Preprocess image for better OCR results"""
    try:
        # Read image with OpenCV
        img = cv2.imread(str(image_path))
        if img is None:
            return Image.open(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding for better contrast
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, h=10)
        
        # Upscale image (improves OCR accuracy)
        scale = 2
        upscaled = cv2.resize(denoised, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        
        # Convert back to PIL Image
        return Image.fromarray(upscaled)
    except Exception as e:
        print(f"   Warning: Preprocessing failed, using original image: {e}")
        return Image.open(image_path)

def extract_text_from_image(image_path):
    """Extract text from a single image using OCR with Czech optimization"""
    try:
        print(f"   Processing: {image_path.name}")
        
        # Preprocess image for better results
        img = preprocess_image(image_path)
        
        # Use Tesseract with Czech language
        # Config options:
        # --psm 1: Automatic page segmentation with OSD (best for mixed text)
        # --psm 3: Fully automatic page segmentation (good default)
        # --psm 6: Assume a single uniform block of text (faster)
        config = f'--psm 3 -l {LANGUAGE}'
        
        text = pytesseract.image_to_string(img, config=config)
        return text
    except Exception as e:
        print(f"   ERROR processing {image_path.name}: {e}")
        return ""

def clean_text(text):
    """Clean and fix common OCR mistakes"""
    # Remove extra spaces
    text = ' '.join(text.split())
    
    # Common Czech OCR corrections
    corrections = {
        'l1': 'll',  # lowercase L confused with 1
        'rn': 'm',   # Common OCR mistake
        'CZ': 'Čž',  # Fix Czech characters if needed
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    return text

def process_images():
    """Main function to process all images and create text file"""
    ensure_input_folder()
    
    # Get all images
    image_files = get_image_files()
    
    if not image_files:
        print(f"ERROR: No images found in '{INPUT_FOLDER}' folder!")
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        return
    
    print(f"--- Found {len(image_files)} image(s) to process ---")
    print(f"--- Using language: Czech ({LANGUAGE}) ---")
    
    # Extract text from all images
    all_text = []
    for image_path in image_files:
        text = extract_text_from_image(image_path)
        text = clean_text(text)
        if text.strip():
            all_text.append(text)
            all_text.append("\n\n")  # Add spacing between images
    
    if not all_text:
        print("ERROR: No text could be extracted from images!")
        return
    
    # Write to output file
    print(f"--- Writing text to file: {OUTPUT_FILE} ---")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(all_text)
    
    print(f"--- DONE! Text saved as '{OUTPUT_FILE}' ---")
    print(f"--- Total images processed: {len(image_files)} ---")

if __name__ == "__main__":
    process_images()