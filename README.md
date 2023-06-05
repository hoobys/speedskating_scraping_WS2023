# Speedskating Results Web Scrapers

Authors: Hubert Wojewoda, Michał Grzyb

This repository is a final project for WS2023 WNE course. It contains three Python web scrapers designed to extract athlete information from a speedskating results website. The scrapers are implemented using BeautifulSoup, Selenium, and Scrapy respectively.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- BeautifulSoup4
- lxml
- pandas
- requests
- Selenium WebDriver
- Scrapy

You can install the Python packages with pip:

```bash
pip install beautifulsoup4 lxml pandas requests selenium scrapy
```

For Selenium, you will also need to have the appropriate WebDriver installed.

## Usage

To run the scripts, navigate to the directory containing the script you want to run, and execute the Python file from the command line.

For the BeautifulSoup scraper:

```bash
cd soup/
python scraper_bs.py
```

For the Selenium scraper:

```bash
cd selenium/
python scraper_selenium.py
```

For the Scrapy scraper:

```bash
cd scrapy/speedskating
scrapy crawl speedskating
```

Each script will generate a CSV file (soup_data.csv, selenium_data.csv, or scrapy_data.csv) in the same directory containing the scraped data. By default, each script will scrape a maximum of 100 athlete profiles; you can adjust this limit in the script's code if you wish.
