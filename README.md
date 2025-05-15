# Crawling-E-commerce-platforms-Customer-reviews

## Overview
This project collects comments from three different e-commerce platforms using Selenium for web scraping. It stores documentation in a log file, saves the extracted data in a data folder, and includes bot detection to identify potentially generated comments.

## Features
- Automated comment collection via Selenium.
- Storage and logging of scraped data.
- Bot detection to filter out synthetic comments.
- Well-structured data organization.

## Project Structure
├── data/
│   ├── bot-detected_data.csv
│   ├── cellphones.csv
│   ├── tgdd.csv
│   ├── tinhte.csv
│
├── logs/
│   ├── crawler.log
│
├── src/
│   ├── bot_detector.py
│   ├── cellphones_crawler.py
│   ├── logger.py
│   ├── main.py
│   ├── thegioididong_crawler.py
│   ├── tinhte_crawler.py
│   ├── utils.py
│
├── README.md
