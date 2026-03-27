import asyncio
import edge_tts
import os

# --- SETTINGS ---
INPUT_FILE = "vstup.txt"        # Input text file
OUTPUT_FILE = "fffff.mp3"       # Output audio file (will be in same folder as script)
VOICE = "cs-CZ-AntoninNeural"   # Czech voice for natural pronunciation

# Audio settings
RATE = "+0%"      # Speech rate: -50% to +100% (default +0%)
PITCH = "+0Hz"    # Voice pitch: -100Hz to +100Hz (default +0Hz)
VOLUME = "+0%"    # Volume level: -100% to +100% (default +0%)
# -----------------

async def generate_audio():
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: File {INPUT_FILE} not found! Create it in the project folder.")
        return

    # Load text from file
    print(f"--- Reading text from file: {INPUT_FILE} ---")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text_content = f.read()

    if not text_content.strip():
        print("ERROR: Text file is empty!")
        return

    # Generate audio with settings
    print("--- Generating audio from text... ---")
    communicate = edge_tts.Communicate(
        text_content, 
        VOICE,
        rate=RATE,
        pitch=PITCH,
        volume=VOLUME
    )

    await communicate.save(OUTPUT_FILE)
    print(f"--- DONE! Audio saved as '{OUTPUT_FILE}' ---")

if __name__ == "__main__":
    asyncio.run(generate_audio())