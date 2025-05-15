# Crawling-E-commerce-platforms-Customer-reviews

## Overview
This project collects comments from three different e-commerce platforms using Selenium for web scraping. It stores documentation in a log file, saves the extracted data in a data folder, and includes bot detection to identify potentially generated comments.

## Features
- Automated comment collection via Selenium.
- Storage and logging of scraped data.
- Bot detection to filter out synthetic comments.
- Well-structured data organization.

## Project Structure
📂 E-Commerce-Comments-Scraper ├── 📂 data                  # Contains collected comment data │   ├── bot-detected_data.csv │   ├── cellphones.csv │   ├── tgdd.csv │   ├── tinhte.csv ├── 📂 logs                  # Log files documenting the scraping process │   ├── crawler.log ├── 📂 src                   # Source code files │   ├── bot_detector.py      # Bot detection logic │   ├── cellphones_crawler.py # Scraper for cellphones site │   ├── logger.py            # Logging utility │   ├── main.py              # Main execution script │   ├── thegioididong_crawler.py # Scraper for TGDD site │   ├── tinhte_crawler.py    # Scraper for Tinhte site │   ├── utils.py             # Helper functions ├── README.md                # Project documentation
