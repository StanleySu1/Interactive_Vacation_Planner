#!/bin/bash

mkdir -p data/scraped/tripadvisor
for city in `ls data/sources/tripadvisor/`; do
  echo $city
  python src/scrape_tripadvisor.py data/sources/tripadvisor/$city data/scraped/tripadvisor/$city.jsonl
done
