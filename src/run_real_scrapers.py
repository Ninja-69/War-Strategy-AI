import subprocess
import time

scrapers = [
    ("Wikipedia", "src/scrape_wikipedia_real.py"),
    ("YouTube", "src/scrape_youtube_real.py"),
    ("Reddit", "src/scrape_reddit_real.py")
]

print("MASTER SCRAPER - RUNNING ALL 3")
print("=" * 70)

for name, script in scrapers:
    print("")
    print("STARTING: " + name)
    print("=" * 70)
    
    try:
        subprocess.run(["python3", script], check=True)
        print("COMPLETE: " + name)
    except:
        print("FAILED: " + name)
    
    print("Cooling down 30 seconds...")
    time.sleep(30)

print("")
print("=" * 70)
print("ALL SCRAPERS COMPLETE!")
print("=" * 70)
