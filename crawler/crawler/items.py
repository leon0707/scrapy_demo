# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PatentItem(scrapy.Item):
    title = scrapy.Field()
    patent_number = scrapy.Field()
    abstract = scrapy.Field()
    type = scrapy.Field()
    date_filed = scrapy.Field()
    date_issued = scrapy.Field()
    assignees = scrapy.Field()
    inventors = scrapy.Field()
    url = scrapy.Field()
    crawled_date = scrapy.Field()
    location = scrapy.Field()
