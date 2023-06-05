# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
from time import time


# This pipeline class will process and store the scraped data
class SpeedSkatingPipeline:
    # Time markers for calculating the time taken for scraping
    start = 0
    end = 0

    def __init__(self):
        # A list to store the scraped data
        self.athlete_info_list = []
        # Record the start time at initialization
        self.start = time()

    def process_item(self, item, spider):
        self.athlete_info_list.append(item)
        return item

    # This method is called when the spider is closed
    def close_spider(self, spider):
        df = pd.DataFrame(self.athlete_info_list)
        self.end = time()
        print(df)
        print(self.end - self.start)
        df.to_csv("scrapy_data.csv", index=False)
