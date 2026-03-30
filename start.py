import subprocess
import sys
import os
import asyncio

# --- SETTINGS ---
OCR_SCRIPT = "ocr_processor.py"
TTS_SCRIPT = "main.py"
# -----------------

def get_script_dir():
    """Get the directory where this script is located"""
    return os.path.dirname(os.path.abspath(__file__))

def run_ocr():
    """Run the OCR script"""
    print("\n" + "="*60)
    print("STEP 1: OCR - Converting images to text")
    print("="*60 + "\n")
    
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, OCR_SCRIPT)
    
    if not os.path.exists(script_path):
        print(f"ERROR: {OCR_SCRIPT} not found in {script_dir}!")
        print("Make sure all scripts are in the same directory.")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: OCR script failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\nERROR: Failed to run OCR script: {e}")
        return False

def run_tts():
    """Run the TTS script"""
    print("\n" + "="*60)
    print("STEP 2: TTS - Converting text to audio")
    print("="*60 + "\n")
    
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, TTS_SCRIPT)
    
    if not os.path.exists(script_path):
        print(f"ERROR: {TTS_SCRIPT} not found in {script_dir}!")
        print("Make sure all scripts are in the same directory.")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: TTS script failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\nERROR: Failed to run TTS script: {e}")
        return False

def main():
    """Main orchestration - runs OCR then TTS"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "AUDIOBOOK GENERATOR - COMPLETE PIPELINE" + " "*9 + "║")
    print("║" + " "*16 + "(OCR + TTS)" + " "*33 + "║")
    print("╚" + "="*58 + "╝")
    print(f"\nWorking directory: {get_script_dir()}\n")
    
    # Step 1: Run OCR
    print(f"Running {OCR_SCRIPT}...")
    ocr_success = run_ocr()
    if not ocr_success:
        print("\n" + "="*60)
        print("❌ OCR FAILED. Exiting pipeline.")
        print("="*60 + "\n")
        return False
    
    # Step 2: Run TTS
    print(f"Running {TTS_SCRIPT}...")
    tts_success = run_tts()
    if not tts_success:
        print("\n" + "="*60)
        print("❌ TTS FAILED. Exiting pipeline.")
        print("="*60 + "\n")
        return False
    
    # Success!
    print("\n" + "="*60)
    print("✅ SUCCESS! Audiobook generated successfully!")
    print("="*60)
    print("\nYour files:")
    print(f"  📄 Text: vstup.txt")
    print(f"  🔊 Audio: fffff.mp3\n")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)