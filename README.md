# Call of Duty: Modern Warfare 3 Translation Project

A comprehensive translation toolkit for Call of Duty: Modern Warfare 3 (MW3) that enables localization of in-game strings from English to any target language. This project uses the OAT (OpenAssetTools) Linker/Unlinker to modify game fastfiles.

## If You Like It

### Sponsor this project

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/mburakyucel)

## 🎯 Overview

This project provides a complete workflow for translating MW3 game strings:

1. Extract localized strings from game fastfiles (`.ff`) with Unlinker
2. Convert strings to JSON format for easy editing
3. Translate strings using DeepL API or Json Translation
4. Convert translated JSON back to STR format (`.str`)
5. Rebuild fastfiles with translated content (`.ff`) with Linker
6. Deploy to game directory

## 📋 Prerequisites

- **Linux** operating system (bash shell required)
- **Python 3.x** with the following packages:
  - `deepl` - For automated translation (optional)
  - `json` (built-in)
  - `os`, `re`, `subprocess` (built-in)
- **Node.js** and npm - For JSON translation tools (optional) (<https://github.com/mololab/json-translator>) 
- **OAT (OpenAssetTools)** - Linker and Unlinker executables (<https://github.com/Laupetin/OpenAssetTools>)
- **DeepL API Key** - For automated translation (optional) (<https://developers.deepl.com>)
- **MW3 Game Files** - Original game installation (do not remember prepare backup)

## 📁 Project Structure

```
oat-linux/
├── translation/              # Translated and Exported JSON and STR files
│  └── exported/              # Exported files
│  │  └── json/               # Exported JSON files from the exported STR files
│  │  └── str/                # Exported STR files using Unlinker from original game
│  └── translated/            # Original game fastfiles
│  │  └── json/               # Translated json files using translate.py or JSON Translator
│  │  └── str/                # Translated STR files from JSON
├── zone_raw/                 # Zone source files for linking
├── zone_out/                 # Generated fastfiles output
├── zone_dump/                # Unlinked game assets
├── mw3/                      # MW3 game directory
│   └── zone/english/         # Original game fastfiles
├── str_to_json.py            # Convert STR files to JSON
├── json_to_str.py            # Convert JSON to STR files
├── json_to_patch_str.py      # Convert JSON to chunked patch STR files
├── translate.py              # Automated translation using DeepL
├── linker.sh                 # Build fastfiles from zone sources
├── unlinker.sh               # Extract assets from fastfiles
└── package.json              # Node.js dependencies
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone this project
git clone git@github.com:mb-anderson/call-of-duty-modern-warfare-3-translation.git

# Install Python dependencies (optional: A)
pip install deepl

# Install Node.js dependencies (optional: B)
npm install

# Clone OpenAssetTools project
git clone git@github.com:Laupetin/OpenAssetTools.git
```

### 2. Extract Game Strings

First, extract strings from the original game files:

```bash
# Extract all fastfiles to zone_dump/
bash unlinker.sh

# Copy extracted zone_raw content to project root
cp -r zone_dump/zone_raw/* zone_raw/
```

### 3. Convert to JSON

Convert extracted STR files to JSON for easier translation:

```bash
python str_to_json.py
```

This creates `all_strings.json` containing all extractable strings from the game.

### 4. Translate Strings

#### Option A: Automated Translation with DeepL

Edit `translate.py` and add your DeepL API key:

```python
auth_key = "your-deepl-api-key-here"
```

Run translation:

```bash
python translate.py
```

#### Option B: JSON Translator

Read the docs: <https://github.com/mololab/json-translator>

#### Option C: Manual Translation

Edit the JSON files manually or use any translation tool of your choice.

### 5. Generate Patch Files

Convert translated JSON back to STR format with chunking (to avoid the 10,000 localized asset limit):

```bash
python json_to_patch_str.py
```

This script will:

- Generate chunked `patch.str`, `patch1.str`, `patch2.str`, etc.
- Copy STR files to appropriate `zone_raw/patch[index]` directories
- Automatically run `linker.sh` to build fastfiles
- Copy generated `.ff` files to game directory

### 6. Manual Linking (Alternative)

If you want to manually control the linking process:

```bash
bash linker.sh
```

Then copy the generated `.ff` files from `zone_out/` to your game's `zone/english/` directory.

## 🔧 Detailed Workflow

### Understanding the Translation Pipeline

1. **Unlinker Phase**
   - Extracts assets from game's `.ff` (fastfile) format
   - Produces `.str` files containing localized strings
   - Creates zone definition files

2. **Conversion Phase**
   - `str_to_json.py`: Parses STR files into structured JSON
   - Makes editing and translation easier
   - Preserves references and formatting

3. **Translation Phase**
   - Manual or automated translation of JSON content
   - DeepL integration for high-quality machine translation
   - Supports batch processing to reduce API calls

4. **Reconstruction Phase**
   - `json_to_patch_str.py`: Converts JSON back to STR format
   - Splits into chunks to avoid engine limitations (10,000 asset limit)
   - Applies character mapping for compatibility

5. **Linking Phase**
   - `linker.sh`: Rebuilds fastfiles from modified sources
   - Creates patch chain: patch → patch1 → patch2 → patch3 → patch4
   - Each patch includes the next in the chain

### Important Notes

#### Asset Limit Handling

MW3 has a hardcoded limit of 10,000 localized assets per fastfile. This project uses a chaining strategy:

- Strings are split into chunks of 5,000 entries each
- Multiple patch files are created (`patch.str`, `patch1.str`, etc.)
- Patches form an include chain in `zone_raw/` definitions
- This allows unlimited translations while respecting engine limits

#### Character Mapping

Turkish and other special characters are mapped to Latin equivalents to prevent rendering issues:

```python
LANGUAGE_MAP_TO_LATIN = {
    "İ": "I", "ı": "i",
    "Ş": "S", "ş": "s",
    "Ğ": "G", "ğ": "g",
    "Ü": "U", "ü": "u",
    "Ö": "O", "ö": "o",
    "Ç": "C", "ç": "c",
}
```

Modify this mapping in `json_to_patch_str.py` for other languages.

## 📝 Configuration

### Setting Game Directory

Edit `json_to_patch_str.py` to set your MW3 installation path:

```python
GAME_DIRECTORY = "/path/to/your/Call of Duty - Modern Warfare 3"
```

### Adjusting Chunk Size

To change how strings are split across patch files, edit `json_to_patch_str.py`:

```python
CHUNK_SIZE = 5000  # Adjust based on your needs
```

### Linker Configuration

The `linker.sh` script uses environment variables. Modify as needed:

```bash
export MODERNWARFAREREPO=$BASEPATH/mw3
export SEARCHPATH=$MODERNWARFAREREPO/main
export ZONEPATH=$MODERNWARFAREREPO/zone/english
```

## 🔍 Troubleshooting

### "Exceeded limit of 10000 'localized' assets" Error

This means too many strings are in a single patch file. Reduce `CHUNK_SIZE` in `json_to_patch_str.py`.

### Missing Translations in Game

Ensure patch files are properly chained in `zone_raw/` definitions:

- `patch.zone` should include `patch1`
- `patch1.zone` should include `patch2`
- And so on...

Your patch[*].zone files should look like:
/patch/english/localizedstrings/patch.str:
```
>game,IW5

localize,patch
localize,patch1
...other...
[DO NOT DELETE OTHER TEXTS]
EOF
```
zone_raw/patch/english/localizedstrings/patch[1-4].str:
```
>game,IW5

localize,patch1
localize,patch2
[DELETE OTHER TEXTS]
EOF
```

```
oat-linux/
    └──zone_raw/
        │    └──patch
        │           └──english/localizedstrings/patch.str
        │    └──patch1
        │           └──english/localizedstrings/patch1.str
        │    └──patch2
        │           └──english/localizedstrings/patch2.str
        │    └──patch3
        │           └──english/localizedstrings/patch3.str
        │    └──patch4
        │           └──english/localizedstrings/patch4.str
```

### Linker Errors

Make sure:

- All paths in `linker.sh` are correct
- Zone definitions in `zone_raw/` are properly formatted
- Original game fastfiles are intact in `mw3/zone/english/`

### Unicode/Character Encoding Issues

If you see garbled text:

- Check that all Python scripts use `utf-8` encoding
- Verify character mapping in `json_to_patch_str.py`
- Some special characters may need to be mapped to ASCII equivalents

## 📦 Output Files

After running the complete pipeline, you'll have:

- `str/*.str` - Extracted original strings
- `all_strings.json` - All strings in JSON format
- `translation/patch*.str` - Translated strings in STR format
- `zone_out/patch*.ff` - Compiled fastfiles ready for game to copy and paste MW3/zone/english

## 🤝 Contributing

Feel free to contribute improvements:

- MW3 Font support
- Support for additional languages
- Better character mapping strategies
- GUI tools for easier translation
- Optimization of translation workflow

## 📄 License

This is a community translation project. Respect Call of Duty: Modern Warfare 3 licensing and only use for personal, non-commercial purposes.

## ⚠️ Disclaimer

This tool modifies game files. Always keep backups of your original game installation. The authors are not responsible for any damage to game files or issues arising from the use of these tools.

## 🙏 Acknowledgments

- **OpenAssetTools (OAT)** - For the Linker/Unlinker tools
- **DeepL** - For translation API
- **Json Translator** - For translation JSON
- **MW3 Community** - For reverse engineering efforts

---

**Note**: Make sure to run `unlinker.sh` first to create the initial `zone_dump/` directory structure before starting the translation process.
