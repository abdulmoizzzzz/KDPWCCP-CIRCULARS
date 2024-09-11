# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KdpwccprojectItem(scrapy.Item):
    resolution_number = scrapy.Field()
    resolution_detail = scrapy.Field()
    pdf_link = scrapy.Field()
    
