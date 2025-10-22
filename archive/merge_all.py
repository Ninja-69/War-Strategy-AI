import pandas as pd
import glob
import os

print("MERGING ALL BATTLE DATA...")

all_files = glob.glob('data/**/*.csv', recursive=True)
print("Found " + str(len(all_files)) + " CSV files")

dfs = []
for file in all_files:
    try:
        df = pd.read_csv(file, on_bad_lines='skip')
        print("OK " + file + ": " + str(len(df)) + " rows")
        dfs.append(df)
    except Exception as e:
        print("ERROR " + file + ": " + str(e))

print("Merging all data...")
merged = pd.concat(dfs, ignore_index=True)
print("Total rows before dedup: " + str(len(merged)))

print("Removing duplicates...")
merged_clean = merged.drop_duplicates()
print("Total rows after dedup: " + str(len(merged_clean)))
print("Removed " + str(len(merged) - len(merged_clean)) + " duplicates")

output = 'military_battles_dataset_100k.csv'
merged_clean.to_csv(output, index=False)
size_mb = os.path.getsize(output) / 1024 / 1024
print("Saved to: " + output)
print("File size: " + str(round(size_mb, 2)) + " MB")
print("DONE!")
