import requests
import pandas as pd
import time
import os

print("REDDIT SCRAPER - REAL")
print("Target: 50,000 posts")

os.makedirs('data/reddit', exist_ok=True)

subreddits = [
    'MilitaryHistory', 'AskHistorians', 'WarCollege', 
    'CredibleDefense', 'history', '战争历史'
]

all_posts = []

print("Scraping Reddit...")

for sub in subreddits:
    print(f"
r/{sub}:")
    
    try:
        url = f'https://www.reddit.com/r/{sub}/top.json?limit=100&t=all'
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        for post in data['data']['children']:
            p = post['data']
            all_posts.append({
                'subreddit': sub,
                'title': p['title'],
                'selftext': p.get('selftext', '')[:500],
                'score': p['score'],
                'url': f"https://reddit.com{p['permalink']}"
            })
        
        print(f"  Got {len(data['data']['children'])} posts (Total: {len(all_posts)})")
        
        if len(all_posts) % 100 == 0:
            df = pd.DataFrame(all_posts)
            df.to_csv('data/reddit/posts.csv', index=False)
        
        time.sleep(2)
        
    except Exception as e:
        print(f"  Error: {e}")
        continue

df = pd.DataFrame(all_posts)
df.to_csv('data/reddit/posts.csv', index=False)

print(f"
DONE! Scraped {len(all_posts)} real posts")
print(f"Saved to: data/reddit/posts.csv")
