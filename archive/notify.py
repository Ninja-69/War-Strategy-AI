import requests
import time
import subprocess

TOKEN = "8429449551:AAGPXBwSGGNMla8w8SEOhnIwQl5gfuTnUac"
CHAT_ID = "7909399410"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except:
        pass

print("Starting telegram notifications...")
send_telegram("🚀 Military AI Training Started!

You'll get updates every 5 minutes.")

while True:
    try:
        with open('training.log', 'r') as f:
            lines = f.readlines()
            # Get last 5 lines
            last_lines = ''.join(lines[-5:]).strip()
        
        msg = f"🤖 Training Update:

{last_lines}"
        send_telegram(msg)
    except Exception as e:
        send_telegram(f"⚠️ Error reading log: {str(e)}")
    
    time.sleep(300)  # 5 minutes
