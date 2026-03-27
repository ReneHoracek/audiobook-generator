# Audiobook Generator

Automaticky konvertuj fotky knihy do audiobooku!

## Funkce

- 📸 **OCR** - Konvertuj fotky textu na text (česky)
- 🎵 **TTS** - Převeď text na mluvené slovo (Edge TTS)
- 🔄 **Pipeline** - Vše spustíš jedním příkazem

## Instalace

1. **Klonuj repo:**
```bash
git clone https://github.com/YOUR_USERNAME/audiobook-genreator.git
cd audiobook-genreator
```

2. **Vytvoř virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# nebo na Windows:
venv\Scripts\activate
```

3. **Nainstaluj závislosti:**
```bash
pip install -r requirements.txt
```

4. **Nainstaluj Tesseract OCR:**
- **Fedora:** `sudo dnf install tesseract tesseract-langpack-ces`
- **Ubuntu:** `sudo apt install tesseract-ocr tesseract-langpack-ces`
- **Mac:** `brew install tesseract`
- **Windows:** Stáhni z https://github.com/UB-Mannheim/tesseract/wiki

## Použití

1. **Umísti fotky do `input_image/` složky**

2. **Spusť pipeline:**
```bash
python start.py
```

3. **Tvůj audiobook je v `audiobook.mp3`** 🎧

## Struktura projektu
```
audiobook-genreator/
├── start.py              # Spusti vše
├── src/
│   ├── ocr_processor.py  # Fotka → Text
│   └── main.py           # Text → Audio
├── input_image/          # Umísti sem fotky
├── requirements.txt
└── README.md
```

## Známé problémy

- OCR na fotkách knihy není ideální (chystaná vylepšení)
- Nejlepší výsledky s čistými, rovnými fotkami

## Plánované features

- [ ] Vylepšit OCR (PaddleOCR)
- [ ] Webové rozhraní
- [ ] Batch processing

## Licence

MIT License