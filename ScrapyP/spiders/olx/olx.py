# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import Item
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity


class OlxSpider(CrawlSpider):
    name = 'olx'
    allowed_domains = ['olx.com']
    start_urls = ['http://www.olx.com.pk/']
    custom_settings = {
        'DOWNLOAD_DELAY' = '3',
        'USER_AGENT' = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }
    rules = (
            Rule(LinkExtractor(restrict_css='.olxpk__categories--menu'),),
            Rule(LinkExtractor(
                restrict_css='.selectcatbox'), callback=self.parse_listing),
            )

    def parse_listing(self, response):

        for url in self.get_all_pages(response):
            yield Request(url=url, callback=self.parse_listing)

        for url in self.get_items_urls(response):
            yield Request(url=url, callback=self.parse_item,
                          meta={'cat: {}'.format(self.get_category(response))})

    def parse_item(self, response):
        item = DateItemLoader(DataItem, response)
        item.add_css('phone_no', '.fnormal::text')
        item.add_css('name', '.userdetails span::text')
        item.add_css('location', '.show-map-link::text')
        item.add_value('category', response.meta['cat'])
        return item.load_item()

    def get_items_urls(self, response):
        return response.css('.lpv-item-link::attr(href)').extract()

    def get_category(self, response):
        return response.css('.breadcrumb li h1::text').extract_first()

    def get_all_pages(self, response):
        return response.css('.pager span a::attr(href)').extract()


class DataItem(Item):
    id = scrapy.Field()
    name = scrapy.Field()
    phone_no = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()


def _clean_in(self, values):
    values = [re.sub('\s+', ' ', x).strip() for x in values if x]
    return [x for x in values if x]


class DateItemLoader(ItemLoader):
    default_item_class = DataItem
    default_input_processor = _clean_in
    default_output_processor = TakeFirst()
