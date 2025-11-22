import csv
import json
import glob
import os

# Folder with CSV exports
csv_folder = "imports"

# Path to your whitelist
whitelist_file = "whitelist.json"

# Load existing whitelist
try:
    with open(whitelist_file, "r") as f:
        whitelist = set(json.load(f))
except FileNotFoundError:
    whitelist = set()

# Process all CSV files in the folder
csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))

for csv_file in csv_files:
    print(f"Processing {csv_file}...")
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("Email Address")  # Adjust if your CSV uses a different header
            if email:
                whitelist.add(email.lower().strip())

# Save back to whitelist.json
with open(whitelist_file, "w") as f:
    json.dump(sorted(list(whitelist)), f, indent=4)

print(f"Whitelist updated with {len(whitelist)} emails from {len(csv_files)} CSV file(s).")
