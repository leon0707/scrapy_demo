# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
from urllib.parse import urlparse
from crawler.items import PatentItem


class PatentSpider(scrapy.Spider):
    name = 'patent'
    allowed_domains = ['justia.com']
    start_urls = ['https://patents.justia.com/assignee/uber-technologies-inc',
                  'https://patents.justia.com/company/linkedin',
                  'https://patents.justia.com/assignee/airbnb-inc']

    def parse(self, response):
        if response.status == 200:
            parsed_url = urlparse(response.url)
            patents = response.xpath('//div[@id="search-results"]/ul//li')
            for patent in patents:
                patent_url = patent.xpath('.//div[@class="head"]//a/@href').extract_first()
                title = patent.xpath('.//div[@class="head"]//a/text()').extract_first()
                combined_url = '{url.scheme}://{url.netloc}{patent_url}'.format(
                    url=parsed_url, patent_url=patent_url)
                patent_number = patent.xpath(
                    './/div[@class="number"]//strong/following-sibling::text()[1]').extract_first()
                abstract = patent.xpath(
                    './/div[@class="abstract"]//strong/following-sibling::text()[1]').extract_first()
                type = patent.xpath(
                    './/div[@class="type"]//strong/following-sibling::text()[1]').extract_first()
                date_filed = patent.xpath('//div[@class="date-filed"]//strong/following-sibling::text()[1]').extract_first()
                date_issued = patent.xpath(
                    './/div[@class="date-issued"]//strong/following-sibling::text()[1]').extract_first()
                assignees = patent.xpath(
                    './/div[@class="assignees"]//strong/following-sibling::text()[1]').extract_first()
                inventors = patent.xpath(
                    './/div[@class="inventors"]//strong/following-sibling::text()[1]').extract_first()
                l = ItemLoader(item=PatentItem())
                l.add_value('patent_number', patent_number.strip() if patent_number else '')
                l.add_value('title', title.strip() if title else '')
                l.add_value('abstract', abstract.strip() if abstract else '')
                l.add_value('type', type.strip() if type else '')
                l.add_value('date_filed', date_filed.strip() if date_filed else '')
                l.add_value('date_issued', date_issued.strip() if date_issued else '')
                l.add_value('assignees', assignees.strip() if assignees else '')
                l.add_value('inventors', inventors.strip() if inventors else '')
                l.add_value('url', combined_url)
                l.add_value('crawled_date', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                l.add_value('location', response.url)
                yield l.load_item()

            next_url = response.xpath('//div[@class="pagination"]//a[text()="next"]/@href').extract_first()
            if next_url:
                yield scrapy.Request('{url.scheme}://{url.netloc}{next_url}'.format(
                    url=parsed_url, next_url=next_url), callback=self.parse)
