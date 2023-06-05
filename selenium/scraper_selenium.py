from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import time

limit_profiles = True


def scrape_athlete_profile(driver, url):
    driver.get(url)

    # Extract name, country, and birth date
    name = driver.find_element(By.CSS_SELECTOR, "h1.underline").text
    country = driver.find_element(By.CSS_SELECTOR, 'a[href*="p=46"]').text
    birthdate = driver.find_element(By.CSS_SELECTOR, "span.date").text

    # Extract personal records
    records_table = driver.find_elements(By.CSS_SELECTOR, "main > .skaterrecords tr")

    records = {}
    for row in records_table:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > 1:
            distance = cells[0].text.strip()
            time = cells[1].text.strip()
            if distance:
                records[distance] = time

    athlete_info = {
        "Name": name,
        "Country": country,
        "Birthdate": birthdate,
        **(records if records else {}),
    }

    return athlete_info


def scrape_athlete_info(driver, url):
    driver.get(url)

    athlete_info = []

    links = driver.find_elements(By.CSS_SELECTOR, "td.name a")
    for link in links:
        athlete_info.append(link.get_attribute("href"))

    return athlete_info


def scrape_pages():
    url_base = "https://speedskatingresults.com/index.php?p=21&g=9999&i={}"
    page_increment = 66
    max_profiles = 100 if limit_profiles else float("inf")

    i = 0
    profile_count = 0
    data = []

    # Start the webdriver
    driver = webdriver.Chrome()
    driver.find_elements()

    while profile_count < max_profiles:
        url = url_base.format(i)
        athlete_urls = scrape_athlete_info(driver, url)

        if not athlete_urls:
            break

        for url in athlete_urls:
            if profile_count >= max_profiles:
                break
            athlete_info = scrape_athlete_profile(driver, url)
            data.append(athlete_info)
            profile_count += 1

        i += page_increment

    # Close the webdriver
    driver.quit()

    df = pd.DataFrame(data)
    return df


start = time()
df = scrape_pages()
end = time()
print(df)
print(end - start)
df.to_csv("selenium_data.csv", index=False)
