import asyncio
import edge_tts
import os
import sys

# --- SETTINGS ---
INPUT_FILE = "vstup.txt"        # Input text file
OUTPUT_FILE = "fffff.mp3"       # Output audio file
VOICE = "cs-CZ-AntoninNeural"   # Czech voice for natural pronunciation

# Audio settings
RATE = "-15%"      # Speech rate: -50% to +100% (default +0%)
PITCH = "-2Hz"    # Voice pitch: -100Hz to +100Hz (default +0Hz)
VOLUME = "+0%"    # Volume level: -100% to +100% (default +0%)
# -----------------

def get_script_dir():
    """Get the directory where this script is located"""
    return os.path.dirname(os.path.abspath(__file__))

def check_dependencies():
    """Verify required packages are installed"""
    print("--- Checking dependencies ---")
    try:
        import edge_tts
        print("✓ edge-tts installed")
    except ImportError:
        print("ERROR: edge-tts not installed!")
        print("Install with: pip install edge-tts")
        return False
    
    print("✓ All dependencies OK\n")
    return True

async def generate_audio():
    """Generate audio from text file using TTS"""
    # Check dependencies first
    if not check_dependencies():
        return False
    
    script_dir = get_script_dir()
    input_path = os.path.join(script_dir, INPUT_FILE)
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"ERROR: File '{INPUT_FILE}' not found!")
        print(f"Expected location: {input_path}")
        print("Make sure to run ocr_processor.py first to generate the text file.")
        return False

    # Load text from file
    print(f"--- Reading text from file: {INPUT_FILE} ---")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text_content = f.read()
    except Exception as e:
        print(f"ERROR: Could not read file: {e}")
        return False

    if not text_content.strip():
        print("ERROR: Text file is empty!")
        return False

    # Validate text length (edge-tts has limits)
    text_length = len(text_content)
    print(f"--- Text length: {text_length:,} characters ---")
    if text_length > 100000:
        print("WARNING: Text is very long. This may take a while...")

    # Generate audio with settings
    print(f"--- Generating audio with voice: {VOICE} ---")
    print(f"--- Settings: Rate={RATE}, Pitch={PITCH}, Volume={VOLUME} ---")
    print("--- This may take a while depending on text length... ---\n")
    
    try:
        communicate = edge_tts.Communicate(
            text_content, 
            VOICE,
            rate=RATE,
            pitch=PITCH,
            volume=VOLUME
        )

        await communicate.save(output_path)
        print(f"\n✓ DONE! Audio saved as '{OUTPUT_FILE}'")
        print(f"✓ Output file: {output_path}\n")
        return True
    except Exception as e:
        print(f"\nERROR: Failed to generate audio: {e}")
        print("Make sure you have a stable internet connection.")
        return False

def main():
    """Main entry point"""
    success = asyncio.run(generate_audio())
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)