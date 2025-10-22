#!/bin/bash

while true; do
    echo "=== Checking scrapers at $(date) ==="
    
    # Check if beast mode is still running
    if ! tmux has-session -t beast 2>/dev/null; then
        echo "⚠️  Beast mode died! Restarting..."
        tmux new -d -s beast "cd /opt/war-room/War-Strategy-AI && python3 src/beast_scraper.py > beast.log 2>&1"
    fi
    
    # Check if massive scraper is still running
    if ! tmux has-session -t massive 2>/dev/null; then
        echo "⚠️  Massive scraper died! Restarting..."
        tmux new -d -s massive "cd /opt/war-room/War-Strategy-AI && python3 src/massive_scraper.py > massive.log 2>&1"
    fi
    
    # Check if enhancer is still running
    if ! tmux has-session -t enhancer 2>/dev/null; then
        echo "⚠️  Enhancer died! Restarting..."
        tmux new -d -s enhancer "cd /opt/war-room/War-Strategy-AI && python3 src/enhance_battles.py > enhance.log 2>&1"
    fi
    
    # Count total battles
    TOTAL=$(find data -name "*.csv" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
    echo "✅ Total battles: $TOTAL"
    
    # Stop if we hit 100k
    if [ "$TOTAL" -gt 100000 ]; then
        echo "🔥🔥🔥 HIT 100K! STOPPING ALL SCRAPERS! 🔥🔥🔥"
        tmux kill-session -t beast 2>/dev/null
        tmux kill-session -t massive 2>/dev/null
        tmux kill-session -t enhancer 2>/dev/null
        echo "✅ ALL STOPPED! Check data/ folder"
        exit 0
    fi
    
    # Wait 5 minutes before checking again
    sleep 300
done
