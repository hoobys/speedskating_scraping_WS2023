import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from time import time

# Boolean variable to limit the number of profiles to scrape
limit_profiles = True


# This function scrapes athlete profile information from a given URL
def scrape_athlete_profile(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tree = html.fromstring(response.content)

    # Extract name, country, and birth date
    name = soup.find("h1", class_="underline").text.strip()
    country = soup.find("a", href=lambda href: href and "p=46" in href).text.strip()
    birthdate = soup.find("span", class_="date").text.strip()

    # Extract personal records
    records_table = tree.xpath("/html/body/div[1]/div/main/table[1]//tr")
    records = {}
    for row in records_table:
        cells = row.xpath("td")
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


# This function scrapes URLs of athlete profiles from a given URL
def scrape_athlete_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    athlete_info = []

    # Extract profile URL and add to list
    for row in soup.find_all("tr"):
        name_cells = row.find_all("td", class_="name")
        for cell in name_cells:
            profile_url = cell.find("a")["href"] if cell.find("a") else None
            athlete_info.append(profile_url)

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

    # Continue scraping while there are still profiles
    while profile_count < max_profiles:
        # Construct URL for next page
        url = url_base.format(i)
        athlete_urls = scrape_athlete_info(url)

        # If no athlete URLs found, break loop
        if not athlete_urls:
            break

        # Visit each athlete URL and scrape profile data
        for url in athlete_urls:
            if profile_count >= max_profiles:
                break
            full_url = f"https://speedskatingresults.com/{url}"
            athlete_info = scrape_athlete_profile(full_url)
            data.append(athlete_info)
            profile_count += 1

        # Move to next page
        i += page_increment

    df = pd.DataFrame(data)
    return df


start = time()
df = scrape_pages()
end = time()
print(df)
print(end - start)
df.to_csv("soup_data.csv", index=False)
