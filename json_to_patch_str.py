# this script converts a JSON file containing string entries back into multiple STR files.
# it splits output every N entries to avoid the MW3 10000 localize asset limit.
# remember, edit patch, patch1, patch2... in the zone_raw/ to include all STR files.
# patch zone should include like queue: 
# patch includes patch1; patch1 includes patch2; patch2 includes patch3; patch3 includes patch4;
# otherwise only patch.str will be loaded. so i recommend making a chain of includes and i did 4 part.
# i prefer this way to avoid 'Exceeded limit of 10000 "localized" assets' error.

import json
import os
import subprocess

LANGUAGE_MAP_TO_LATIN = str.maketrans({
    "İ": "I", "I": "I",
    "ı": "i", "i": "i",
    "Ş": "S", "ş": "s",
    "Ğ": "G", "ğ": "g",
    "Ü": "U", "ü": "u",
    "Ö": "O", "ö": "o",
    "Ç": "C", "ç": "c",
})

GAME_DIRECTORY = "/media/anderson/VAIO/Call of Duty - Modern Warfare 3"
TRANSLATION_PATH = "translation"
EXPORTED_JSON_PATH = f"{TRANSLATION_PATH}/exported/json"
TRANSLATED_JSON = f"{EXPORTED_JSON_PATH}/translated.json.tr.json"
TRANSLATED_STR_PATH = f"{TRANSLATION_PATH}/translated/str"
CHUNK_SIZE = 5000   # Every N entries, create a new STR file

os.makedirs(TRANSLATED_STR_PATH, exist_ok=True)

with open(TRANSLATED_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

def write_header(f, name_without_ext):
    f.write(f'// Dumped from fastfile "{name_without_ext}".\n')
    f.write('// In their original format the strings might have been separated in multiple files.\n')
    f.write('VERSION             "1"\n')
    f.write('CONFIG              "C:/trees/cod3/cod3/bin/StringEd.cfg"\n')
    f.write('FILENOTES           ""\n\n')


file_index = 0
entry_count = 0
out_file = None

def open_new_file(idx):
    filename = f"patch{'' if idx == 0 else idx}.str"
    path = os.path.join(TRANSLATED_STR_PATH, filename)
    f = open(path, "w", encoding="utf-8")
    write_header(f, filename.replace(".str", ""))
    return f, filename

# Open the first output file
out_file, current_name = open_new_file(file_index)

for filename, entries in data.items():
    for ref, text in entries.items():

            # Eğer chunk dolduysa yeni dosya aç
        if entry_count > 0 and entry_count % CHUNK_SIZE == 0:
            out_file.write("ENDMARKER")
            out_file.close()

            file_index += 1
            out_file, current_name = open_new_file(file_index)

        safe_text = json.dumps(text, ensure_ascii=False)[1:-1]
        safe_text = safe_text.translate(LANGUAGE_MAP_TO_LATIN)

        out_file.write(f'REFERENCE           {ref}\n')
        out_file.write(f'LANG_ENGLISH        "{safe_text}"\n\n')

        entry_count += 1

# Son dosyayı kapat
out_file.write("ENDMARKER")
out_file.close()

print(f"{entry_count} REFERENCE entries successfully split into {file_index + 1} STR files.")
print(f"Outputs written to: {TRANSLATED_STR_PATH}")


print("Copying STR files to zone_raw folder...")
for i in range(file_index + 1):
    file_index_str = f"{'' if i == 0 else i}"
    subprocess.run(["cp", TRANSLATED_STR_PATH + f"/patch{file_index_str}.str", f"zone_raw/patch{file_index_str}/english/localizedstrings/patch{file_index_str}.str"])
    print(f"Copied patch{file_index_str}.str to zone_raw folder.")
print("STR files copied to zone_raw folder.")

subprocess.run(["sh", "linker.sh"])
print("FF files generated in zone_out folder.")

print("Copying FF files to game zone folder...")
for i in range(file_index + 1):
    file_index_str = f"{'' if i == 0 else i}"
    subprocess.run(["cp", f"zone_out/patch{file_index_str}.ff" ,f"{GAME_DIRECTORY}/zone/english"])
    print(f"Copied patch{file_index_str}.ff to game zone folder.")
print("FF files copied to game zone folder.")