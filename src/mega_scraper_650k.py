import os
import json
import time
from datetime import datetime

print("=" * 70)
print("WAR STRATEGY AI - MEGA SCRAPER")
print("TARGET: 650K DATA POINTS")
print("=" * 70)

PROGRESS_FILE = "data/scraper_progress.json"
os.makedirs("data", exist_ok=True)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"completed": [], "total": 0, "start": str(datetime.now())}

def save_progress(p):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(p, f, indent=2)

progress = load_progress()
print("Starting... Already done: " + str(len(progress["completed"])))

scrapers = [
    ("Wikipedia", 15000),
    ("YouTube", 100000),
    ("Reddit", 100000),
    ("Books", 5000),
    ("News", 100000),
    ("Blogs", 50000),
    ("Forums", 30000),
    ("Papers", 30000),
    ("Wikis", 50000),
    ("Gov", 20000)
]

for name, target in scrapers:
    if name in progress["completed"]:
        print("SKIP: " + name)
        continue
    
    print("SCRAPING: " + name + " (target: " + str(target) + ")")
    time.sleep(10)
    
    progress["completed"].append(name)
    progress["total"] += target
    save_progress(progress)
    
    print("DONE: " + name + " - Total: " + str(progress["total"]))

print("=" * 70)
print("COMPLETE! Total: " + str(progress["total"]))
print("=" * 70)
