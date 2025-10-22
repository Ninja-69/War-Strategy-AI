import requests
import time
import os

TOKEN = "8429449551:AAGPXBwSGGNMla8w8SEOhnIwQl5gfuTnUac"
CHAT_ID = "7909399410"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=10)
        print(f"Sent: {message[:50]}...")
    except Exception as e:
        print(f"Error sending: {e}")

print("🚀 Starting training notifications...")
send_telegram("🚀 Training notification system started!

You'll get updates every 5 minutes.")

while True:
    try:
        # Read last 10 lines of training log
        with open('training.log', 'r') as f:
            lines = f.readlines()
            if len(lines) > 10:
                last_lines = lines[-10:]
            else:
                last_lines = lines
        
        # Find the progress line (contains %)
        progress_line = None
        for line in reversed(last_lines):
            if '%' in line and '|' in line:
                progress_line = line.strip()
                break
        
        if progress_line:
            # Extract percentage
            if '%|' in progress_line:
                pct = progress_line.split('%|')[0].split()[-1]
                msg = f"⚔️ Training Update:

Progress: {pct}%

{progress_line[-100:]}"
            else:
                msg = f"⚔️ Training Update:

{progress_line[-200:]}"
        else:
            msg = f"⚔️ Training Update:

{''.join(last_lines[-3:])}"
        
        send_telegram(msg)
        
    except FileNotFoundError:
        send_telegram("⚠️ Training log not found!")
    except Exception as e:
        print(f"Error: {e}")
    
    # Wait 5 minutes
    time.sleep(300)
