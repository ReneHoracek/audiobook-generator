import subprocess
import sys
import os

# --- SETTINGS ---
OCR_SCRIPT = "src/ocr_processor.py"
TTS_SCRIPT = "src/main.py"
# -----------------

def run_ocr():
    """Run the OCR script"""
    print("\n" + "="*60)
    print("STEP 1: OCR - Converting images to text")
    print("="*60 + "\n")
    
    if not os.path.exists(OCR_SCRIPT):
        print(f"ERROR: {OCR_SCRIPT} not found!")
        return False
    
    try:
        result = subprocess.run([sys.executable, OCR_SCRIPT], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"ERROR: OCR script failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to run OCR script: {e}")
        return False

def run_tts():
    """Run the TTS script"""
    print("\n" + "="*60)
    print("STEP 2: TTS - Converting text to audio")
    print("="*60 + "\n")
    
    if not os.path.exists(TTS_SCRIPT):
        print(f"ERROR: {TTS_SCRIPT} not found!")
        return False
    
    try:
        result = subprocess.run([sys.executable, TTS_SCRIPT], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"ERROR: TTS script failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to run TTS script: {e}")
        return False

def main():
    """Main orchestration - runs OCR then TTS"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "AUDIOBOOK GENERATOR - COMPLETE PIPELINE" + " "*9 + "║")
    print("║" + " "*16 + "(OCR + TTS)" + " "*33 + "║")
    print("╚" + "="*58 + "╝")
    
    # Step 1: Run OCR
    print(f"\nRunning {OCR_SCRIPT}...")
    ocr_success = run_ocr()
    if not ocr_success:
        print("\n❌ OCR failed. Exiting.")
        return False
    
    # Step 2: Run TTS
    print(f"\nRunning {TTS_SCRIPT}...")
    tts_success = run_tts()
    if not tts_success:
        print("\n❌ TTS failed. Exiting.")
        return False
    
    # Success!
    print("\n" + "="*60)
    print("✅ COMPLETE! Audiobook generated successfully!")
    print("="*60 + "\n")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)