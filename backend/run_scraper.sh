#!/bin/bash
for i in {1..6}
do
  python3 /home/ubuntu/ticket-scraper/backend/scrape.py
  sleep 10
done
