#!/bin/bash

LOCKFILE="/home/ubuntu/ticket-scraper/backend/scraper_cycle.lock"

# Function to clean up the lock file upon exit
cleanup() {
    rm -f "$LOCKFILE"
    exit
}

# Trap signals to ensure cleanup is done
trap "cleanup" INT TERM EXIT

# Check if lock file exists and the process is running
if [ -e "$LOCKFILE" ]; then
    PID=$(cat "$LOCKFILE")
    if kill -0 "$PID" 2>/dev/null; then
        exit 1
    else
        rm -f "$LOCKFILE"
    fi
fi

# Create a new lock file with current PID
echo $$ > "$LOCKFILE"

# Ensure the lock file is removed on exit
trap "cleanup" INT TERM EXIT


# Run the Python script 6 times with a 10-second interval, log each run
for i in {1..6}
do
    # Use xvfb-run to ensure a virtual display environment for headless Chrome
    xvfb-run -a python3 /home/ubuntu/ticket-scraper/backend/scrape.py 
    sleep 10
done


