import pytesseract
from PIL import Image
import os
from pathlib import Path
import cv2
import numpy as np
import sys

# --- SETTINGS ---
INPUT_FOLDER = "input_image"       # Folder containing images
OUTPUT_FILE = "vstup.txt"          # Output text file
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
LANGUAGE = "ces"                   # Czech language code for Tesseract
# -----------------

def get_script_dir():
    """Get the directory where this script is located"""
    return os.path.dirname(os.path.abspath(__file__))

def check_dependencies():
    """Verify all required packages are installed"""
    print("--- Checking dependencies ---")
    required = {
        'cv2': 'opencv-python',
        'PIL': 'pillow',
        'pytesseract': 'pytesseract'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"ERROR: Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    # Check Tesseract installation
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        print("ERROR: Tesseract OCR not installed!")
        print("Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    
    print("✓ All dependencies OK\n")
    return True

def ensure_input_folder():
    """Create input folder if it doesn't exist"""
    script_dir = get_script_dir()
    input_path = os.path.join(script_dir, INPUT_FOLDER)
    
    if not os.path.exists(input_path):
        os.makedirs(input_path)
        print(f"--- Created folder: {input_path} ---")
    else:
        print(f"--- Using existing folder: {input_path} ---")
    
    return input_path

def get_image_files(input_path):
    """Get all supported image files from input folder"""
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(Path(input_path).glob(f"*{ext}"))
        image_files.extend(Path(input_path).glob(f"*{ext.upper()}"))
    
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
        print(f"      Warning: Preprocessing failed, using original image: {e}")
        return Image.open(image_path)

def extract_text_from_image(image_path):
    """Extract text from a single image using OCR with Czech optimization"""
    try:
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
        print(f"      ERROR processing {image_path.name}: {e}")
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
    # Check dependencies first
    if not check_dependencies():
        return False
    
    # Ensure input folder exists
    input_path = ensure_input_folder()
    
    # Get all images
    image_files = get_image_files(input_path)
    
    if not image_files:
        print(f"ERROR: No images found in '{input_path}' folder!")
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        return False
    
    print(f"--- Found {len(image_files)} image(s) to process ---")
    print(f"--- Using language: Czech ({LANGUAGE}) ---\n")
    
    # Extract text from all images
    all_text = []
    successful_count = 0
    
    for idx, image_path in enumerate(image_files, 1):
        print(f"   [{idx}/{len(image_files)}] Processing: {image_path.name}")
        text = extract_text_from_image(image_path)
        text = clean_text(text)
        if text.strip():
            all_text.append(text)
            all_text.append("\n\n")  # Add spacing between images
            successful_count += 1
        else:
            print(f"           ⚠ No text extracted from this image")
    
    if not all_text:
        print("\nERROR: No text could be extracted from images!")
        return False
    
    # Write to output file
    script_dir = get_script_dir()
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    print(f"\n--- Writing text to file: {output_path} ---")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(all_text)
        print(f"✓ DONE! Text saved as '{OUTPUT_FILE}'")
        print(f"✓ Successfully processed: {successful_count}/{len(image_files)} images\n")
        return True
    except Exception as e:
        print(f"ERROR: Could not write to file: {e}")
        return False

if __name__ == "__main__":
    success = process_images()
    sys.exit(0 if success else 1)