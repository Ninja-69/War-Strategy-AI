from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import time
import os

print("YOUTUBE TRANSCRIPT SCRAPER - REAL")
print("Target: 50,000 videos")

os.makedirs('data/youtube', exist_ok=True)

# Top military history channels
channels = {
    'Kings and Generals': [
        'mAUY1J8KizU', 'BqJbZiMTbhM', 'fZGW_zxA_Zc', 'ZRmA9rLfT_I',
        '8iNat48Q-1Y', 'FoH54conzGs', 'g-xKrbm2tKE', 'MqE_v4ktR7E'
    ],
    'Epic History': [
        'MXq-KbbKY94', '1_GUGLNgT9Y', 'uebInqG1pJI', '7IgB3PRx7UM'
    ]
}

all_transcripts = []
count = 0

print("Downloading transcripts...")

for channel, video_ids in channels.items():
    print(f"
{channel}:")
    
    for vid_id in video_ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid_id)
            
            full_text = ' '.join([t['text'] for t in transcript])
            
            all_transcripts.append({
                'video_id': vid_id,
                'channel': channel,
                'transcript': full_text[:2000],
                'url': f'https://youtube.com/watch?v={vid_id}'
            })
            
            count += 1
            print(f"  {count}. {vid_id[:8]}... OK")
            
            if count % 10 == 0:
                df = pd.DataFrame(all_transcripts)
                df.to_csv('data/youtube/transcripts.csv', index=False)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  {vid_id[:8]}... SKIP ({e})")
            continue

df = pd.DataFrame(all_transcripts)
df.to_csv('data/youtube/transcripts.csv', index=False)

print(f"
DONE! Scraped {len(all_transcripts)} real transcripts")
print(f"Saved to: data/youtube/transcripts.csv")
