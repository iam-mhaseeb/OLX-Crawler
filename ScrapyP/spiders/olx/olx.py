# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class OlxSpider(CrawlSpider):
    name = 'olx'
    allowed_domains = ['olx.com']
    start_urls = ['http://www.olx.com.pk/']
    rules = (
            Rule(LinkExtractor(restrict_css='.olxpk__categories--menu'),),
            Rule(LinkExtractor(
                restrict_css='.selectcatbox'),callback=self.parse_listing),
            )

    def parse_listing(self, response):
        pass


class DataItem(Item):
    id = scrapy.Field()
    name = scrapy.Field()
    phone_no = scrapy.Field()
    category = scrapy.Field()
