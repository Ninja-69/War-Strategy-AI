import wikipedia
import pandas as pd
import time
from datetime import datetime
from multiprocessing import Pool, Manager
import sys

def scrape_worker(args):
    worker_id, categories, shared_count = args
    battles = []
    
    for cat in categories:
        try:
            results = wikipedia.search(f"{cat}", results=2000)
            for title in results:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    battles.append({
                        "title": page.title,
                        "summary": page.summary[:3000],
                        "url": page.url,
                        "category": cat,
                        "worker": worker_id
                    })
                    
                    with shared_count.get_lock():
                        shared_count.value += 1
                    
                    if len(battles) % 50 == 0:
                        df = pd.DataFrame(battles)
                        df.to_csv(f"data/worker_{worker_id}_battles.csv", index=False)
                    
                    time.sleep(0.3)  # FAST!
                    
                except:
                    continue
        except:
            continue
    
    return battles

if __name__ == "__main__":
    all_categories = [
        "Battle", "War", "Conflict", "Siege", "Campaign", "Military operation",
        "Naval battle", "Air battle", "Tank battle", "Ancient warfare",
        "Medieval warfare", "Early modern warfare", "Modern warfare",
        "World War I battles", "World War II battles", "Napoleonic battles",
        "American Civil War battles", "Vietnam War battles", "Korean War battles",
        "Gulf War", "Iraq War", "Afghanistan War", "Syrian Civil War",
        "Colonial wars", "Revolutionary wars", "Independence wars",
        "Crusades", "Mongol invasions", "Viking raids", "Conquests",
        "Rebellions", "Uprisings", "Revolutions", "Coups", "Insurgencies",
        "Guerrilla warfare", "Partisan warfare", "Resistance movements",
        "Special operations", "Commando raids", "Airborne operations",
        "Amphibious warfare", "Submarine warfare", "Naval warfare",
        "Aerial warfare", "Strategic bombing", "Tactical operations"
    ]
    
    print("="*80)
    print("🔥 BEAST MODE - 12 PARALLEL WORKERS - 200K TARGET! 🔥")
    print(f"Started: {datetime.now()}")
    print("="*80)
    
    manager = Manager()
    shared_count = manager.Value('i', 0)
    
    # Split categories among 12 workers
    chunk_size = len(all_categories) // 12 + 1
    tasks = []
    for i in range(12):
        start = i * chunk_size
        end = min(start + chunk_size, len(all_categories))
        tasks.append((i, all_categories[start:end], shared_count))
    
    # Launch 12 workers!
    with Pool(processes=12) as pool:
        results = pool.map(scrape_worker, tasks)
    
    # Combine and dedupe
    all_battles = []
    for result in results:
        all_battles.extend(result)
    
    df = pd.DataFrame(all_battles)
    df = df.drop_duplicates(subset=["title"])
    df.to_csv("data/beast_mode_battles.csv", index=False)
    
    print("="*80)
    print(f"🔥 BEAST MODE DONE! {len(df)} battles")
    print("="*80)
