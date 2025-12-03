import json

# Read the exported JSON file
EXPORTED_PATH = "translation/exported"
EXPORTED_JSON_PATH = f"{EXPORTED_PATH}/json"
EXPORTED_JSON = f"{EXPORTED_JSON_PATH}/all_strings.json"

with open(EXPORTED_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# Calculate total character count
character_count = 0
for entries in data.values():
    for text in entries.values():
        character_count += len(text)

print(f"Total string entries in JSON: {character_count}")

# Character limit check
if character_count > 500000:
    print(f"Warning: Total character count exceeds for DeepL (max 500,000, current {character_count}).")
    print("Optimizing translation process by splitting the JSON...")

    part_size = 490000  # Target maximum characters per part
    parts = []
    current_part = {}
    current_size = 0

    for filename, entries in data.items():
        if filename not in current_part:
            current_part[filename] = {}

        for key, text in entries.items():
            text_length = len(text)

            # If the current part size is exceeded, create a new part
            if current_size + text_length > part_size and current_size > 0:
                parts.append(current_part)
                current_part = {filename: {}}
                current_size = 0

            current_part[filename][key] = text
            current_size += text_length

    if current_part:
        parts.append(current_part)

    # Save parts as separate JSON files
    for idx, part in enumerate(parts):
        part_filename = f"{EXPORTED_JSON_PATH}/all_strings_part{idx + 1}.json"
        with open(part_filename, "w", encoding="utf-8") as pf:
            json.dump(part, pf, ensure_ascii=False, indent=2)
        # Approximate character count
        approx_chars = sum(len(t) for entries in part.values() for t in entries.values())
        print(f"Wrote {part_filename} with approximately {approx_chars} characters.")

else:
    print("Character count is within acceptable limits for DeepL translation.")
