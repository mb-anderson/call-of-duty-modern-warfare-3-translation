import os
import re
import json

TRANSLATION_PATH = "translation"
EXPORTED_JSON_PATH = f"{TRANSLATION_PATH}/exported/json"
EXPORTED_STR_PATH = f"{TRANSLATION_PATH}/exported/str"
EXPORTED_JSON = f"{EXPORTED_JSON_PATH}/all_strings.json"

result = {}

for filename in os.listdir(EXPORTED_STR_PATH):
    if filename.endswith(".str"):
        filepath = os.path.join(EXPORTED_STR_PATH, filename)
        with open(filepath) as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                print(f"File read error (UnicodeDecodeError): {filename}")
                continue
            
        entries = {}
        # Find REFERENCE and LANG_ENGLISH blocks
        pattern = re.compile(r'REFERENCE\s+([^\n]+)\nLANG_ENGLISH\s+"((?:[^"\\]|\\.)*)"')
        for ref, text in pattern.findall(content):
            entries[ref.strip()] = text.replace('\n', '\\n')
        result[filename] = entries

with open(EXPORTED_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("Total STR files:", len(result))
print("Total strings:", sum(len(strings) for strings in result.values()))

print(f"JSON file created: {EXPORTED_JSON}")