# this script converts a JSON file containing string entries back into multiple STR files.
# it is the reverse of str_to_json.py
# because of the controlled format of STR files so we can see what files they came from, we add a header comment in each STR file.
# this is useful for checking file structure, escape characters' usage, strings and debugging.

import json
import os

TRANSLATION_PATH = "translation"
EXPORTED_JSON_PATH = f"{TRANSLATION_PATH}/exported/json"
EXPORTED_JSON = f"{EXPORTED_JSON_PATH}/all_strings.json"
EXPORTED_STR_PATH = f"{TRANSLATION_PATH}/exported/str"

os.makedirs(EXPORTED_STR_PATH, exist_ok=True)

with open(EXPORTED_JSON, encoding="utf-8") as f:
    data = json.load(f)

for filename, entries in data.items():
    out_path = os.path.join(EXPORTED_STR_PATH, filename)
    with open(out_path, "w", encoding="utf-8") as out:
        # Başlık kısmı (örnek, Berlin için)
        out.write(f'// Dumped from fastfile "{filename.replace(".str", "")}".\n')
        out.write('// In their original format the strings might have been separated in multiple files.\n')
        out.write('VERSION             "1"\n')
        out.write('CONFIG              "C:/trees/cod3/cod3/bin/StringEd.cfg"\n')
        out.write('FILENOTES           ""\n\n')
        for ref, text in entries.items():
            out.write(f'REFERENCE           {ref}\n')
            out.write(f'LANG_ENGLISH        "{text.replace("\\n", "\\n")}"\n\n')
        out.write("ENDMARKER")

print(f"STR files have been written to the '{EXPORTED_STR_PATH}' directory.")