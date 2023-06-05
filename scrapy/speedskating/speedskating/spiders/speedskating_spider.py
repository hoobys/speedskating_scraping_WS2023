import scrapy
import pandas as pd

limit_athletes = True


class SpeedSkatingSpider(scrapy.Spider):
    name = "speedskating"
    max_profiles = 100 if limit_athletes else float("inf")
    i = 0
    profile_count = 0
    page_increment = 66
    base_url = "https://speedskatingresults.com/index.php?p=21&g=9999&i={}"

    def start_requests(self):
        yield scrapy.Request(self.base_url.format(0), callback=self.parse_main_page)

    def parse_main_page(self, response):
        athlete_links = response.css("td.name a::attr(href)").getall()

        if not athlete_links:
            return

        for link in athlete_links:
            self.profile_count += 1
            if self.profile_count > self.max_profiles:
                break

            yield response.follow(link, callback=self.parse_athlete_profile)

        self.i += self.page_increment

        if self.profile_count < self.max_profiles:
            yield response.follow(
                self.base_url.format(self.i), callback=self.parse_main_page
            )

    def parse_athlete_profile(self, response):
        name = response.css("h1.underline::text").get().strip()
        country = response.css('a[href *="p=46"]::text').get().strip()
        birthdate = response.css("span.date::text").get().strip()

        records_table = response.xpath("/html/body/div[1]/div/main/table[1]//tr")

        records = {}
        for row in records_table:
            cells = row.css("td")
            if len(cells) > 1:
                distance = cells[0].css("::text").get().strip()
                time = cells[1].css("::text").get().strip()
                if distance:
                    records[distance] = time

        athlete_info = {
            "Name": name,
            "Country": country,
            "Birthdate": birthdate,
            **(records if records else {}),
        }

        yield athlete_info
