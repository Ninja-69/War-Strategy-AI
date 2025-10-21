#!/bin/bash

while true; do
    DATE=$(date +%Y%m%d_%H%M%S)
    
    # Backup all CSV files
    mkdir -p backups
    tar -czf backups/battles_backup_$DATE.tar.gz data/*.csv data/*/*.csv 2>/dev/null
    
    # Count and log
    TOTAL=$(find data -name "*.csv" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
    echo "$DATE - $TOTAL battles backed up" >> backups/progress.log
    
    # Keep only last 10 backups
    cd backups
    ls -t battles_backup_*.tar.gz | tail -n +11 | xargs rm -f 2>/dev/null
    cd ..
    
    # Wait 30 minutes
    sleep 1800
done
