import json
import deepl
import os
from pathlib import Path

# Enter Deepl API Key or set DEEPL_AUTH_KEY environment variable
AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not AUTH_KEY:
    raise ValueError("DEEPL_AUTH_KEY environment variable is not set")

TRANSLATION_PATH = "translation"
EXPORTED_JSON_PATH = f"{TRANSLATION_PATH}/exported/json"
TRANSLATED_PATH = f"{TRANSLATION_PATH}/translated/json"

# Create DeepL client
translator = deepl.Translator(AUTH_KEY)

def translate_json_file(input_file, output_file, source_lang="EN", target_lang="TR"):
    """
    Translate JSON file using DeepL and save to a new file.
    
    Args:
        input_file: Input JSON file path
        output_file: Output JSON file path
        source_lang: Source language code (default: EN)
        target_lang: Target language code (default: TR)
    """
    print(f"📖 Reading {input_file}...")
    
    # Read JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    translated_data = {}
    total_files = len(data)
    current_file = 0
    
    # For each file in the JSON
    for filename, entries in data.items():
        current_file += 1
        print(f"\n[{current_file}/{total_files}] 📝 Translating {filename}...")
        
        translated_entries = {}
        
        # Collect all texts
        refs = list(entries.keys())
        texts = list(entries.values())
        
        if not texts:
            translated_data[filename] = {}
            continue
        
        # Filter out empty texts
        non_empty_indices = [i for i, text in enumerate(texts) if text.strip()]
        non_empty_texts = [texts[i] for i in non_empty_indices]
        
        if not non_empty_texts:
            # All texts are empty
            for ref, text in entries.items():
                translated_entries[ref] = text
        else:
            try:
                # Batch translation with DeepL
                print(f"   ⏳ Translating {len(non_empty_texts)} texts...")
                results = translator.translate_text(
                    non_empty_texts,
                    source_lang=source_lang,
                    target_lang=target_lang
                )
                
                # Process results
                result_iter = iter(results if isinstance(results, list) else [results])
                for i, (ref, text) in enumerate(zip(refs, texts)):
                    if i in non_empty_indices:
                        translated_text = next(result_iter).text
                        translated_entries[ref] = translated_text
                    else:
                        # Leave empty texts as is
                        translated_entries[ref] = text
                
                print(f"   ✅ Completed!")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                print(f"   ⚠️  Using original texts...")
                translated_entries = entries.copy()
        
        translated_data[filename] = translated_entries
    
    # Save translated data
    print(f"\n💾 {output_file} saving...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)
    
    print(f"✨ Translation complete! Saved: {output_file}")

def main():
    # Translate Part 1
    print("=" * 60)
    print("🌍 Starting translation of Part 1...")
    print("=" * 60)
    translate_json_file(
        f"{EXPORTED_JSON_PATH}/all_strings_part1.json",
        f"{TRANSLATED_PATH}/translated_part1.tr.json",
        source_lang="EN",
        target_lang="TR"
    )
    
    print("\n" + "=" * 60)
    print("🌍 Starting translation of Part 2...")
    print("=" * 60)
    # Translate Part 2
    translate_json_file(
        f"{EXPORTED_JSON_PATH}/all_strings_part2.json",
        f"{TRANSLATED_PATH}/translated_part2.tr.json",
        source_lang="EN",
        target_lang="TR"
    )
    
    print("\n" + "=" * 60)
    print("🎉 All translations completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
