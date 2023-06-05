from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from time import time

# Boolean variable to limit the number of profiles to scrape
limit_profiles = True


# This function scrapes athlete profile information from a given URL using Selenium
def scrape_athlete_profile(driver, url):
    driver.get(url)

    # Extract name, country, and birth date using CSS selectors
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

    # Combine all scraped data
    athlete_info = {
        "Name": name,
        "Country": country,
        "Birthdate": birthdate,
        **(records if records else {}),
    }

    return athlete_info


# This function scrapes URLs of athlete profiles from a given URL using Selenium
def scrape_athlete_info(driver, url):
    driver.get(url)

    athlete_info = []

    # Find all links in name cells
    links = driver.find_elements(By.CSS_SELECTOR, "td.name a")
    # Extract the href attribute of each link and add it to the list
    for link in links:
        athlete_info.append(link.get_attribute("href"))

    return athlete_info


# This function iterates over multiple pages and uses the above functions to scrape data
def scrape_pages():
    # URL pattern, where each page URL is constructed by substituting a page number
    url_base = "https://speedskatingresults.com/index.php?p=21&g=9999&i={}"
    page_increment = 66  # Pagination increment
    max_profiles = 100 if limit_profiles else float("inf")

    i = 0
    profile_count = 0
    data = []

    # Start the webdriver
    driver = webdriver.Chrome()

    # Continue scraping while there are still profiles
    while profile_count < max_profiles:
        # Construct URL for next page
        url = url_base.format(i)
        athlete_urls = scrape_athlete_info(driver, url)

        # If no athlete URLs found, break loop
        if not athlete_urls:
            break

        # Visit each athlete URL and scrape profile data
        for url in athlete_urls:
            if profile_count >= max_profiles:
                break
            athlete_info = scrape_athlete_profile(driver, url)
            data.append(athlete_info)
            profile_count += 1

        # Move to next page
        i += page_increment

    # Close the webdriver after scraping is complete
    driver.quit()

    df = pd.DataFrame(data)
    return df


start = time()
df = scrape_pages()
end = time()
print(df)
print(end - start)
df.to_csv("selenium_data.csv", index=False)
