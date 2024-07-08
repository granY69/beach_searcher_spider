# Beach Searcher Spider

This Python scraper, built with Scrapy, takes country URLs and dives deep into beach-searcher pages to uncover all its beaches. 
It follows the provided country link, meticulously gathers beach details, and stores them neatly in a JSON file, ready for further analysis.

## Goal:
- Extracting Complex Listing Structure and Extract Dynamic Prices
- Parse API responses and then request further child pages
- Implemented Download Delay to avoid server overloading.

## OS Platform:

Python 3 (Linux/Mac/WSL/Windows)

## Installing Dependencies:

To install dependencies open terminal and type:

```Bash
git clone https://github.com/seemab-yamin/beach_searcher_spider/
cd beach_searcher_spider
pip install -r requirements.txt
```

## Run:
First update config.json to add target urls in "start_urls" list in JSON dict.

```Bash
python3 main.py
```

## Video Demo:
[![Demo Video](https://i9.ytimg.com/vi/O9z-nWOISOU/mqdefault.jpg?sqp=CLSqsLQG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYACugWKAgwIABABGGUgVihVMA8=&rs=AOn4CLCwEIGC-P1Jl5xOSKRTgPPAPpRYjA)](https://youtu.be/O9z-nWOISOU)

## Resources:

- Scrapy: https://scrapy.org/