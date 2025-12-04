import json
import os
import subprocess

# --- CONFIGURATION AND CONSTANTS ---

# Convert to Latin alphabet (for Turkish characters)
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
TRANSLATED_PATH = f"{TRANSLATION_PATH}/translated"
TRANSLATED_JSON_PATH = f"{TRANSLATED_PATH}/json"
TRANSLATED_STR_PATH = f"{TRANSLATED_PATH}/str"
TRANSLATED_JSON = f"{TRANSLATED_JSON_PATH}/translated.json.tr.json"
CHUNK_SIZE = 7000   # Every N entries, create a new STR file

# Group game maps by Act (with .str extensions)
ACT_MISSION_FILES = {
    "ACT1": [
        "ny_harbor.str", "hijack.str", "london.str", "hamburg.str", "innocent.str", "intro.str",
    ],
    "ACT2": [
        "warlord.str", "paris_a.str", "payback.str", "prague.str", "rescue_2.str", "castle.str", "prague_escape.str",
    ],
    "ACT3": [
        "ny_manhattan.str", "berlin.str", "dubai.str", "paris_b.str", "paris_ac130.str",
    ],
}

# Files and key patterns to exclude (MP/SO/UI etc.)
EXCLUDED_FILES = {
    "patch_mp.str", "localized_ui_mp.str", "common_mp.str", # Completely MP/SO files
}
EXCLUDED_KEY_PATTERNS = {
    "CHALLENGE_", "UAV_", "MP_", "MPUI_", "PLAYERCARDS_", "EXE_", "GAME_", "PLATFORM_", "PERKS_",
    "PRESENCE_", "SPLASHES_", "XBOXLIVE_", "COOP_", "CLANS_", "KEY_", "PAINTER_", "KILLSTREAKS_",
    "CREDIT_", "SO_"
}

# --- INITIAL LOADING AND FILTERING ---

os.makedirs(TRANSLATED_STR_PATH, exist_ok=True)

with open(TRANSLATED_JSON, "r", encoding="utf-8") as f:
    all_json_data = json.load(f)

# Collect all mission files in a single set
all_mission_files = set()
for file_list in ACT_MISSION_FILES.values():
    all_mission_files.update(file_list)

# Identify Core UI (Menu) files: Everything not excluded and not a mission file.
core_ui_data = {}
for filename, entries in all_json_data.items():
    if filename not in EXCLUDED_FILES and filename not in all_mission_files:
        
        # Also clean MP/SO keys from UI/Core files
        filtered_entries = {}
        for ref, text in entries.items():
             if not any(ref.startswith(pattern) for pattern in EXCLUDED_KEY_PATTERNS):
                filtered_entries[ref] = text
        
        if filtered_entries:
            core_ui_data[filename] = filtered_entries


# --- WRITE FUNCTIONS ---

def write_header(f, name_without_ext):
    """Writes STR file header."""
    f.write(f'// Dumped from fastfile "{name_without_ext}".\n')
    f.write('// This file is part of the custom Turkish Localization Patch.\n')
    f.write('VERSION             "1"\n')
    f.write('CONFIG              "C:/trees/cod3/cod3/bin/StringEd.cfg"\n')
    f.write('FILENOTES           ""\n\n')

def open_new_file(act_name, idx):
    """Opens a new split STR file."""
    filename = f"patch_{act_name}{'_' + str(idx) if idx > 1 else ''}.str"
    path = os.path.join(TRANSLATED_STR_PATH, filename)
    f = open(path, "w", encoding="utf-8")
    write_header(f, filename.replace(".str", ""))
    return f, filename

def process_and_split_act(act_name, mission_files):
    """Merges specific Act and Core UI data and splits into STR files according to limits."""
    
    # 1. Collect all data (Core UI + Act Missions)
    act_data = core_ui_data.copy()
    total_entry_count = 0

    for filename in mission_files:
        if filename in all_json_data:
            # Only get valid keys from mission files
            for ref, text in all_json_data[filename].items():
                if not any(ref.startswith(pattern) for pattern in EXCLUDED_KEY_PATTERNS):
                    act_data[ref] = text # This simple copy logic loses filename info,
                                        # but works under the assumption of unique keys (no collision).
                                        # More correct method below, merging in a single dict.
                    
    
    # Combine all Core UI and Act data into a single list
    all_combined_entries = {}
    
    # Add Core UI first
    for filename, entries in core_ui_data.items():
        all_combined_entries.update(entries)
        
    # Then add Act mission files (if same key exists, Core UI is overwritten)
    for filename in mission_files:
        if filename in all_json_data:
            for ref, text in all_json_data[filename].items():
                if not any(ref.startswith(pattern) for pattern in EXCLUDED_KEY_PATTERNS):
                    all_combined_entries[ref] = text # Çakışmayı burada çözüyoruz

    # 2. Split into STR files
    file_index = 1
    entry_count = 0
    
    print(f"\n--- Creating STR Files for {act_name} (Total: {len(all_combined_entries)} keys) ---")
    
    # Open the first file
    out_file, current_name = open_new_file(act_name, file_index)
    
    for ref, text in all_combined_entries.items():

        # If chunk is full, open a new file
        if entry_count > 0 and entry_count % CHUNK_SIZE == 0:
            out_file.write("ENDMARKER")
            out_file.close()
            file_index += 1
            out_file, current_name = open_new_file(act_name, file_index)
            
        safe_text = json.dumps(text, ensure_ascii=False)[1:-1]
        safe_text = safe_text.translate(LANGUAGE_MAP_TO_LATIN)

        out_file.write(f'REFERENCE           {ref}\n')
        out_file.write(f'LANG_ENGLISH        "{safe_text}"\n\n')

        entry_count += 1
    
    # Close the last file
    out_file.write("ENDMARKER")
    out_file.close()
        
    # Print the localize list needed for Linker
    print(f"\n[Suggested Linker (.zone) Content for {act_name}]:")
    zone_content = [f'localize,patch_{act_name}{'_' + str(i) if i > 0 else ''}' for i in range(1, file_index + 1)]
    print('  ' + '\n  '.join(zone_content))
    
    return file_index # Number of files created

# --- MAIN EXECUTION PART ---

for act, files in ACT_MISSION_FILES.items():
    process_and_split_act(act, files)


print("\n\n#####################################################################")
print("✅ STR files successfully split and created.")
print(f"Outputs are in the {TRANSLATED_STR_PATH} folder.")
print("#####################################################################")



print("Copying STR files to zone_raw folder...")
for act_name in ACT_MISSION_FILES.keys():
    subprocess.run(["cp", TRANSLATED_STR_PATH + f"/patch_{act_name}.str", f"zone_raw/patch_{act_name}/english/localizedstrings/patch_{act_name}.str"])
    print(f"Copied patch_{act_name}.str to zone_raw folder.")
print("STR files copied to zone_raw folder.")


subprocess.run(["sh", "linker.sh"])
print("FF files generated in zone_out folder.")


print("Copying FF files to game zone folder...")
for act_name in ACT_MISSION_FILES.keys():
    subprocess.run(["cp", f"zone_out/patch_{act_name}.ff" ,f"{GAME_DIRECTORY}/zone/english"])
    print(f"Copied patch_{act_name}.ff to game zone folder.")
print("FF files copied to game zone folder.")