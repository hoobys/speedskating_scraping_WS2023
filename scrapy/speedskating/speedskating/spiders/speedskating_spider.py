import scrapy

# Boolean variable to limit the number of profiles to scrape
limit_athletes = True


# Spider for scraping speedskating data
class SpeedSkatingSpider(scrapy.Spider):
    name = "speedskating"
    max_profiles = 100 if limit_athletes else float("inf")
    # Variables for managing pagination
    i = 0
    profile_count = 0
    page_increment = 66
    base_url = "https://speedskatingresults.com/index.php?p=21&g=9999&i={}"

    # Initial request
    def start_requests(self):
        # Start at page 0 and call parse_main_page method on response
        yield scrapy.Request(self.base_url.format(0), callback=self.parse_main_page)

    # Parse main page of the website (listing of athletes)
    def parse_main_page(self, response):
        # Extract athlete profile links
        athlete_links = response.css("td.name a::attr(href)").getall()

        # If no links found, stop
        if not athlete_links:
            return

        for link in athlete_links:
            self.profile_count += 1
            # If the maximum number of profiles has been scraped, stop
            if self.profile_count > self.max_profiles:
                break

            # Follow the link to the athlete's profile and call parse_athlete_profile on response
            yield response.follow(link, callback=self.parse_athlete_profile)

        # Increment the page number
        self.i += self.page_increment

        # If there are still profiles left to scrape, request the next page
        if self.profile_count < self.max_profiles:
            yield response.follow(
                self.base_url.format(self.i), callback=self.parse_main_page
            )

    # Parse an individual athlete's profile
    def parse_athlete_profile(self, response):
        # Extract name, country, and birth date
        name = response.css("h1.underline::text").get().strip()
        country = response.css('a[href *="p=46"]::text').get().strip()
        birthdate = response.css("span.date::text").get().strip()

        # Extract personal records
        records_table = response.xpath("/html/body/div[1]/div/main/table[1]//tr")
        records = {}
        for row in records_table:
            cells = row.css("td")
            if len(cells) > 1:
                distance = cells[0].css("::text").get().strip()
                time = cells[1].css("::text").get().strip()
                if distance:
                    records[distance] = time

        # Combine all scraped data
        athlete_info = {
            "Name": name,
            "Country": country,
            "Birthdate": birthdate,
            **(records if records else {}),
        }

        # Yield the dictionary, which will be output by the spider
        yield athlete_info
