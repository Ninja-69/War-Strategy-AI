import requests
import pandas as pd
import time

print("ARCHIVE.ORG MILITARY BOOKS SCRAPER")

books = {
    'Art of War': 'artofwar00suntuoft',
    'On War': 'onwar00clau',
    'The Prince': 'prince00machiala',
    'Book of Five Rings': 'bookoffiverings00miya',
    'Strategy': 'strategy00liddrich'
}

extracts = []

for title, book_id in books.items():
    print(f"Downloading: {title}...")
    try:
        url = f"https://archive.org/stream/{book_id}/{book_id}_djvu.txt"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            text = response.text
            sections = [text[i:i+2000] for i in range(0, len(text), 2000)]
            
            for idx, section in enumerate(sections[:10]):
                if len(section) > 100:
                    extracts.append({
                        'book': title,
                        'section': idx + 1,
                        'text': section,
                        'source': 'Archive.org'
                    })
            
            print(f"  OK {title}: {len(sections[:10])} sections")
        
        time.sleep(2)
        
    except:
        print(f"  SKIP {title}")

df = pd.DataFrame(extracts)
df.to_csv('data/strategy_books.csv', index=False)
print(f"DONE! {len(extracts)} book sections")
